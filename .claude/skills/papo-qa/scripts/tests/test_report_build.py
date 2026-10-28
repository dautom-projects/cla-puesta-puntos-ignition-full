"""
Tests of papo_core.report.build(): one call fills the report data from its list of sections, reading only the
cycle of the report station when the viewer passes workstationNodeID. The Project Library module runs here on
a simulated gateway: SQLite instead of SQL Server, json instead of system.util.jsonDecode and small stand-ins
for java.util.Date and java.text.SimpleDateFormat. Cases taken from the F&A pilot (AC10-0202, AC10-0301,
AC10-1101, CA02-2102).

Run: python3 -m unittest discover -s .claude/skills/papo-qa/scripts/tests -v
"""

import builtins
import datetime
import io
import json
import os
import sqlite3
import sys
import types
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.join(HERE, "..", "..", "..", "..", "..", "cla-project", "ignition", "script-python", "papo_core", "report", "code.py")


# ---- simulated gateway ----------------------------------------------------------------------------------

class JDate(object):
	"""java.util.Date stand-in around a datetime."""
	def __init__(self, dt):
		self.dt = dt

	def __eq__(self, other):
		return isinstance(other, JDate) and self.dt == other.dt

	def __repr__(self):
		return "JDate({})".format(self.dt)


BOGOTA = datetime.timezone(datetime.timedelta(hours=-5))


class SimpleDateFormat(object):
	FORMATS = {"EEE MMM dd HH:mm:ss Z yyyy": "%a %b %d %H:%M:%S %z %Y", "HH:mm:ss": "%H:%M:%S"}

	def __init__(self, fmt, locale=None):
		self.fmt = self.FORMATS.get(fmt)
		self.zone = None

	def setTimeZone(self, zone):
		self.zone = zone

	def parse(self, text):
		if self.fmt is None or "%z" not in self.fmt:
			raise ValueError(text)
		return JDate(datetime.datetime.strptime(text, self.fmt))

	def format(self, date):
		return date.dt.astimezone(self.zone).strftime(self.fmt)


def _plantShift(date):
	"""papo_core.ui.getShift stand-in: T1 22-06, T2 06-14, T3 14-22 in America/Bogota."""
	hour = date.dt.astimezone(BOGOTA).hour
	return 1 if hour >= 22 or hour < 6 else (2 if hour < 14 else 3)


def _javaModules():
	java = types.ModuleType("java")
	util = types.ModuleType("java.util")
	text = types.ModuleType("java.text")
	util.Date = JDate
	util.Locale = types.SimpleNamespace(US="US")
	util.TimeZone = types.SimpleNamespace(getTimeZone=lambda name: BOGOTA)
	text.SimpleDateFormat = SimpleDateFormat
	java.util, java.text = util, text
	# Jython imports a Java class like a module (import java.util.Date)
	java.__path__, util.__path__ = [], []
	return {"java": java, "java.util": util, "java.text": text, "java.util.Date": JDate}


class Dataset(object):
	"""Enough of a Dataset / PyDataSet for the report module."""
	def __init__(self, headers, rows):
		self.headers, self.rows = list(headers), [list(r) for r in rows]

	def getRowCount(self):
		return len(self.rows)

	def getColumnCount(self):
		return len(self.headers)

	def getColumnName(self, i):
		return self.headers[i]

	def getValueAt(self, row, col):
		return self.rows[row][col if isinstance(col, int) else self.headers.index(col)]


class FakeSystem(object):
	def __init__(self, conn):
		self.conn = conn
		self.queries = []
		self.errors = []
		system = self

		class Logger(object):
			def __init__(self, name):
				self.name = name

			def error(self, msg):
				system.errors.append(msg)

			def info(self, msg):
				pass

		self.db = types.SimpleNamespace(runPrepQuery=self._query)
		self.util = types.SimpleNamespace(jsonDecode=json.loads, getLogger=Logger)
		self.dataset = types.SimpleNamespace(toDataSet=self._toDataSet)
		self.date = types.SimpleNamespace(getHour24=lambda d: d.dt.hour, fromMillis=lambda ms: JDate(datetime.datetime.fromtimestamp(ms / 1000.0)))

	def _query(self, sql, params, db):
		self.queries.append((sql, list(params)))
		cur = self.conn.execute(sql, list(params))
		headers = [c[0] for c in cur.description]
		return Dataset(headers, cur.fetchall())

	def _toDataSet(self, headers, rows=None):
		if rows is None:
			return Dataset(headers.headers, headers.rows)
		return Dataset(headers, rows)


