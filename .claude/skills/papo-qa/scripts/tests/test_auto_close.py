"""
Tests of papo_core.sign.autoCloseOpenForms (gateway scheduled script at 06:10, 14:10 and 22:10).

The Project Library module runs on a simulated gateway: SQLite instead of SQL Server and small stand-ins for
java.util.Calendar / TimeZone and system.date. Each case is a station with one cycle; the job runs at 14:10
(Turno 3 starts at 14:00) and closes only the cycles started before 14:00 that are still open.

Run: python3 -m unittest discover -s .claude/skills/papo-qa/scripts/tests -v
"""

import datetime
import json
import os
import sqlite3
import sys
import types
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SIGN = os.path.join(HERE, "..", "..", "..", "..", "..", "cla-project", "ignition", "script-python", "papo_core", "sign", "code.py")
BOGOTA = datetime.timezone(datetime.timedelta(hours=-5))
FMT = "%Y-%m-%d %H:%M:%S"


def at(text):
	return datetime.datetime.strptime(text, FMT).replace(tzinfo=BOGOTA)


class Calendar(object):
	"""java.util.Calendar stand-in for the fields the job uses."""
	HOUR_OF_DAY, MINUTE, SECOND, MILLISECOND, DAY_OF_MONTH = "hour", "minute", "second", "microsecond", "day"

	def __init__(self):
		self.dt = None

	@classmethod
	def getInstance(cls, zone=None):
		return cls()

	def setTime(self, date):
		self.dt = date.astimezone(BOGOTA)

	def get(self, field):
		return getattr(self.dt, field)

	def set(self, field, value):
		self.dt = self.dt.replace(**{field: value})

	def add(self, field, amount):
		self.dt = self.dt + datetime.timedelta(days=amount)

	def getTime(self):
		return self.dt


class Dataset(object):
	def __init__(self, cursor):
		self.headers = [d[0] for d in cursor.description]
		self.rows = cursor.fetchall()

	def getRowCount(self):
		return len(self.rows)

	def getValueAt(self, row, col):
		value = self.rows[row][col if isinstance(col, int) else self.headers.index(col)]
		if isinstance(value, str) and len(value) == 19 and value[4] == "-" and value[10] == " ":
			return at(value)
		return value


class FakeSystem(object):
	def __init__(self, conn, now):
		self.conn, self.errors = conn, []
		system = self

		class Logger(object):
			def __init__(self, name):
				pass

			def error(self, msg):
				system.errors.append(msg)

			def info(self, msg):
				pass

		self.util = types.SimpleNamespace(getLogger=Logger, jsonEncode=lambda v: json.dumps(v))
		self.date = types.SimpleNamespace(now=lambda: now, isBefore=lambda a, b: a < b)
		self.db = types.SimpleNamespace(runPrepQuery=self._query, runPrepUpdate=self._update)

	def _args(self, params):
		return [p.strftime(FMT) if isinstance(p, datetime.datetime) else p for p in params]

	def _query(self, sql, params, db):
		return Dataset(self.conn.execute(sql, self._args(params)))

	def _update(self, sql, params, db):
		self.conn.execute(sql, self._args(params))


def plantShift(date):
	hour = date.astimezone(BOGOTA).hour
	return 1 if hour >= 22 or hour < 6 else (2 if hour < 14 else 3)


def javaModules():
	"""java.util as Jython imports it inside the functions (Calendar, TimeZone)."""
	java = types.ModuleType("java")
	util = types.ModuleType("java.util")
	util.Calendar = Calendar
	util.TimeZone = types.SimpleNamespace(getTimeZone=lambda name: BOGOTA)
	java.util = util
	return {"java": java, "java.util": util}


def loadSign(system):
	module = {"system": system, "papo_core": types.SimpleNamespace(ui=types.SimpleNamespace(getShift=plantShift))}
	with open(SIGN, encoding="utf-8") as source:
		exec(compile(source.read(), SIGN, "exec"), module)
	return module


