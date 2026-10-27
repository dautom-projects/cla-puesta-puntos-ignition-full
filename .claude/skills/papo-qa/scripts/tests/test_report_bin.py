"""
Tests of report_bin: the text records of a report data.bin are rewritten without touching any other byte.

Run: python3 -m unittest discover -s .claude/skills/papo-qa/scripts/tests -v
"""

import glob
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import report_bin as rb

REPORTS = os.path.join(HERE, "..", "..", "..", "..", "..", "cla-project", "com.inductiveautomation.reporting", "reports")


def _copy(name):
	folder = tempfile.mkdtemp(prefix="report-bin-test-")
	path = os.path.join(folder, "data.bin")
	shutil.copy2(os.path.join(REPORTS, name, "data.bin"), path)
	return path


class ReportBinTest(unittest.TestCase):
	def test_roundTripEveryReport(self):
		paths = glob.glob(os.path.join(REPORTS, "**", "data.bin"), recursive=True)
		self.assertTrue(paths)
		for path in paths:
			self.assertTrue(rb.roundTrip(path)[0], path)

	def test_replaceTemplateKeepsTheRest(self):
		path = _copy("Clarios/Andina/F&A/PT11-0104")
		before = rb.ReportBin(path)
		doc = rb.ReportBin(path)
		doc.replaceTemplate("@register1.cumple.papoItemID6256@", "@register1.cumple.papoItemID6256X@")
		doc.save()
		after = rb.ReportBin(path)
		self.assertIn("@register1.cumple.papoItemID6256X@", after.template())
		self.assertEqual(after.script(), before.script())
		self.assertEqual(after.template().replace("6256X@", "6256@"), before.template())

	def test_replaceScriptKeepsTheTemplate(self):
		path = _copy("Clarios/Andina/Metalurgia/PA11-0401")
		before = rb.ReportBin(path)
		doc = rb.ReportBin(path)
		line = next(l for l in doc.script().splitlines(True) if l.strip() and doc.script().count(l) == 1)
		doc.replaceScript(line, line + "\t# test\n")
		doc.save()
		after = rb.ReportBin(path)
		self.assertEqual(after.template(), before.template())
		self.assertEqual(len(after.raw) - len(before.raw), len(after.script().encode("utf-8")) - len(before.script().encode("utf-8")))

	def test_textMustAppearOnce(self):
		doc = rb.ReportBin(_copy("Clarios/Andina/F&A/PT11-0104"))
		with self.assertRaises(ValueError):
			doc.replaceTemplate("@register1.", "@registerX.")


if __name__ == "__main__":
	unittest.main()
