"""
Tests of the time of the supervisor signature (papo_core.sign._insertSignature).

The "Revisado" must carry the gateway time, like the rest of the cycle. SQLite's CURRENT_TIMESTAMP is UTC, as the
SQL Server of develop: with the server time the signature lands 5 h ahead of the cycle.

Run: python3 -m unittest discover -s .claude/skills/papo-qa/scripts/tests -v
"""

import sqlite3
import unittest

from test_auto_close import FakeSystem, at, loadSign


class SignatureTimeTest(unittest.TestCase):
	def setUp(self):
		self.conn = sqlite3.connect(":memory:")
		self.conn.execute("""CREATE TABLE registerhistory (ID INTEGER PRIMARY KEY AUTOINCREMENT, [Timestamp] TEXT,
			DataAnswer TEXT, Status TEXT, PapoID INTEGER, RegisterTypeID INTEGER, [User] TEXT, WorkstationNodeID INTEGER,
			NodeID INTEGER, WorkstationID INTEGER, RegisterCode INTEGER)""")

	def test_signatureTakesTheGatewayTime(self):
		system = FakeSystem(self.conn, at("2026-10-29 09:30:00"))
		loadSign(system)["_insertSignature"]("papo_db", "{}", 31, "qa.supervisor", 21, 38, 16, 10)
		row = self.conn.execute("SELECT [Timestamp], Status, RegisterTypeID, RegisterCode FROM registerhistory").fetchone()
		self.assertEqual(row, ("2026-10-29 09:30:00", "Revisado", 10, 10))


if __name__ == "__main__":
	unittest.main()
