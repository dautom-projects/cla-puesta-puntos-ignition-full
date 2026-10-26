"""
Builds the PAPO standard objects (views/Objects/*/view.json) from one definition.

Edit this file and run it to change every object at once; forms only pass parameters.
Contract (all objects): question, papoItemID, fontSize (input) · value (inout) · answer (output).
Inputs also take enabled. List layout: showQuestion, questionBasis. See .claude/docs/OBJETOS_ESTANDAR.md.

Version: 2.5.0

Changelog:
	2026-10-24 | William M. | v2.0.0 - value inout, answer output, options/answerFrom (Dropdown)
	2026-10-25 | William M. | v2.1.0 - emptyAnswer; Objects/OptionGroup and Objects/DateTime
	2026-10-25 | William M. | v2.2.0 - enabled; question resolved once in view.custom.question; Checkbox
		trueText/falseText; questionAsPlaceholder; Dropdown showClearIcon and "Seleccionar";
		OptionGroup in one row (orientation, align, radioStyle)
	2026-10-25 | William M. | v2.3.0 - Root with position relative: the hidden input of checkboxes and radios
		stays inside the object (clicking one no longer scrolls the page away in long sections)
	2026-10-25 | William M. | v2.4.0 - OptionGroup radios carry selected from value: the radio inputs are always
		controlled (the first option could stay checked in the browser and ignore the first click)
	2026-10-26 | William M. | v2.5.0 - DateTime startNow: without a value it starts with the time the form opens,
		like the native date-time input (also when the form pushes the empty value after the object started)

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
QUESTION = "{view.custom.question}"
# DateTime with startNow: the native date-time input of the forms shows the time the form opens
START_NOW = {"system": {"onStartup": {"config": {"script": "\t# A time field starts with the time the form opens, like the native date-time input\n"
	"\tif self.params.startNow and self.params.value is None:\n\t\tself.params.value = system.date.now()"}, "scope": "G", "type": "script"}}}
# The form can push its empty value after the object started: the field keeps a time, as the native one does
KEEP_TIME = ("\t# The form can push its empty value after the object started: keep the opening time\n"
	"\tif currentValue.value is None and self.params.startNow:\n\t\tself.params.value = system.date.now()")
# Radios of an option group: every radio says whether it is the value (a radio without "selected" leaves
# its <input> uncontrolled and the browser can keep a stale check that swallows the first click)
RADIOS = "\treturn [{\"text\": option, \"value\": option, \"selected\": option == value[\"value\"]} for option in value[\"options\"] or []]"
# Checkbox text: the state text when trueText/falseText are set (e.g. ✔ / ✘), otherwise the question
CHECKBOX_TEXT = ("if(coalesce({view.params.trueText}, \"\") + coalesce({view.params.falseText}, \"\") != \"\", "
	"if({view.params.value}, {view.params.trueText}, {view.params.falseText}), {view.custom.question})")
# Input placeholder: the question when questionAsPlaceholder is set, otherwise the placeholder text
PLACEHOLDER = "if({view.params.questionAsPlaceholder}, {view.custom.question}, {view.params.placeholder})"


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


def view(params, directions, answer, children, events=None, onChange=None):
	propConfig = {"custom.dbConnection": dict(prop("session.custom.dbConnection"), persistent=True),
		"custom.question": dict(questionText(), persistent=True)}
	for name, direction in directions.items():
		propConfig["params." + name] = {"paramDirection": direction, "persistent": True}
	for name, script in (onChange or {}).items():
		propConfig["params." + name]["onChange"] = {"enabled": None, "script": script}
	propConfig["params.answer"] = dict(answer, paramDirection="output", persistent=True)
	extra = {"events": events} if events else {}
	return dict(extra, **{"custom": {"dbConnection": "papo_db", "question": ""}, "params": params, "propConfig": propConfig,
		"props": {"defaultSize": {"height": 50, "width": 400}},
		# position relative: containing block of the absolute hidden <input> of checkboxes and radios
		"root": {"children": children, "meta": {"name": "root"},
			"props": {"alignItems": "stretch", "style": {"overflow": "hidden", "position": "relative"}}, "type": "ia.container.flex"}})


def questionLabel():
	return {"meta": {"name": "Question"}, "position": {"shrink": 0},
		"propConfig": {"position.basis": prop("view.params.questionBasis"), "position.display": prop("view.params.showQuestion"),
			"props.text": expr(QUESTION), "props.textStyle.fontSize": prop("view.params.fontSize")},
		"type": "ia.display.label"}


def field(ctype, propConfig, props, position=None, enabled=True):
	if enabled:
		propConfig = dict(propConfig, **{"props.enabled": prop("view.params.enabled")})
	return {"meta": {"name": "Field"}, "position": position or {"basis": "0px", "grow": 1}, "propConfig": propConfig,
		"props": props, "type": ctype}


def rangeColor(kind):
	return struct(("maxValue", "minValue", "value"),
		"\treturn papo_core.items.getRangeColor(value[\"value\"], value[\"minValue\"], value[\"maxValue\"], \"%s\")" % kind)


COMMON = {"question": "", "papoItemID": None, "fontSize": 17, "enabled": True}
COMMON_DIR = {"question": "input", "papoItemID": "input", "fontSize": "input", "enabled": "input"}
COMMON_LABEL = {k: v for k, v in COMMON.items() if k != "enabled"}
COMMON_LABEL_DIR = {k: v for k, v in COMMON_DIR.items() if k != "enabled"}
INPUT_TEXT = {"placeholder": "Escriba aqui", "questionAsPlaceholder": False}
INPUT_TEXT_DIR = {"placeholder": "input", "questionAsPlaceholder": "input"}
# Icon color of a disabled checkbox (the forms used the brand blue)
DISABLED_ICON = {"color": {"disabled": "#1199C7"}}
LIST = {"showQuestion": True, "questionBasis": "60%"}
LIST_DIR = {"showQuestion": "input", "questionBasis": "input"}
FONT = prop("view.params.fontSize")


def definitions():
	"""Return {object name: view} for every standard object."""
	return {
		# The question is the checkbox text (or the state text); answer = trueValue / falseValue
		"Checkbox": view(dict(COMMON, trueValue="Cumple", falseValue="No Cumple", trueText="", falseText="", value=False,
				answer="No Cumple"),
			dict(COMMON_DIR, trueValue="input", falseValue="input", trueText="input", falseText="input", value="inout"),
			expr("if({view.params.value}, {view.params.trueValue}, {view.params.falseValue})"),
			[field("ia.input.checkbox", {"props.selected": prop("view.params.value", True), "props.text": expr(CHECKBOX_TEXT),
				"props.style.fontSize": FONT}, {"checkedIcon": DISABLED_ICON, "style": {"classes": "PAPO/Field/Checkbox"},
				"uncheckedIcon": DISABLED_ICON})]),
		"NumericField": view(dict(COMMON, minValue=None, maxValue=None, emptyAnswer=None, value=None, answer=None,
				**dict(INPUT_TEXT, **LIST)),
			dict(COMMON_DIR, minValue="input", maxValue="input", emptyAnswer="input", value="inout", **dict(INPUT_TEXT_DIR, **LIST_DIR)),
			struct(("emptyAnswer", "value"), ANSWER_VALUE),
			[questionLabel(), field("ia.input.numeric-entry-field", {"props.value": prop("view.params.value", True),
				"props.placeholder": expr(PLACEHOLDER), "props.style.color": rangeColor("text"),
				"props.style.borderColor": rangeColor("border"), "props.style.fontSize": FONT},
				{"align": "left", "format": "none", "spinner": {"enabled": False}, "style": {"classes": "PAPO/Field/Input"}})]),
		"TextField": view(dict(COMMON, emptyAnswer=None, value="", answer="", **dict(INPUT_TEXT, **LIST)),
			dict(COMMON_DIR, emptyAnswer="input", value="inout", **dict(INPUT_TEXT_DIR, **LIST_DIR)),
			struct(("emptyAnswer", "value"), ANSWER_VALUE),
			[questionLabel(), field("ia.input.text-field", {"props.text": prop("view.params.value", True),
				"props.placeholder": expr(PLACEHOLDER), "props.style.fontSize": FONT},
				{"style": {"classes": "PAPO/Field/Input"}})]),
		"Dropdown": view(dict(COMMON, options=[], answerFrom="label", placeholder="Seleccionar", showClearIcon=False,
				emptyAnswer=None, value=None, answer="", **LIST),
			dict(COMMON_DIR, options="input", answerFrom="input", placeholder="input", showClearIcon="input",
				emptyAnswer="input", value="inout", **LIST_DIR),
			struct(("answerFrom", "emptyAnswer", "options", "value"), ANSWER_DROPDOWN),
			[questionLabel(), field("ia.input.dropdown", {"props.value": prop("view.params.value", True),
				"props.options": prop("view.params.options"), "props.placeholder.text": prop("view.params.placeholder"),
				"props.showClearIcon": prop("view.params.showClearIcon"), "props.style.fontSize": FONT},
				{"placeholder": {}, "style": {"classes": "PAPO/Field/Dropdown"}})]),
		# One choice among options (list of texts) in one row; answer = the chosen text, or emptyAnswer
		"OptionGroup": view(dict(COMMON, options=[], emptyAnswer="-", value=None, answer="-", **LIST),
			dict(COMMON_DIR, options="input", emptyAnswer="input", value="inout", **LIST_DIR),
			struct(("emptyAnswer", "value"), ANSWER_VALUE),
			[questionLabel(), field("ia.input.radio-group", {"props.value": prop("view.params.value", True),
				"props.radios": struct(("options", "value"), RADIOS),
				"props.style.fontSize": FONT}, {"align": "center", "orientation": "row",
				"radioStyle": {"paddingBottom": 0, "paddingLeft": 0, "paddingRight": 24, "paddingTop": 0},
				"style": {"classes": "PAPO/Field/Checkbox"}, "textPosition": "right"},
				position={"basis": "auto", "grow": 1, "shrink": 0})]),
		# Date or time picker; answer = the value formatted with format (default: time as text)
		"DateTime": view(dict(COMMON, pickerType="time", format="h:mm:ss a", startNow=False, value=None, answer=None, **LIST),
			dict(COMMON_DIR, pickerType="input", format="input", startNow="input", value="inout", **LIST_DIR),
			struct(("format", "value"), ANSWER_DATETIME),
			[questionLabel(), field("ia.input.date-time-input", {"props.value": prop("view.params.value", True),
				"props.pickerType": prop("view.params.pickerType"), "props.style.fontSize": FONT},
				{"style": {"classes": "PAPO/Field/Input"}})], events=START_NOW, onChange={"value": KEEP_TIME}),
		# Read-only tag value; answer = the value read from tagPath
		"Label": view(dict(COMMON_LABEL, tagPath="", answer=None, **LIST), dict(COMMON_LABEL_DIR, tagPath="input", **LIST_DIR),
			expr("{/root/Field.props.text}"),
			[questionLabel(), field("ia.display.label", {"props.text": {"binding": {"config": {"fallbackDelay": 2.5,
				"mode": "indirect", "references": {"1": "{view.params.tagPath}"}, "tagPath": "{1}"}, "type": "tag"}},
				"props.textStyle.fontSize": FONT}, {"style": {"classes": "PAPO/Field/TagValue"}}, enabled=False)]),
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
