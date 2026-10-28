"""
Tests of papo_core.items.getCycleSum and getCycleRegisters (FO10-0100 Ing. Baterias: table and total of the form).

The Project Library module runs on a simulated gateway: SQLite instead of SQL Server (TOP 1 is rewritten as LIMIT 1)
and a stand-in for the form component (view.params, view.custom). The open cycle is the last RegisterCode of the
station; only the registers of the form's type count.

Run: python3 -m unittest discover -s .claude/skills/papo-qa/scripts/tests -v
"""

import datetime
import json
import os
import re
import sqlite3
import types
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ITEMS = os.path.join(HERE, "..", "..", "..", "..", "..", "cla-project", "ignition", "script-python", "papo_core", "items", "code.py")
FMT = "%Y-%m-%d %H:%M:%S"


class Dataset(object):
	def __init__(self, cursor):
		self.headers = [d[0] for d in cursor.description]
		self.rows = cursor.fetchall()

	def getRowCount(self):
		return len(self.rows)

	def getValueAt(self, row, col):
		value = self.rows[row][col if isinstance(col, int) else self.headers.index(col)]
		if isinstance(value, str) and len(value) == 19 and value[4] == "-" and value[10] == " ":
			return datetime.datetime.strptime(value, FMT)
		return value


class FakeSystem(object):
	def __init__(self, conn):
		self.conn, self.errors = conn, []
		system = self

		class Logger(object):
			def __init__(self, name):
				pass

			def error(self, msg):
				system.errors.append(msg)

		self.util = types.SimpleNamespace(getLogger=Logger, jsonDecode=lambda text: json.loads(text))
		self.date = types.SimpleNamespace(format=lambda date, pattern: date.strftime(pattern.replace("HH", "%H").replace("mm", "%M")))
		self.db = types.SimpleNamespace(runPrepQuery=self._query)

	def _query(self, sql, params, db):
		# SQL Server TOP 1 ... ORDER BY ... ) -> SQLite ... ORDER BY ... LIMIT 1 )
		sql = re.sub(r"SELECT TOP 1 (.*?)\)", lambda m: "SELECT " + m.group(1).rstrip() + " LIMIT 1\n)", sql, flags=re.S)
		return Dataset(self.conn.execute(sql, params))


def loadItems(system):
	module = {"system": system, "unicode": str, "basestring": str}
	with open(ITEMS, encoding="utf-8") as source:
		exec(compile(source.read(), ITEMS, "exec"), module)
	return module


def form(station=13, papo=56, registerType=16):
	view = types.SimpleNamespace(params=types.SimpleNamespace(workstationnodeID=station, papoID=papo),
		custom=types.SimpleNamespace(registerTypeID=registerType, dbConnection="papo_db", referencePapo="FO10-0100"))
	return types.SimpleNamespace(view=view)


class CycleItemsTest(unittest.TestCase):
	def setUp(self):
		self.conn = sqlite3.connect(":memory:")
		self.conn.execute("CREATE TABLE registerhistory (ID INTEGER PRIMARY KEY AUTOINCREMENT, [Timestamp] TEXT, DataAnswer TEXT, "
			"Status TEXT, PapoID INTEGER, RegisterTypeID INTEGER, [User] TEXT, WorkstationNodeID INTEGER, RegisterCode INTEGER)")
		self.system = FakeSystem(self.conn)
		self.items = loadItems(self.system)

	def tearDown(self):
		self.conn.close()
		self.assertEqual(self.system.errors, [])

	def save(self, when, rtype, code, answers, station=13, user="oper", status="En proceso", insights=" | T: 3"):
		data = {"items": [{"papoItemID": k, "answer": v, "registerTypeID": rtype} for k, v in answers.items()]
			+ [{"insights": insights, "registerTypeID": rtype, "user": user, "timestamp": when}]}
		self.conn.execute("INSERT INTO registerhistory ([Timestamp], DataAnswer, Status, PapoID, RegisterTypeID, [User], "
			"WorkstationNodeID, RegisterCode) VALUES (?, ?, ?, 56, ?, ?, ?, ?)", (when, json.dumps(data), status, rtype, user, station, code))

	def cycle(self):
		# Cycle 2 closed (Inicio, one entry, Fin, signatures); cycle 3 open with Inicio and two entries on two tables
		self.save("2026-10-28 06:10:00", 7, 2, {6601: "Cumple"})
		self.save("2026-10-28 07:00:00", 16, 2, {6623: 4, 6629: "50"})
		self.save("2026-10-28 13:50:00", 10, 2, {}, status="Finalizado")
		self.save("2026-10-28 13:50:00", 12, 3, {}, status="Sin Iniciar")
		self.save("2026-10-28 14:05:00", 7, 3, {6601: "Cumple"})
		self.save("2026-10-28 14:30:00", 16, 3, {6623: 18, 6624: "No Cumple", 6626: 113, 6629: "10", 6630: "14:31:00", 6640: "10"},
			insights="Mesa lenta | T: 3, H: 14:28 - oper")
		self.save("2026-10-28 15:10:00", 16, 3, {6623: 7.0, 6624: "Cumple", 6626: 120, 6629: "5,5", 6640: "15,5"}, user="oper2")
		self.save("2026-10-28 15:20:00", 16, 3, {6623: 18, 6629: "8"}, station=44)  # another station

	def test_totalAddsEveryEntryOfTheCycle(self):
		self.cycle()
		self.assertEqual(self.items["getCycleSum"](form(), 6629, None, None, "4"), "19.5")

	def test_totalWithoutTheValueBeingEntered(self):
		self.cycle()
		self.assertEqual(self.items["getCycleSum"](form(), 6629, None, None, ""), "15.5")

	def test_totalByTableStillWorks(self):
		self.cycle()
		self.assertEqual(self.items["getCycleSum"](form(), 6629, 6623, "18", "2"), "12")
		self.assertEqual(self.items["getCycleSum"](form(), 6629, 6623, "", "2"), "")

	def test_newCycleStartsAtTheValueBeingEntered(self):
		self.cycle()
		self.save("2026-10-28 21:55:00", 10, 3, {}, status="Finalizado")
		self.save("2026-10-28 21:55:00", 12, 4, {}, status="Sin Iniciar")
		self.assertEqual(self.items["getCycleSum"](form(), 6629, None, None, "3"), "3")
		self.assertEqual(self.items["getCycleRegisters"](form(), {"cantidad": 6629}), [])

	def test_tableListsTheEntriesOfTheCycle(self):
		self.cycle()
		rows = self.items["getCycleRegisters"](form(), {"hora": "time", "mesa": 6623, "combinada": 6624, "referencia": 6626,
			"cantidad": 6629, "inicio": 6630, "operario": "user", "observaciones": "insights"}, ["combinada"])
		self.assertEqual(rows, [
			{"hora": "14:30", "mesa": "18", "combinada": u"\u2718", "referencia": "113", "cantidad": "10", "inicio": "14:31:00",
				"operario": "oper", "observaciones": "Mesa lenta | T: 3, H: 14:28 - oper"},
			{"hora": "15:10", "mesa": "7", "combinada": u"\u2714", "referencia": "120", "cantidad": "5,5", "inicio": "",
				"operario": "oper2", "observaciones": "| T: 3"},
		])

	def test_emptyStation(self):
		self.assertEqual(self.items["getCycleRegisters"](form(station=99), {"cantidad": 6629}), [])
		self.assertEqual(self.items["getCycleSum"](form(station=99), 6629, None, None, ""), "")


if __name__ == "__main__":
	unittest.main()
