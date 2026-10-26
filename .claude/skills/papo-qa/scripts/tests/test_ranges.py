"""
Tests of ranges.py: the closed range of a numeric field comes from running its own color script, and a red
that is not a closed range leaves the field native. Cases taken from F&A/Form_AC10-0201_start.

Run: python3 -m unittest discover -s .claude/skills/papo-qa/scripts/tests -v
"""

import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import papo_qa as qa
import ranges

COLOR = "\n\tif value == \"\":\n\t\tvalue = \"#C0C0C0\"\n\telse:\n\t\tif {test}:\n\t\t\tvalue = \"#000000\"\n\t\telse:\n\t\t\tvalue = \"#F70808\"\n\treturn value"


def _field(custom, test, prefix=""):
	code = prefix + COLOR.format(test=test)
	return {"type": "ia.input.numeric-entry-field", "custom": custom,
		"propConfig": {"custom.color": {"binding": {"type": "property", "config": {"path": "this.props.value"},
			"transforms": [{"type": "script", "code": code}]}}}}


class RangesTest(unittest.TestCase):
	def test_lowHigh(self):
		field = _field({"rang_down": 1280, "rang_up": 1305}, "minimo <= value <= maximo", "\n\tminimo = self.custom.rang_down\n\tmaximo = self.custom.rang_up")
		self.assertEqual(ranges.rangeOf(field), (1280, 1305))

	def test_startPlusMinus(self):
		field = _field({"start": 12.5, "rang": 0.1}, "minimo <= value <= maximo", "\n\tminimo = self.custom.start - self.custom.rang\n\tmaximo = self.custom.start + self.custom.rang")
		self.assertEqual(ranges.rangeOf(field), (12.4, 12.6))
		self.assertTrue(ranges.isRed(field, 7))
		self.assertFalse(ranges.isRed(field, 12.5))

	def test_lowerBoundOnlyStaysNative(self):
		# Valid when value >= 12.75: no closed range paints the same
		field = _field({"rang_down": 0, "rang_up": 12.75}, "value >= maximo", "\n\tmaximo = self.custom.rang_up")
		self.assertEqual(ranges.rangeOf(field), ranges.UNSUPPORTED)

	def test_noColorLogic(self):
		self.assertIsNone(ranges.rangeOf({"type": "ia.input.numeric-entry-field", "custom": {"rang_down": 1, "rang_up": 2}}))

	def test_qaCatchesWrongRange(self):
		field = _field({"rang_down": 0, "rang_up": 12.75}, "value >= maximo", "\n\tmaximo = self.custom.rang_up")
		node = {"props": {"path": "Objects/NumericField", "params": {"minValue": 0, "maxValue": 12.75}}}
		self.assertTrue(qa._rangeProblems({"node": field}, node, 5848))
		node["props"]["params"].update(minValue=None, maxValue=None)
		self.assertTrue(qa._rangeProblems({"node": field}, node, 5848))


if __name__ == "__main__":
	unittest.main()
