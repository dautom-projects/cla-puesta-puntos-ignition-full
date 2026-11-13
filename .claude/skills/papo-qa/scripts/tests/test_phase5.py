"""
Tests of the phase 5 conversions of papo_objects v2.12: a field the view only reads in bindings, an option group
answered by a chain of if() and a checkbox that answers its own Sí / No text. Each case converts a real view as
it was before phase 5 (commit d87d8ad) and checks the object, the redirected bindings and stage 3 of the QA.

Run: python3 -m unittest discover -s .claude/skills/papo-qa/scripts/tests -v
"""

import collections
import json
import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "papo-design", "scripts"))
import papo_qa as qa
import papo_objects as po
import view_refs

BEFORE = "d87d8ad"
VIEWS = "cla-project/com.inductiveautomation.perspective/views/Page/Embedded/"
OPTIONS = {"rows": True, "repeaters": True, "legacy": True, "formClass": True, "staticIDs": True}


def _convert(view):
	"""(view at BEFORE, converted copy, stats)."""
	text = subprocess.run(["git", "-C", qa.REPO, "show", "{}:{}{}/view.json".format(BEFORE, VIEWS, view)], capture_output=True, text=True).stdout
	before, after = json.loads(text), json.loads(text)
	stats = collections.Counter()
	po.standardize(after, dict(OPTIONS), stats)
	return before, after, stats


def _node(view, path):
	node = view["root"]
	for name in path.split("/"):
		node = next(c for c in node["children"] if c["meta"]["name"] == name)
	return node


class Phase5Test(unittest.TestCase):
	def test_valueReadRedirected(self):
		before, after, stats = _convert("OREC/Form_EC07-0101_barcada")
		read = _node(after, "FlexContainerGroup1/FlexContainer19/NumericEntryField_0")
		self.assertEqual(read["props"]["path"], "Objects/NumericField")
		reader = _node(after, "FlexContainerGroup1/FlexContainer17/NumericEntryField_0")
		expression = reader["propConfig"]["props.params.value"]["binding"]["config"]["expression"]
		self.assertIn("{.../FlexContainer19/NumericEntryField_0.props.params.value}", expression)
		self.assertNotIn("NumericEntryField_0.props.value}", expression)
		self.assertFalse(view_refs.broken(after) - view_refs.broken(before))
		self.assertEqual([qa._key(s) for s in qa.answerSources(before)], [qa._key(s) for s in qa.answerSources(after)])
		self.assertEqual(stats["campos leídos por otros convertidos"], 4)

	def test_scriptReadStaysNative(self):
		# +/- labels change the value from a script: the field keeps its native component
		_, after, _ = _convert("F&A/Form_TE11-0401_defects")
		self.assertEqual(_node(after, "FlexContainerGroup1/S4/FlexContainer_0/NumericEntryField")["type"], "ia.input.numeric-entry-field")

	def test_optionChain(self):
		before, after, _ = _convert("General/Form_PL11-0101-CA_start")
		group = _node(after, "FlexContainerGroup3/FlexContainer3/FlexContainer_0")
		params = group["props"]["params"]
		self.assertEqual(group["props"]["path"], "Objects/OptionGroup")
		self.assertEqual(params["options"], ["LN", "GN", "CN", "ZN"])
		self.assertEqual(params["emptyAnswer"], "")
		# 9176 is a fixed short text (docs/sql/preguntas_texto_fijo.json): the question stays written
		self.assertEqual(params["question"], "CAV1")
		self.assertEqual(qa.stageAnswers(after, {"view": before}), ([], 2))

	def test_checkboxTextAnswer(self):
		before, after, _ = _convert("OREC/Form_MZ07-0101_start")
		box = _node(after, "FlexContainerGroup1/FlexContainer_2/FlexContainer_3/Checkbox")
		params = box["props"]["params"]
		self.assertEqual((params["trueValue"], params["falseValue"]), ("Sí", "No"))
		self.assertEqual((params["trueText"], params["falseText"]), ("Sí", "No"))
		self.assertEqual(params["answer"], "Sí")
		self.assertEqual(qa.stageAnswers(after, {"view": before}), ([], 2))

	def test_rangeByOtherFields(self):
		# EA11-2501_2h: the bounds depend on the battery size checkboxes; inputBounds 0-100 is carried
		before, after, stats = _convert("Ensamble/Form_EA11-2501_2h")
		field = _node(after, "FlexContainerGroup5/FlexContainer_20/FlexContainer_5/NumericEntryField")
		self.assertEqual(field["props"]["path"], "Objects/NumericField")
		self.assertEqual(field["props"]["params"]["inputBounds"], {"maximum": 100, "minimum": 0})
		struct = field["propConfig"]["props.params.maxValue"]["binding"]["config"]["struct"]
		self.assertEqual(sorted(struct), ["isLarge", "isMedium"])
		self.assertEqual(stats["numéricos con rango según otro campo"], 16)
		self.assertFalse(view_refs.broken(after) - view_refs.broken(before))
		problems, checked = qa.stageAnswers(after, {"view": before})
		self.assertEqual(problems, [])
		self.assertEqual(qa.stageFieldProps(after, {"view": before}), [])

	def test_qaCatchesWrongDynamicBound(self):
		before, after, _ = _convert("Ensamble/Form_EA11-2501_2h")
		field = _node(after, "FlexContainerGroup5/FlexContainer_0/FlexContainer_5/NumericEntryField")
		binding = field["propConfig"]["props.params.maxValue"]["binding"]
		binding["transforms"][0]["code"] = binding["transforms"][0]["code"].replace("maxValue = 3", "maxValue = 4")
		problems, _ = qa.stageAnswers(after, {"view": before})
		self.assertTrue(any("rango" in p for p in problems))


if __name__ == "__main__":
	unittest.main()
