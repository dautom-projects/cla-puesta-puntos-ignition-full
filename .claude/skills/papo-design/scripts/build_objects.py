"""
Builds the PAPO standard objects (views/Objects/*/view.json) from one definition.

Edit this file and run it to change every object at once; forms only pass parameters.
Contract (all objects): question, papoItemID, fontSize (input) · value (inout) · answer (output).
List layout: showQuestion, questionBasis. See .claude/docs/OBJETOS_ESTANDAR.md.

Version: 2.1.0

Changelog:
	2026-10-24 | William M. | v2.0.0 - value inout, answer output, options/answerFrom (Dropdown)
	2026-10-25 | William M. | v2.1.0 - emptyAnswer; Objects/OptionGroup and Objects/DateTime

Args (CLI):
	--check: Only report which objects would change

Returns:
	Exit code 0
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import papo_design as design

OBJECTS_DIR = os.path.join(design.VIEWS_DIR, "Objects")

# Answer of value fields: the value; when emptyAnswer is set, emptyAnswer for an empty value
# (same rule as the forms' transform: return value if value else "-")
ANSWER_VALUE = (
	"\t# Answer is the value, or emptyAnswer when the value is empty and emptyAnswer is set\n"
	"\tif value[\"emptyAnswer\"] is None:\n"
	"\t\treturn value[\"value\"]\n"
	"\treturn value[\"value\"] if value[\"value\"] else value[\"emptyAnswer\"]\n")

# Answer of a dropdown: label of the selected option (what most forms save) or its value
ANSWER_DROPDOWN = (
	"\t# Answer is the selected option label, or its value when answerFrom is \"value\"\n"
	"\tif value[\"answerFrom\"] == \"value\":\n"
	"\t\tif value[\"emptyAnswer\"] is None:\n"
	"\t\t\treturn value[\"value\"]\n"
	"\t\treturn value[\"value\"] if value[\"value\"] else value[\"emptyAnswer\"]\n"
	"\tfor option in value[\"options\"] or []:\n"
	"\t\tif str(option[\"value\"]) == str(value[\"value\"]):\n"
	"\t\t\treturn option[\"label\"]\n"
	"\treturn \"\"\n")

# Answer of a time field: the selected time as text (same logic the forms used)
ANSWER_DATETIME = (
	"\t# Answer is the selected time formatted as text; None when there is no value\n"
	"\tfrom java.text import SimpleDateFormat\n"
	"\tfrom java.util import Locale\n"
	"\ttry:\n"
	"\t\tif value[\"value\"] is None:\n"
	"\t\t\treturn None\n"
	"\t\treturn SimpleDateFormat(value[\"format\"], Locale.ENGLISH).format(value[\"value\"])\n"
	"\texcept:\n"
	"\t\treturn None\n")

QUESTION_TEXT = "\treturn value[\"question\"] or papo_core.items.getQuestionText(value)"


def prop(path, bidirectional=False):
	config = {"path": path}
	if bidirectional:
		config["bidirectional"] = True
	return {"binding": {"config": config, "type": "property"}}


def expr(expression):
	return {"binding": {"config": {"expression": expression}, "type": "expr"}}


def struct(fields, code):
	return {"binding": {"config": {"struct": {k: "{view.params.%s}" % k for k in fields}, "waitOnAll": True},
		"transforms": [{"code": code, "type": "script"}], "type": "expr-struct"}}


def questionText():
	return {"binding": {"config": {"struct": {"dbConnection": "{view.custom.dbConnection}",
		"papoItemID": "{view.params.papoItemID}", "question": "{view.params.question}"}, "waitOnAll": True},
		"transforms": [{"code": QUESTION_TEXT, "type": "script"}], "type": "expr-struct"}}


def view(params, directions, answer, children):
	propConfig = {"custom.dbConnection": dict(prop("session.custom.dbConnection"), persistent=True)}
	for name, direction in directions.items():
		propConfig["params." + name] = {"paramDirection": direction, "persistent": True}
	propConfig["params.answer"] = dict(answer, paramDirection="output", persistent=True)
	return {"custom": {"dbConnection": "papo_db"}, "params": params, "propConfig": propConfig,
		"props": {"defaultSize": {"height": 50, "width": 400}},
		"root": {"children": children, "meta": {"name": "root"},
			"props": {"alignItems": "stretch", "style": {"overflow": "hidden"}}, "type": "ia.container.flex"}}


def questionLabel():
	return {"meta": {"name": "Question"}, "position": {"shrink": 0},
		"propConfig": {"position.basis": prop("view.params.questionBasis"), "position.display": prop("view.params.showQuestion"),
			"props.text": questionText(), "props.textStyle.fontSize": prop("view.params.fontSize")},
		"type": "ia.display.label"}


def field(ctype, propConfig, props):
	return {"meta": {"name": "Field"}, "position": {"basis": "0px", "grow": 1}, "propConfig": propConfig,
		"props": props, "type": ctype}


def rangeColor(kind):
	return struct(("maxValue", "minValue", "value"),
		"\treturn papo_core.items.getRangeColor(value[\"value\"], value[\"minValue\"], value[\"maxValue\"], \"%s\")" % kind)


COMMON = {"question": "", "papoItemID": None, "fontSize": 17}
COMMON_DIR = {"question": "input", "papoItemID": "input", "fontSize": "input"}
LIST = {"showQuestion": True, "questionBasis": "60%"}
LIST_DIR = {"showQuestion": "input", "questionBasis": "input"}
FONT = prop("view.params.fontSize")


def definitions():
	"""Return {object name: view} for every standard object."""
	return {
		# The question is the checkbox text; answer = trueValue / falseValue
		"Checkbox": view(dict(COMMON, trueValue="Cumple", falseValue="No Cumple", value=False, answer="No Cumple"),
			dict(COMMON_DIR, trueValue="input", falseValue="input", value="inout"),
			expr("if({view.params.value}, {view.params.trueValue}, {view.params.falseValue})"),
			[field("ia.input.checkbox", {"props.selected": prop("view.params.value", True), "props.text": questionText(),
				"props.style.fontSize": FONT}, {"style": {"classes": "PAPO/Field/Checkbox"}})]),
		"NumericField": view(dict(COMMON, minValue=None, maxValue=None, placeholder="Escriba aqui", emptyAnswer=None,
				value=None, answer=None, **LIST),
			dict(COMMON_DIR, minValue="input", maxValue="input", placeholder="input", emptyAnswer="input", value="inout", **LIST_DIR),
			struct(("emptyAnswer", "value"), ANSWER_VALUE),
			[questionLabel(), field("ia.input.numeric-entry-field", {"props.value": prop("view.params.value", True),
				"props.placeholder": prop("view.params.placeholder"), "props.style.color": rangeColor("text"),
				"props.style.borderColor": rangeColor("border"), "props.style.fontSize": FONT},
				{"align": "left", "format": "none", "spinner": {"enabled": False}, "style": {"classes": "PAPO/Field/Input"}})]),
		"TextField": view(dict(COMMON, placeholder="Escriba aqui", emptyAnswer=None, value="", answer="", **LIST),
			dict(COMMON_DIR, placeholder="input", emptyAnswer="input", value="inout", **LIST_DIR),
			struct(("emptyAnswer", "value"), ANSWER_VALUE),
			[questionLabel(), field("ia.input.text-field", {"props.text": prop("view.params.value", True),
				"props.placeholder": prop("view.params.placeholder"), "props.style.fontSize": FONT},
				{"style": {"classes": "PAPO/Field/Input"}})]),
		"Dropdown": view(dict(COMMON, options=[], answerFrom="label", placeholder="Seleccione", emptyAnswer=None,
				value=None, answer="", **LIST),
			dict(COMMON_DIR, options="input", answerFrom="input", placeholder="input", emptyAnswer="input", value="inout", **LIST_DIR),
			struct(("answerFrom", "emptyAnswer", "options", "value"), ANSWER_DROPDOWN),
			[questionLabel(), field("ia.input.dropdown", {"props.value": prop("view.params.value", True),
				"props.options": prop("view.params.options"), "props.placeholder.text": prop("view.params.placeholder"),
				"props.style.fontSize": FONT}, {"placeholder": {}, "style": {"classes": "PAPO/Field/Dropdown"}})]),
		# One choice among options (list of texts); answer = the chosen text, or emptyAnswer
		"OptionGroup": view(dict(COMMON, options=[], emptyAnswer="-", value=None, answer="-", **LIST),
			dict(COMMON_DIR, options="input", emptyAnswer="input", value="inout", **LIST_DIR),
			struct(("emptyAnswer", "value"), ANSWER_VALUE),
			[questionLabel(), field("ia.input.radio-group", {"props.value": prop("view.params.value", True),
				"props.radios": {"binding": {"config": {"path": "view.params.options"},
					"transforms": [{"code": "\treturn [{\"text\": option, \"value\": option} for option in value or []]", "type": "script"}],
					"type": "property"}},
				"props.style.fontSize": FONT}, {"layout": "row", "style": {"classes": "PAPO/Field/Checkbox"}})]),
		# Date or time picker; answer = the value formatted with format (default: time as text)
		"DateTime": view(dict(COMMON, pickerType="time", format="h:mm:ss a", value=None, answer=None, **LIST),
			dict(COMMON_DIR, pickerType="input", format="input", value="inout", **LIST_DIR),
			struct(("format", "value"), ANSWER_DATETIME),
			[questionLabel(), field("ia.input.date-time-input", {"props.value": prop("view.params.value", True),
				"props.pickerType": prop("view.params.pickerType"), "props.style.fontSize": FONT},
				{"style": {"classes": "PAPO/Field/Input"}})]),
		# Read-only tag value; answer = the value read from tagPath
		"Label": view(dict(COMMON, tagPath="", answer=None, **LIST), dict(COMMON_DIR, tagPath="input", **LIST_DIR),
			expr("{/root/Field.props.text}"),
			[questionLabel(), field("ia.display.label", {"props.text": {"binding": {"config": {"fallbackDelay": 2.5,
				"mode": "indirect", "references": {"1": "{view.params.tagPath}"}, "tagPath": "{1}"}, "type": "tag"}},
				"props.textStyle.fontSize": FONT}, {"style": {"classes": "PAPO/Field/TagValue"}})]),
	}


RESOURCE = ('{\n  "scope": "G",\n  "version": 1,\n  "restricted": false,\n  "overridable": true,\n'
	'  "files": [\n    "view.json"\n  ],\n  "attributes": {\n    "lastModification": {\n'
	'      "actor": "external",\n      "timestamp": "2026-10-25T00:00:00Z"\n    }\n  }\n}')


def main():
	parser = argparse.ArgumentParser(description="Genera los objetos estándar PAPO")
	parser.add_argument("--check", action="store_true")
	args = parser.parse_args()
	for name, obj in sorted(definitions().items()):
		folder = os.path.join(OBJECTS_DIR, name)
		path = os.path.join(folder, "view.json")
		new = design.gsonDump(obj)
		old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
		status = "igual" if old == new else ("nuevo" if old is None else "cambia")
		print("{:<12} {}".format(name, status))
		if args.check or status == "igual":
			continue
		os.makedirs(folder, exist_ok=True)
		open(path, "w", encoding="utf-8").write(new)
		if not os.path.exists(os.path.join(folder, "resource.json")):
			open(os.path.join(folder, "resource.json"), "w", encoding="utf-8").write(RESOURCE)
	return 0


if __name__ == "__main__":
	sys.exit(main())
