"""
Tests of sql_encoding: papoitem texts without accents or ñ, in SQL scripts with only ASCII.

Run: python3 -m unittest discover -s .claude/skills/papo-qa/scripts/tests -v
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import sql_encoding as se


class SqlEncodingTest(unittest.TestCase):
	def test_plainRemovesAccentsAndEnye(self):
		self.assertEqual(se.plain(u"Verificación del Daño: ÁÉÍÓÚ Ñ ü plàstico"), u"Verificacion del Dano: AEIOU N u plastico")

	def test_plainKeepsOtherSymbols(self):
		self.assertEqual(se.plain(u"¿Huella 3.5 ± 0.5 mm, 20 °C, Ø?"), u"¿Huella 3.5 ± 0.5 mm, 20 °C, Ø?")

	def test_scriptSetTextWithoutAccents(self):
		sql = u"-- Preguntas · producción\nUPDATE papoitem SET Description = N'Verificación ''QA'' ±1' WHERE ID = 280; -- antes: N'Verificacion'\n"
		out = se.to_ascii(sql)
		self.assertTrue(all(ord(c) < 128 for c in out))
		self.assertIn(u"SET Description = N'Verificacion ''QA'' ' + NCHAR(177) + N'1' WHERE ID = 280;", out)

	def test_whereKeepsItsText(self):
		sql = u"UPDATE papoitem SET Description = (N'PRESI' + NCHAR(211) + N'N') WHERE ID = 3030 AND Description = (N'PRESIa' + NCHAR(194) + NCHAR(147) + N'N');"
		out = se.to_ascii(sql)
		self.assertIn(u"SET Description = N'PRESION' WHERE", out)
		self.assertIn(u"AND Description = (N'PRESIa' + NCHAR(194) + NCHAR(147) + N'N');", out)


if __name__ == "__main__":
	unittest.main()
