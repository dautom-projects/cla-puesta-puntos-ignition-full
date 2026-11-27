"""
Tests of the tablet-mode rules of papo_qa stage 5: the section headers and groups of the root do not shrink
(EA11-1201_start at 1280x800: "Parametros..." squashed to 4 px when the form was taller than the screen).

Run: python3 -m unittest discover -s .claude/skills/papo-qa/scripts/tests -v
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import papo_qa as qa


def _view(sectionPosition, groupPosition):
	return {"root": {"meta": {"name": "root"}, "props": {"style": {"classes": "PAPO/Form"}}, "children": [
		{"meta": {"name": "Section1"}, "type": "ia.display.label", "position": sectionPosition},
		{"meta": {"name": "FlexContainerGroup1"}, "type": "ia.container.flex", "position": groupPosition, "children": []},
		{"meta": {"name": "FlexContainerSupervisor"}, "type": "ia.container.flex", "position": {"basis": "50px"}, "children": []},
	]}}


class TabletRulesTest(unittest.TestCase):
	def test_sectionWithoutShrinkFails(self):
		view = _view({"basis": "40px"}, {"basis": "0px", "shrink": 0})
		problems = qa.stageDesign(view, {"view": view})
		self.assertTrue(any(p.startswith("Section1: sin shrink 0") for p in problems), problems)

	def test_groupWithoutShrinkFails(self):
		view = _view({"basis": "40px", "shrink": 0}, {"basis": "0px"})
		problems = qa.stageDesign(view, {"view": view})
		self.assertTrue(any(p.startswith("FlexContainerGroup1: sin shrink 0") for p in problems), problems)

	def test_shrinkZeroPasses(self):
		# The supervisor container is not a section: it keeps its own position
		view = _view({"basis": "40px", "shrink": 0}, {"basis": "0px", "shrink": 0})
		problems = qa.stageDesign(view, {"view": view})
		self.assertFalse([p for p in problems if "shrink" in p], problems)


if __name__ == "__main__":
	unittest.main()
