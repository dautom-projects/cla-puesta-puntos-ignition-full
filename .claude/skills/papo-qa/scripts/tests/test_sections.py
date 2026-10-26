"""
Tests of papo_objects.fitSections: an open section keeps its height and fits its rows. Cases taken from
F&A/Form_AC10-0201_30min (group that could shrink) and F&A/Form_AC10-0201_end (height below its rows).

Run: python3 -m unittest discover -s .claude/skills/papo-qa/scripts/tests -v
"""

import collections
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "papo-design", "scripts"))
import papo_objects as objects


def _view(base, rows, position=None, style=None):
	group = {"meta": {"name": "FlexContainerGroup1"}, "custom": {"baseBasisPx": base}, "type": "ia.container.flex",
		"position": position if position is not None else {"basis": "0px", "display": False, "shrink": 0},
		"props": {"direction": "column", "style": style or {}},
		"children": [{"meta": {"name": "Row{}".format(i)}, "type": "ia.container.flex", "position": {"basis": "{}px".format(h)},
			"props": {"style": {"marginTop": m}}} for i, (h, m) in enumerate(rows)]}
	return {"root": {"meta": {"name": "root"}, "children": [group]}}, group


class SectionsTest(unittest.TestCase):
	def test_heightReachesRows(self):
		view, group = _view(419, [(60, 0), (48, 0), (230, 0), (60, 0), (50, 0)])
		stats = collections.Counter()
		objects.fitSections(view, stats)
		self.assertEqual(group["custom"]["baseBasisPx"], 448)

	def test_marginsAndPadding(self):
		view, group = _view(100, [(40, 5), (40, 5)], style={"paddingTop": 10, "paddingBottom": 10})
		objects.fitSections(view, collections.Counter())
		self.assertEqual(group["custom"]["baseBasisPx"], 110)

	def test_groupDoesNotShrink(self):
		view, group = _view(2615, [(50, 0)] * 10, position={"basis": "0px", "display": False})
		stats = collections.Counter()
		objects.fitSections(view, stats)
		self.assertEqual(group["position"]["shrink"], 0)
		self.assertEqual(group["custom"]["baseBasisPx"], 2615)

	def test_alreadyFits(self):
		view, group = _view(500, [(50, 0)] * 4)
		stats = collections.Counter()
		objects.fitSections(view, stats)
		self.assertFalse(stats)


if __name__ == "__main__":
	unittest.main()