def _answer(items, user="Soporte D.", when="Tue Oct 27 19:43:47 COT 2026", insight=" | T: 3 - QA"):
	rows = [{"papoItemID": pid, "answer": value, "registerTypeID": 7} for pid, value in items]
	rows.append({"insights": insight, "registerTypeID": 7, "user": user, "timestamp": when})
	return json.dumps({"items": rows})


def _signature(name, lastname, roles=("Administrator", "Supervisor_PAPO")):
	return json.dumps({"role": list(roles), "name": name, "user": "admin", "lastname": lastname})


def _loadReport(conn):
	"""Run papo_core/report/code.py as the gateway would, with the simulated system."""
	saved = {k: sys.modules.get(k) for k in ("java", "java.util", "java.text", "java.util.Date")}
	sys.modules.update(_javaModules())
	builtins.basestring, builtins.long, builtins.unicode = str, int, str
	module = types.ModuleType("papo_core.report")
	module.system = FakeSystem(conn)
	module.papo_core = types.SimpleNamespace(ui=types.SimpleNamespace(getShift=_plantShift))
	with io.open(REPORT, encoding="utf-8") as f:
		exec(compile(f.read(), REPORT, "exec"), module.__dict__)
	return module, saved


class ReportBuildTest(unittest.TestCase):
	def setUp(self):
		self.conn = sqlite3.connect(":memory:")
		self.conn.executescript("""
			CREATE TABLE papo (ID INTEGER, Reference TEXT, MasterPapoID INTEGER);
			CREATE TABLE registertype (ID INTEGER, Description TEXT);
			CREATE TABLE registerhistory (ID INTEGER, PapoID INTEGER, NodeID INTEGER, WorkstationNodeID INTEGER,
				RegisterCode INTEGER, RegisterTypeID INTEGER, Status TEXT, [User] TEXT, Timestamp TEXT, DataAnswer TEXT);
			INSERT INTO papo VALUES (18, 'AC10-0202', NULL);
			INSERT INTO registertype VALUES (7, 'Inicio de turno'), (4, 'Cuatro horas'), (8, 'Fin de turno'), (10, 'Firma');
		""")
		rows = [
			# Station 7 of node 30, cycle 1
			(1, 7, 7, "En proceso", "Soporte D.", "2026-10-27 19:43:47", _answer([(6100, "Cumple"), (6101, 12.34), (6115, "No Cumple")])),
			(2, 4, 7, "En proceso", "Soporte D.", "2026-10-27 19:44:10", _answer([(6110, "No Cumple")], insight=" | T: 3 - 4h")),
			(3, 7, 7, "En proceso", "Otro U.", "2026-10-27 19:45:00", _answer([(6100, "No Cumple"), (6115, "Cumple")], user="Otro U.")),
			(4, 8, 7, "En proceso", "Soporte D.", "2026-10-27 19:46:00", _answer([(6117, "Cumple"), (6120, "No Cumple")])),
			(5, 10, 7, "Revisado", "admin", "2026-10-28 00:46:30", _signature("Super", "Visor")),
			(6, 10, 7, "Finalizado", "admin", "2026-10-27 19:47:00", _signature("Soporte", "D.", ("Operator", "Supervisor_PAPO"))),
			# Station 9 of the same node, also numbered cycle 1
			(7, 7, 9, "En proceso", "Estacion B", "2026-03-05 11:01:34", _answer([(6100, "Cumple")], user="Estacion B", insight=" | otra estacion")),
		]
		for rid, typeID, station, status, user, ts, answer in rows:
			self.conn.execute("INSERT INTO registerhistory VALUES (?, 18, 30, ?, 1, ?, ?, ?, ?, ?)",
				(rid, station, typeID, status, user, ts, answer))
		self.report, self.saved = _loadReport(self.conn)

	def tearDown(self):
		self.conn.close()
		for k, v in self.saved.items():
			if v is None:
				sys.modules.pop(k, None)
			else:
				sys.modules[k] = v

	def _data(self, station=None):
		data = {"papoID": 18, "nodeID": 30, "registerCode": 1, "db": "papo_db"}
		if station is not None:
			data["workstationNodeID"] = station
		return data

	def _pilot(self, data):
		self.report.build(data, [
			{"types": [3, 5, 6, 7], "name": "register", "reprocessedIds": [6115], "reprocessedName": "reprocesed"},
			{"types": [4], "name": "fourhour"},
			{"types": [8], "name": "endShift", "reprocessedIds": [6117, 6120, 6121], "reprocessedName": "endShiftReprocesed"},
		])
		self.assertEqual(self.report.system.errors, [])
		return data

	def test_oneSlotPerRecord(self):
		data = self._pilot(self._data(station=7))
		self.assertEqual(data["register1"]["papoItemID6100"], u"✔")
		self.assertEqual(data["register1"]["papoItemID6101"], "12.3")
		self.assertEqual(data["register1"]["user"], "Soporte D.")
		self.assertEqual(data["register1"]["shift"], "3")
		self.assertEqual(data["register1"]["hora_registro"], "19:43:47")
		self.assertEqual(data["register2"]["papoItemID6100"], u"✘")
		self.assertNotIn("register3", data)
		self.assertEqual(data["fourhour1"]["papoItemID6110"], u"✘")
		self.assertEqual(data["endShift1"]["papoItemID6117"], u"✔")

	def test_reprocessedMarksPerSlot(self):
		data = self._pilot(self._data(station=7))
		self.assertEqual(data["reprocesed1"], {"nocumplepapoItemID6115": u"✘"})
		self.assertEqual(data["reprocesed2"], {"cumplepapoItemID6115": u"✔"})
		self.assertEqual(data["endShiftReprocesed1"], {"cumplepapoItemID6117": u"✔", "nocumplepapoItemID6120": u"✘"})

	def test_reprocessedNormalizeApart(self):
		data = self._data(station=7)
		self.report.build(data, [{"types": [3, 5, 6, 7], "name": "register", "normalize": "yn", "reprocessedIds": [6115],
			"reprocessedName": "reprocesed", "reprocessedNormalize": "ok"}], history=None)
		self.assertEqual(data["register1"]["papoItemID6100"], "Si")
		self.assertEqual(data["reprocesed1"], {"nocumplepapoItemID6115": "N OK"})
		self.assertEqual(data["reprocesed2"], {"cumplepapoItemID6115": "OK"})

	def test_reprocessedGroupsAndModes(self):
		data = self._data(station=7)
		self.report.build(data, [{"types": [3, 5, 6, 7], "name": "startShift", "slot": "single", "reprocessed": [
			{"ids": [6115], "name": "reprocessed"},
			{"ids": [6115], "name": "yn", "mode": "yn"},
			{"ids": [6100], "name": "ok", "mode": "ok"},
			{"ids": [6101], "name": "number", "mode": "number"}]}], history=None)
		self.assertEqual(data["reprocessed"], {"nocumplepapoItemID6115": u"\u2718", "cumplepapoItemID6115": u"\u2714"})
		self.assertEqual(data["yn"], {"noItemID6115": u"\u2718", "siItemID6115": u"\u2714"})
		self.assertEqual(data["ok"], {"papoItemID6100": "NO OK"})
		self.assertEqual(data["number"], {"number12.34papoItemID": u"\u2718"})

	def test_typeNamePerSlot(self):
		data = self._data(station=7)
		self.report.build(data, [{"types": [3, 4, 5, 6, 7], "name": "register", "typeName": True}], history=None)
		self.assertEqual([data["register{}_type".format(i)] for i in (1, 2, 3)], ["Inicio de turno", "Cuatro horas", "Inicio de turno"])

	def test_signaturesLastOne(self):
		data = self._data(station=7)
		self.report.build(data, [], history=None, signatures="roleLast")
		self.assertEqual(data["firmaAdministrator"], "Soporte D.")
		self.assertEqual(data["firmaOperator"], "Soporte D.")
		self.assertNotIn("firmaAdministrator1", data)
		data = self._data(station=7)
		self.report.build(data, [], history=None, signatures="roleLast", signatureRoles=("INTEGRADOR",))
		self.assertNotIn("firmaAdministrator", data)

	def test_singleSlotMergesRecords(self):
		data = self._data(station=7)
		self.report.build(data, [{"types": [3, 5, 6, 7], "name": "startShift", "slot": "single"}], history=None)
		self.assertEqual(data["startShift"]["papoItemID6100"], u"✔")
		self.assertNotIn("startShift1", data)
		self.assertNotIn("RegisterHistoryStation", data)

	def test_stationKeepsItsOwnCycle(self):
		data = self._pilot(self._data(station=9))
		self.assertEqual(data["register1"]["user"], "Estacion B")
		self.assertNotIn("register2", data)
		self.assertNotIn("endShift1", data)
		self.assertEqual(data["comment"], "| otra estacion")
		self.assertEqual(data["RegisterHistoryStation"].getRowCount(), 1)

	def test_withoutStationReadsTheNodeAsBefore(self):
		data = self._pilot(self._data())
		self.assertEqual([data["register{}".format(i)]["user"] for i in (1, 2, 3)], ["Soporte D.", "Otro U.", "Estacion B"])
		self.assertEqual(data["RegisterHistoryStation"].getRowCount(), 7)

	def test_plantShiftNotTheOrecNumbering(self):
		# 09:15 is T2 for the plant (06-14); the OREC report scripts called it 3
		self.conn.execute("INSERT INTO registerhistory VALUES (8, 18, 30, 7, 2, 7, 'En proceso', 'x', '2026-10-28 09:15:00', ?)",
			(_answer([(6100, None)], when="Wed Oct 28 09:15:00 COT 2026"),))
		data = {"papoID": 18, "nodeID": 30, "registerCode": 2, "db": "papo_db"}
		self.report.build(data, [{"types": [7], "name": "shift"}], history=None)
		self.assertEqual(data["shift1"]["shift"], "2")
		self.assertEqual(data["shift1"]["hora_registro"], "09:15:00")
		self.assertEqual(data["shift1"]["papoItemID6100"], "")

	def test_comment(self):
		data = self._pilot(self._data(station=7))
		self.assertEqual(data["comment"], "| T: 3 - QA. | T: 3 - 4h")

	def test_signaturesByRoleAsTheReportScripts(self):
		data = self._pilot(self._data(station=7))
		# Supervisor_PAPO numbers the supervisor slots; a user with Operator also fills the operator key
		self.assertEqual(data["firmaAdministrator1"], "Super Visor")
		self.assertEqual(data["firmaAdministrator2"], "Soporte D.")
		self.assertEqual(data["firmaOperator"], "Soporte D.")
		self.assertNotIn("firmaAdministrator", data)
		self.assertNotIn("firmaOperator1", data)

	def test_signaturesByStatus(self):
		data = self._data(station=7)
		self.report.build(data, [], signatures="status")
		self.assertEqual(data["firmaAdministrator1"], "Super Visor")
		self.assertEqual(data["firmaAdministrator"], "Super Visor")
		self.assertEqual(data["firmaOperator1"], "Soporte D.")
		self.assertNotIn("firmaAdministrator2", data)

	def test_historyListLikeTheReportQuery(self):
		data = self._pilot(self._data(station=7))
		history = data["RegisterHistoryStation"]
		self.assertEqual(history.headers, ["Fecha", "Global ID", "Estado", "Tipo Registro", "RegisterTypeID"])
		self.assertEqual([history.getValueAt(i, "Tipo Registro") for i in range(history.getRowCount())],
			["Inicio de turno", "Cuatro horas", "Inicio de turno", "Fin de turno", "Firma", "Firma"])
		self.assertEqual(history.getValueAt(5, "Estado"), "Revisado")

	def test_everyQueryFiltersTheStation(self):
		self._pilot(self._data(station=7))
		cycleQueries = [q for q in self.report.system.queries if "registerhistory" in q[0]]
		self.assertEqual(len(cycleQueries), 6)
		for sql, params in cycleQueries:
			self.assertIn("WorkstationNodeID = ?", sql)
			self.assertEqual(params[3:5], [7, 7])

	def test_extractReportDataAutoStillRuns(self):
		self.conn.executescript("""
			CREATE TABLE papoitem (ID INTEGER, PapoID INTEGER);
			CREATE TABLE papoitem_registertype (PapoItemID INTEGER, RegisterTypeID INTEGER);
			INSERT INTO papoitem VALUES (6100, 18);
			INSERT INTO papoitem_registertype VALUES (6100, 7);
		""")
		data = self._data(station=7)
		self.report.extractReportDataAuto(data)
		self.assertEqual(self.report.system.errors, [])
		self.assertEqual(data["Iniciodeturno1"]["papoItemID6100"], u"✔")
		self.assertEqual(data["Iniciodeturno2"]["papoItemID6100"], u"✘")
		self.assertNotIn("Iniciodeturno3", data)


if __name__ == "__main__":
	unittest.main()
