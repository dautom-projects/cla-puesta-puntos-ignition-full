"""
Tests of the supervisor signature record (papo_core.sign._insertSignature and signSupervisor).

The "Revisado" must carry the gateway time, like the rest of the cycle. SQLite's CURRENT_TIMESTAMP is UTC, as the
SQL Server of develop: with the server time the signature lands 5 h ahead of the cycle. Its role is the list of
the signer's roles, like Gestion and the popup save it (the session gives them as a Java array).

Run: python3 -m unittest discover -s .claude/skills/papo-qa/scripts/tests -v
"""

import json
import sqlite3
import types
import unittest

from test_auto_close import FakeSystem, at, loadSign


class JavaArray(object):
	"""Stand-in for the Java array of session.props.auth.user.roles: iterable, not a Python list."""

	def __init__(self, *items):
		self.items = items

	def __iter__(self):
		return iter(self.items)

	def __len__(self):
		return len(self.items)

	def __getitem__(self, i):
		return self.items[i]

	def __str__(self):
		return "<ArrayWrapper>: [{}]".format(", ".join("u'{}'".format(i) for i in self.items))


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

	def test_signatureKeepsEveryRoleAsAList(self):
		system = FakeSystem(self.conn, at("2026-10-29 09:30:00"))
		module = loadSign(system)
		module["alerts"] = types.SimpleNamespace(actionSuccess=lambda **kw: None)
		sign = types.SimpleNamespace(user="admin", role=JavaArray("Administrator", "Supervisor_PAPO"), name="Soporte", lastname="D.")
		root = types.SimpleNamespace(
			view=types.SimpleNamespace(params=types.SimpleNamespace(papoID=48, nodeID=72, workstationnodeID=38, workstationID=31),
				custom=types.SimpleNamespace(referencePapo="AC10-0501", registerCode=7, dbConnection="papo_db", sign=sign)))
		module["signSupervisor"](root)
		self.assertEqual(system.errors, [])
		data = json.loads(self.conn.execute("SELECT DataAnswer FROM registerhistory").fetchone()[0])
		self.assertEqual(data["role"], ["Administrator", "Supervisor_PAPO"])


if __name__ == "__main__":
	unittest.main()
