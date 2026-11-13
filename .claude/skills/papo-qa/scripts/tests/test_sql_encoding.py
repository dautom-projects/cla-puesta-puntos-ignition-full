"""
Tests of sql_encoding: SQL scripts with only ASCII and the repair of the weird symbols of papoitem.

Run: python3 -m unittest discover -s .claude/skills/papo-qa/scripts/tests -v
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import sql_encoding as se

QUESTIONS = [
	u"Verificación dimensional de la placa con galga según procedimiento",
	u"¿Tengo todos los elementos de protección personal?",
	u"PRESIÓN DE AIRE 6,2 bar +/- 0,2 bar",
	u"Huella 3.5 ± 0.5 mm, Ø interno, Daño, Ñandú, Ü",
	u"La presión es la correcta (80–100 psi) ↑→↓← plàsticos",
]


def damage(text, enc):
	return "".join(se.misread(c, enc) if ord(c) > 127 else c for c in text)


def repair(text):
	for bad, good in se.patterns():
		text = text.replace(bad, good)
	return text


class SqlEncodingTest(unittest.TestCase):
	def test_asciiScriptKeepsTheText(self):
		sql = u"-- Preguntas · producción\nUPDATE papoitem SET Description = N'Verificación ''QA''' WHERE ID = 280; -- antes: N'Verificacion'\n"
		out = se.to_ascii(sql)
		self.assertTrue(all(ord(c) < 128 for c in out))
		self.assertIn(u"(N'Verificaci' + NCHAR(243) + N'n ''QA''')", out)
		self.assertEqual(se.evaluate("(N'Verificaci' + NCHAR(243) + N'n ''QA''')"), u"Verificación 'QA'")

	def test_scriptReadAsWindows1252WouldDamageIt(self):
		# What SSMS writes when it opens a UTF-8 script as Windows-1252
		self.assertEqual(damage(u"Verificación", "cp1252"), u"VerificaciÃ³n")
		self.assertEqual(damage(u"¿Tengo", "cp1252"), u"Â¿Tengo")

	def test_repairUndoesBothEncodings(self):
		for text in QUESTIONS:
			for enc in ("cp1252", "latin-1"):
				self.assertEqual(repair(damage(text, enc)), text, (text, enc))

	def test_repairKeepsGoodText(self):
		for text in QUESTIONS:
			self.assertEqual(repair(text), text)

	def test_repairScriptIsAscii(self):
		script = se.repair_script()
		self.assertTrue(all(ord(c) < 128 for c in script))
		self.assertIn("papoitem_bak_20261113", script)


if __name__ == "__main__":
	unittest.main()