class AutoCloseTest(unittest.TestCase):
	def setUp(self):
		# The job imports java.util when it runs: keep the stand-ins installed for the whole test
		self.savedModules = {k: sys.modules.get(k) for k in ("java", "java.util")}
		sys.modules.update(javaModules())
		self.conn = sqlite3.connect(":memory:")
		self.conn.executescript("""
			CREATE TABLE node (ID INTEGER, Type TEXT, Name TEXT, ParentNodeID INTEGER);
			CREATE TABLE registerhistory (ID INTEGER PRIMARY KEY AUTOINCREMENT, [Timestamp] TEXT, DataAnswer TEXT,
				Status TEXT, PapoID INTEGER, RegisterTypeID INTEGER, [User] TEXT, WorkstationNodeID INTEGER,
				NodeID INTEGER, WorkstationID INTEGER, RegisterCode INTEGER);
		""")
		# Andina: F&A (28) > Granja de acidos (29) and Terminado (31) > cells 70, 74; Metalurgia (4) > Fundicion (8) > cell 100
		self.conn.executemany("INSERT INTO node VALUES (?, ?, ?, ?)", [
			(2, "SITE", "Andina", 1), (28, "AREA", "F&A", 2), (29, "LINE", "Granja de acidos", 28),
			(31, "LINE", "Terminado", 28), (70, "CELL", "Llenadora final", 31), (74, "CELL", "Termoencogible", 31),
			(4, "AREA", "Metalurgia", 2), (8, "LINE", "Fundicion", 4), (100, "CELL", "Horno", 8)])

	def tearDown(self):
		for k, v in self.savedModules.items():
			if v is None:
				sys.modules.pop(k, None)
			else:
				sys.modules[k] = v

	def cycle(self, papo, station, node, code, rows):
		# rows: (time, status, type); the supervisor signs as "super", every other row is the operator's
		for when, status, rtype in rows:
			user = "super" if status == "Revisado" else "oper"
			self.conn.execute("INSERT INTO registerhistory ([Timestamp], DataAnswer, Status, PapoID, RegisterTypeID, [User], "
				"WorkstationNodeID, NodeID, WorkstationID, RegisterCode) VALUES (?, '{}', ?, ?, ?, ?, ?, ?, 1, ?)",
				(when, status, papo, rtype, user, station, node, code))

	def runJob(self, now="2026-10-28 14:10:00"):
		system = FakeSystem(self.conn, at(now))
		closed = loadSign(system)["autoCloseOpenForms"]("papo_db")
		self.assertEqual(system.errors, [])
		return closed

	def closings(self, papo):
		return self.conn.execute("SELECT Status, RegisterTypeID, RegisterCode, DataAnswer FROM registerhistory "
			"WHERE PapoID = ? AND [Timestamp] = '2026-10-28 14:10:00' ORDER BY ID", (papo,)).fetchall()

	def test_closesCycleOfThePreviousShift(self):
		self.cycle(1, 37, 70, 5, [("2026-10-28 10:00:00", "En proceso", 7), ("2026-10-28 12:30:00", "En proceso", 3)])
		self.assertEqual(self.runJob(), 1)
		rows = self.closings(1)
		self.assertEqual([(r[0], r[1], r[2]) for r in rows], [("Finalizado", 10, 5), ("Sin Iniciar", 12, 6)])
		self.assertEqual(json.loads(rows[0][3])["comment"], "T: 2, H: 14:10 - Cierre automatico")

	def test_leavesFormOpenedInTheGraceMinutes(self):
		self.cycle(2, 38, 70, 3, [("2026-10-28 14:03:00", "En proceso", 7)])
		self.assertEqual(self.runJob(), 0)
		self.assertEqual(self.closings(2), [])

	def test_cycleStartedBeforeWithActivityAfterIsClosed(self):
		self.cycle(3, 39, 70, 8, [("2026-10-28 13:50:00", "En proceso", 7), ("2026-10-28 14:05:00", "En proceso", 3)])
		self.assertEqual(self.runJob(), 1)

	def test_excludesGranjaAndMetalurgiaByNode(self):
		self.cycle(4, 11, 29, 2, [("2026-10-28 09:00:00", "En proceso", 7)])     # Granja de acidos (line)
		self.cycle(5, 68, 100, 2, [("2026-10-28 09:00:00", "En proceso", 7)])    # Metalurgia cell
		self.cycle(6, 69, 8, 2, [("2026-10-28 09:00:00", "En proceso", 7)])      # Metalurgia line
		self.assertEqual(self.runJob(), 0)

	def test_stationNumberIsNotTakenForANode(self):
		# Station 29 (Termoencogible) shares its number with the Granja de acidos node: it must be closed
		self.cycle(7, 29, 74, 4, [("2026-10-28 09:00:00", "En proceso", 7)])
		self.assertEqual(self.runJob(), 1)

	def test_closesCycleLeftAtTheSupervisorSignature(self):
		self.cycle(8, 40, 70, 6, [("2026-10-28 07:00:00", "En proceso", 7), ("2026-10-28 08:00:00", "Revisado", 10)])
		self.assertEqual(self.runJob(), 1)
		self.assertEqual([(r[0], r[2]) for r in self.closings(8)], [("Finalizado", 6), ("Sin Iniciar", 7)])
		users = self.conn.execute("SELECT DISTINCT [User] FROM registerhistory WHERE PapoID = 8 AND [Timestamp] = '2026-10-28 14:10:00'").fetchall()
		self.assertEqual(users, [("oper",)])  # the operator, not the supervisor who signed last

	def test_emptyCycleAfterALateSignatureIsLeftAlone(self):
		# The operator closed cycle 6; the supervisor signed afterwards on the empty cycle 7: nothing to close
		self.cycle(12, 44, 81, 6, [("2026-10-28 09:30:00", "En proceso", 16), ("2026-10-28 09:36:00", "Finalizado", 10)])
		self.cycle(12, 44, 81, 7, [("2026-10-28 09:36:00", "Sin Iniciar", 12), ("2026-10-28 09:37:00", "Revisado", 10)])
		self.assertEqual(self.runJob(), 0)

	def test_closedCyclesAreLeftAlone(self):
		self.cycle(9, 41, 70, 2, [("2026-10-28 07:00:00", "En proceso", 7), ("2026-10-28 13:00:00", "Finalizado", 10)])
		self.cycle(9, 41, 70, 3, [("2026-10-28 13:00:00", "Sin Iniciar", 12)])
		self.assertEqual(self.runJob(), 0)

	def test_nightShiftRunSeesTheDayBefore(self):
		# 06:10 closes what started before 06:00, including the night shift that began at 22:00 the day before
		self.cycle(10, 42, 70, 1, [("2026-10-27 23:30:00", "En proceso", 7)])
		self.cycle(11, 43, 70, 1, [("2026-10-28 06:02:00", "En proceso", 7)])
		system = FakeSystem(self.conn, at("2026-10-28 06:10:00"))
		closed = loadSign(system)["autoCloseOpenForms"]("papo_db")
		self.assertEqual(closed, 1)
		row = self.conn.execute("SELECT DataAnswer FROM registerhistory WHERE PapoID = 10 AND RegisterTypeID = 10").fetchone()
		self.assertEqual(json.loads(row[0])["comment"], "T: 1, H: 06:10 - Cierre automatico")


if __name__ == "__main__":
	unittest.main()
