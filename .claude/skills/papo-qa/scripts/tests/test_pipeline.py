"""
Tests of the PAPO QA pipeline: a clean copy of the pilot must pass and one seeded error per
stage must fail. Uses the pilot at HEAD and its original copy at commit bd2dd43.

Run: python3 -m unittest discover -s .claude/skills/papo-qa/scripts/tests -v
"""

import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import papo_qa as qa

PILOT = "cla-project/com.inductiveautomation.perspective/views/Page/Embedded/Ensamble/Form_EA11-0901_1h_PruebaPiloto/view.json"
ORIGINAL_COMMIT = "bd2dd43"


def _git(ref, path):
	return subprocess.run(["git", "-C", qa.REPO, "show", "{}:{}".format(ref, path)], capture_output=True, text=True).stdout


def _embeds(view):
	out = []

	def walk(n):
		if n.get("type") == "ia.display.view":
			out.append(n)
		for c in n.get("children", []):
			walk(c)
	walk(view["root"])
	return out


class PipelineTest(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.base = {"view": json.loads(_git(ORIGINAL_COMMIT, PILOT)), "crlf": False}
		pilot = json.loads(_git("HEAD", PILOT))
		# Clean copy: the two known pending issues fixed (default answer of 11408, legacy handler)
		for n in _embeds(pilot):
			if n["custom"]["item"]["papoItemID"] == 11408:
				n["props"]["params"]["answer"] = None
				n["props"]["params"]["value"] = None

		def dropLegacy(n):
			scripts = n.get("scripts") or {}
			if n.get("meta", {}).get("name") != "root" and scripts.get("messageHandlers"):
				scripts["messageHandlers"] = []
			for c in n.get("children", []):
				dropLegacy(c)
		dropLegacy(pilot["root"])
		cls.clean = pilot

	def run_case(self, view, raw=None):
		folder = tempfile.mkdtemp(prefix="papo-qa-test-")
		path = os.path.join(folder, "Form_Test", "view.json")
		os.makedirs(os.path.dirname(path))
		open(path, "w", encoding="utf-8").write(raw if raw is not None else qa.design.gsonDump(view))
		results, _, _ = qa.checkView(path, self.base)
		return {stage for stage, problems in results.items() if problems}

	def test_clean_copy_passes(self):
		self.assertEqual(self.run_case(self.clean), set())

	def test_structure_non_canonical(self):
		self.assertIn("1", self.run_case(None, raw=json.dumps(self.clean, indent=4)))

	def test_collection_changed_item(self):
		v = copy.deepcopy(self.clean)
		_embeds(v)[0]["custom"]["item"]["papoItemID"] = 999999
		self.assertIn("2", self.run_case(v))

	def test_collection_swapped_order(self):
		v = copy.deepcopy(self.clean)
		group = v["root"]["children"][2]
		group["children"][1], group["children"][4] = group["children"][4], group["children"][1]
		self.assertIn("2", self.run_case(v))

	def test_answers_wrong_false_value(self):
		v = copy.deepcopy(self.clean)
		box = [n for n in _embeds(v) if n["props"]["path"] == "Objects/Checkbox"][0]
		box["props"]["params"]["falseValue"] = "No cumple"
		self.assertIn("3", self.run_case(v))

	def test_flow_missing_wrapper(self):
		v = copy.deepcopy(self.clean)
		v["root"]["scripts"]["customMethods"] = [m for m in v["root"]["scripts"]["customMethods"] if m["name"] != "answerRecopile"]
		self.assertIn("4", self.run_case(v))

	def test_flow_new_hardcoded_db(self):
		v = copy.deepcopy(self.clean)
		v["root"]["scripts"]["messageHandlers"][0]["script"] += '\n\tdb = "papo_db"'
		self.assertIn("4", self.run_case(v))

	def test_design_without_form_class(self):
		v = copy.deepcopy(self.clean)
		v["root"]["props"]["style"]["classes"] = "container-borders-dautom-widget"
		self.assertIn("5", self.run_case(v))

	def test_design_fixed_width(self):
		v = copy.deepcopy(self.clean)
		_embeds(v)[0]["props"].setdefault("style", {})["width"] = "250px"
		self.assertIn("5", self.run_case(v))

	def test_collection_broken_reference(self):
		v = copy.deepcopy(self.clean)
		_embeds(v)[0]["propConfig"]["props.params.fontSize"] = {"binding": {"config": {"path": "../NoExiste.props.value"}, "type": "property"}}
		self.assertIn("2", self.run_case(v))

	def test_contract_unknown_param(self):
		v = copy.deepcopy(self.clean)
		_embeds(v)[0]["props"]["params"]["foo"] = 1
		self.assertIn("6", self.run_case(v))

	def test_contract_answer_not_bound(self):
		v = copy.deepcopy(self.clean)
		_embeds(v)[0]["propConfig"]["custom.item.answer"]["binding"]["config"]["path"] = "this.props.params.value"
		self.assertIn("6", self.run_case(v))


if __name__ == "__main__":
	unittest.main()
