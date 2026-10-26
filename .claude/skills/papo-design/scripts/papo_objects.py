"""
Converts PAPO Form views to the standard: fields as embedded standard objects (Objects/*).

The custom.item of every field stays on a component of the form inside the same
FlexContainerGroupN / FlexContainerSupervisor; its answer reads the object's output param
"answer", so papo_core.register.recopile collects the same items in the same order.

Modes (per row of a group):
	row       a list row of a column group (container + question label + one field, or a field
	          that is the row) becomes one object with the question inside (showQuestion true)
	field     in grids and row groups (FlexContainerSupervisor), only the field is replaced and
	          the cell keeps its layout
Every prop of the field is carried to the object: static values and bindings become params
(value, enabled, placeholder, options, the checkbox text...). A field with a prop the object
cannot take stays native.
	repeater  a Flex Repeater of Fundamental Views/Checkbox becomes one object per instance
Also: dead legacy save handlers are removed (--legacy) and the root gets PAPO/Form (--form-class).
A component is not replaced when something else in the view references it. Dry run by default.

Version: 2.2.0

Changelog:
	2026-10-24 | William M. | v1.0.0 - Initial version (EA11-0901_1h pilot)
	2026-10-25 | William M. | v2.0.0 - Row and repeater modes, emptyAnswer, checkbox fallback,
		option groups, date-time, legacy cleanup, PAPO/Form, reference safety
	2026-10-25 | William M. | v2.1.0 - Carry every field prop (checkbox text and state text, question as
		placeholder, enabled, value/option bindings) or keep the field native; rows only in column
		groups; a row without a question takes the full width
	2026-10-25 | William M. | v2.2.0 - Section height (custom.baseBasisPx) grows with the rows; an option
		group keeps the width of its question label

Args (CLI):
	--views (str...) / --all-forms: views to convert
	--apply: write (default: dry run)  --backup (str): backup folder
	--no-rows, --no-repeaters: disable those modes
	--legacy: remove dead legacy save handlers  --form-class: add PAPO/Form to the root

Returns:
	Exit code 0 when every view passed verification, 1 otherwise
"""

import argparse
import collections
import copy
import datetime
import glob
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "papo-qa", "scripts"))
import papo_design as design
import view_refs
import papo_qa as qa

OBJECTS = {
	"ia.input.checkbox": "Objects/Checkbox",
	"ia.input.numeric-entry-field": "Objects/NumericField",
	"ia.input.text-field": "Objects/TextField",
	"ia.input.dropdown": "Objects/Dropdown",
	"ia.input.date-time-input": "Objects/DateTime",
	"ia.container.flex": "Objects/OptionGroup",
}
VALUE_PROP = {
	"ia.input.checkbox": "this.props.selected",
	"ia.input.numeric-entry-field": "this.props.value",
	"ia.input.text-field": "this.props.text",
	"ia.input.dropdown": "this.props.value",
	"ia.input.date-time-input": "this.props.value",
}
DEFAULTS = {"Objects/NumericField": (None, None), "Objects/TextField": ("", "")}
GROUP = re.compile(r"^(FlexContainerGroup\d+|FlexContainerSupervisor)$")
RE_RANGE = re.compile(r"([\d.]+)\s*<=\s*value\s*<=\s*([\d.]+)")
DESCRIPTION_QUERY = "SELECT Description FROM papoitem WHERE ID = ?"
# Field props each object takes as a param (static value or binding)
FIELD_PARAMS = {
	"ia.input.checkbox": {"selected": "value", "enabled": "enabled"},
	"ia.input.numeric-entry-field": {"value": "value", "placeholder": "placeholder", "enabled": "enabled"},
	"ia.input.text-field": {"text": "value", "placeholder": "placeholder", "enabled": "enabled"},
	"ia.input.dropdown": {"value": "value", "options": "options", "placeholder": "placeholder", "enabled": "enabled",
		"showClearIcon": "showClearIcon"},
	"ia.input.date-time-input": {"value": "value", "pickerType": "pickerType", "enabled": "enabled"},
}
# Props the object sets itself (standard design or fixed behavior); the checkbox text is resolved apart
OBJECT_SETS = {
	"ia.input.checkbox": ("text", "checkedIcon", "uncheckedIcon", "direction"),
	"ia.input.numeric-entry-field": ("align", "format", "spinner", "containerStyle", "borderColor"),
	"ia.input.text-field": ("spellcheck",),
	"ia.input.dropdown": (),
	"ia.input.date-time-input": ("formattedValue",),
}
# Spellings of the default placeholder ("Escriba aqui") found in the forms
RE_DEFAULT_PLACEHOLDER = re.compile(r"^\s*esc?r?i?ba(\s+aqu[ií])?\s*$", re.I)
DROPDOWN_PLACEHOLDER = "Seleccionar"
REPEATER_VIEW = "Page/Embedded/Metalurgia/Fundamental Views/Checkbox"
ROW_BASIS = 50


def _prop(path):
	return {"binding": {"config": {"path": path}, "type": "property"}}


def _code(transform):
	return " ".join((transform.get("code") or "").split())


# ==================== WHAT CAN BE CONVERTED ====================

def answerRule(component):
	"""Return a dict describing how the field answers, or None when its logic is its own."""
	ctype = component.get("type")
	propConfig = component.get("propConfig", {})
	if _nestedItems(component):
		return None
	if ctype == "ia.container.flex":
		options = qa._optionTexts(component) if "checkboxAnswers" in component.get("custom", {}) else None
		return {"kind": "options", "options": options} if options else None
	binding = propConfig.get("custom.item.answer", {}).get("binding")
	if ctype not in VALUE_PROP or not binding or binding.get("type") != "property" or binding["config"].get("path") != VALUE_PROP[ctype]:
		return None
	transforms = binding.get("transforms", [])
	if ctype == "ia.input.date-time-input":
		ok = len(transforms) == 1 and 'SimpleDateFormat("h:mm:ss a"' in (transforms[0].get("code") or "")
		return {"kind": "time"} if ok else None
	if ctype == "ia.input.checkbox":
		if len(transforms) != 1 or transforms[0].get("type") != "map":
			return None
		table = {m.get("input"): m.get("output") for m in transforms[0].get("mappings", [])}
		if True not in table:
			return None
		falseValue = table[False] if False in table else transforms[0].get("fallback")
		return {"kind": "checkbox", "true": table[True], "false": falseValue}
	if not transforms:
		return {"kind": "value", "empty": None}
	if len(transforms) == 1 and transforms[0].get("type") == "script":
		code = _code(transforms[0])
		if code == qa.EMPTY_DASH:
			return {"kind": "value", "empty": "-"}
		if ctype == "ia.input.dropdown" and "self.props.options" in code and 'item["label"]' in code and 'str(item["value"]) == str(value)' in code:
			return {"kind": "label"}
	return None


def _nestedItems(component):
	"""True when another custom.item lives inside the component (recopile collects both)."""
	def walk(node):
		return any("item" in c.get("custom", {}) or walk(c) for c in node.get("children", []))
	return walk(component)


def _relative(binding):
	"""True when a binding config references components relative to its owner."""
	text = json.dumps((binding or {}).get("config", {}))
	return bool(re.search(r'"path": "(this|parent)\.|"path": "\.|\{(this|parent)\.|\{\.', text))


def _rangeOf(component):
	custom = component.get("custom", {})
	if "rang_down" in custom and "rang_up" in custom:
		return custom["rang_down"], custom["rang_up"]
	color = component.get("propConfig", {}).get("custom.color")
	if color:
		match = RE_RANGE.search(color["binding"]["transforms"][0].get("code") or "")
		if match:
			return tuple(float(x) if "." in x else int(x) for x in match.groups())
	return None


def objectParams(component, rule, stats, moved=False):
	"""Params and bindings of the object that replaces a field, or None when one of its props cannot be carried."""
	ctype = component["type"]
	props = component.get("props") or {}
	propConfig = component.get("propConfig", {})
	params, bindings = {}, {}
	kind = rule["kind"]
	if kind == "checkbox":
		selected = bool(props.get("selected", False))
		if selected:
			stats["valores iniciales conservados"] += 1
		params.update(trueValue=rule["true"], falseValue=rule["false"], value=selected, answer=rule["true"] if selected else rule["false"])
	elif kind == "options":
		answers = component["custom"].get("checkboxAnswers") or []
		chosen = [o for o, on in zip(rule["options"], answers) if on]
		params.update(options=rule["options"], emptyAnswer="-", value=chosen[0] if chosen else None,
			answer=chosen[0] if chosen else "-")
		return params, bindings
	elif kind == "time":
		value = props.get("value")
		params.update(pickerType=props.get("pickerType", "time"), format="h:mm:ss a", value=value, answer=qa._formatTime(value))
	elif ctype == "ia.input.dropdown":
		labelMode = kind == "label"
		value = props.get("value")
		if labelMode:
			answer = next((o.get("label") for o in props.get("options") or [] if str(o.get("value")) == str(value)), "")
		else:
			answer = value if rule.get("empty") is None else (value if value else rule["empty"])
		if value not in (None, ""):
			stats["valores iniciales conservados"] += 1
		params.update(value=value, answerFrom="label" if labelMode else "value", answer=answer)
		if rule.get("empty") is not None:
			params["emptyAnswer"] = rule["empty"]
		if "props.options" not in propConfig:
			params["options"] = props.get("options", [])
		stats["dropdown " + params["answerFrom"]] += 1
	else:
		valueProp = VALUE_PROP[ctype].split(".")[-1]
		value = props.get(valueProp, DEFAULTS[OBJECTS[ctype]][0])
		if value not in (None, ""):
			stats["valores iniciales conservados"] += 1
		params.update(value=value, answer=value if rule["empty"] is None else (value if value else rule["empty"]))
		if rule["empty"] is not None:
			params["emptyAnswer"] = rule["empty"]
		limits = _rangeOf(component) if ctype == "ia.input.numeric-entry-field" else None
		if limits:
			params.update(minValue=limits[0], maxValue=limits[1])
			stats["numéricos con rango"] += 1
	carried = carryProps(component, moved)
	if carried is None:
		return None
	params.update(carried[0])
	bindings.update(carried[1])
	return params, bindings


# ==================== FIELD PROPS ====================

def _itemID():
	return {"props.params.papoItemID": _prop("this.custom.item.papoItemID")}


def _rebase(binding, ctype):
	"""Binding with the field's own value prop pointed at the object's value param."""
	prop = VALUE_PROP[ctype].split(".")[-1]
	text = re.sub(r"\b(this|self)\.props\.{}\b".format(prop), lambda m: m.group(1) + ".props.params.value", json.dumps(binding))
	return json.loads(text)


def _portable(binding, moved):
	"""True when the binding resolves the same on the object (same place in the tree, or one level up when moved)."""
	text = json.dumps(binding)
	if re.search(r"\b(this|self)\.props\.(?!params\.)|\b(this|self)\.custom\.(?!item\b)|self\.(getChild|children)", text):
		return False
	return not moved or not re.search(r'"path": "(parent\.|\.)|\{(parent\.|\.)|self\.(parent|getSibling)', text)


def _describesItem(component, binding):
	"""True when the binding shows the description of the field's own papoItemID (papoitem query)."""
	transforms = (binding or {}).get("transforms", [])
	if not binding or binding.get("type") != "property" or len(transforms) != 1 or DESCRIPTION_QUERY not in _code(transforms[0]):
		return False
	path = binding.get("config", {}).get("path")
	if path == "this.custom.item.papoItemID":
		return True
	item = component.get("propConfig", {}).get("custom.item.papoItemID", {}).get("binding") or {}
	return bool(path) and item.get("type") == "property" and not item.get("transforms") and item.get("config", {}).get("path") == path


def _stateTexts(binding, ctype):
	"""(trueText, falseText) when the binding maps the checkbox state to two texts (e.g. ✔ / ✘)."""
	if not binding or binding.get("type") != "property" or binding.get("config") != {"path": VALUE_PROP[ctype]}:
		return None
	transforms = binding.get("transforms", [])
	if len(transforms) != 1 or transforms[0].get("type") != "map":
		return None
	table = {m.get("input"): m.get("output") for m in transforms[0].get("mappings", [])}
	if set(table) != {True, False} or not all(isinstance(v, str) for v in table.values()):
		return None
	return table[True], table[False]


def checkboxText(component, moved):
	"""Params and bindings that show the checkbox text on the object, or None when it cannot be carried."""
	config = component.get("propConfig", {}).get("props.text") or {}
	binding = config.get("binding")
	if set(config) - {"binding", "persistent"}:
		return None
	if not binding:
		return {"question": (component.get("props") or {}).get("text", "") or ""}, {}
	if _describesItem(component, binding):
		return {"question": ""}, _itemID()
	state = _stateTexts(binding, component["type"])
	if state:
		return {"question": "", "trueText": state[0], "falseText": state[1]}, {}
	binding = _rebase(binding, component["type"])
	return ({"question": ""}, {"props.params.question": {"binding": binding}}) if _portable(binding, moved) else None


def carryProps(component, moved):
	"""Params and bindings for the field props (enabled, placeholder, value and option bindings...), or None."""
	ctype = component["type"]
	props = component.get("props") or {}
	mapping = FIELD_PARAMS[ctype]
	if component.get("events") or component.get("scripts"):
		return None
	if any(k != "style" and k not in mapping and k not in OBJECT_SETS[ctype] for k in props):
		return None
	params, bindings = {}, {}
	if props.get("enabled") is False:
		params["enabled"] = False
	if props.get("showClearIcon"):
		params["showClearIcon"] = True
	placeholder = props.get("placeholder")
	if ctype == "ia.input.dropdown":
		text = placeholder.get("text") if isinstance(placeholder, dict) else None
		if text and text != DROPDOWN_PLACEHOLDER:
			params["placeholder"] = text
	elif isinstance(placeholder, str) and placeholder and not RE_DEFAULT_PLACEHOLDER.match(placeholder):
		params["placeholder"] = placeholder
	for key, config in component.get("propConfig", {}).items():
		if key.startswith("custom.item"):
			continue
		if config.get("onChange"):
			return None
		if not key.startswith("props.") or key.startswith("props.style") or (key == "props.text" and ctype == "ia.input.checkbox"):
			continue
		name = key[len("props."):]
		root = name.split(".")[0]
		if root in OBJECT_SETS[ctype]:
			continue
		binding = config.get("binding")
		if root not in mapping or not binding or (name != root and name != "placeholder.text"):
			return None
		if root == "placeholder" and ctype != "ia.input.dropdown" and _describesItem(component, binding):
			params["questionAsPlaceholder"] = True
			bindings.update(_itemID())
			continue
		binding = _rebase(binding, ctype)
		if not _portable(binding, moved):
			return None
		bindings["props.params." + mapping[root]] = dict(config, binding=binding)
	return params, bindings


# ==================== QUESTION OF A LIST ROW ====================

def _questionOf(textOwner, binding, row):
	"""Resolve where a question text comes from: ("text", s) or ("item", id) or None."""
	if not binding:
		return ("text", (textOwner.get("props") or {}).get("text", "") or "")
	transforms = binding.get("transforms", [])
	path = binding.get("config", {}).get("path", "")
	if binding.get("type") != "property" or len(transforms) != 1 or DESCRIPTION_QUERY not in " ".join((transforms[0].get("code") or "").split()):
		return None
	if path == "this.custom.item.papoItemID":
		return ("field", None)
	source = textOwner if path.startswith("this.") else row if path.startswith("parent.") else None
	key = path.split(".", 2)[-1] if source is not None else None
	value = (source or {}).get("custom", {}).get(key.replace("custom.", "", 1)) if key and key.startswith("custom.") else None
	if isinstance(value, int) and ("propConfig" not in source or "custom." + key.replace("custom.", "", 1) not in source.get("propConfig", {})):
		return ("item", value)
	return None


def rowCandidate(row):
	"""Return (field, question) when the row is one field plus at most one question label."""
	if "item" in row.get("custom", {}) and row.get("type") in OBJECTS and row.get("type") != "ia.container.flex":
		field, labels = row, []
	elif row.get("type") == "ia.container.flex" and "item" not in row.get("custom", {}):
		kids = row.get("children", [])
		fields = [k for k in kids if "item" in k.get("custom", {})]
		labels = [k for k in kids if k.get("type") == "ia.display.label" and "item" not in k.get("custom", {})]
		if len(fields) != 1 or len(fields) + len(labels) != len(kids) or len(labels) > 1:
			return None
		field = fields[0]
		if field.get("type") not in OBJECTS or field.get("type") == "ia.container.flex":
			return None
	else:
		return None
	# A field inside a row container moves one level up: its custom.item bindings must not be relative
	if field is not row and any(k.startswith("custom.item") and k != "custom.item.answer" and _relative(v.get("binding"))
			for k, v in field.get("propConfig", {}).items()):
		return None
	if field["type"] == "ia.input.checkbox" and not labels:
		question = ("checkbox", None)
	elif labels:
		# A checkbox with its own text next to a question label is a cell, not a row
		if field["type"] == "ia.input.checkbox" and ((field.get("props") or {}).get("text") or "props.text" in field.get("propConfig", {})):
			return None
		label = labels[0]
		question = _questionOf(label, label.get("propConfig", {}).get("props.text", {}).get("binding"), row)
	else:
		question = ("text", "")
	return (field, question) if question else None


# ==================== EMBEDS ====================

def _embed(field, meta, position, style, params, bindings, path):
	propConfig = {"custom.item.answer": _prop("this.props.params.answer"), "props.params.fontSize": _prop("view.custom.fontSize")}
	propConfig.update({k: copy.deepcopy(v) for k, v in field.get("propConfig", {}).items()
		if k.startswith("custom.item") and k != "custom.item.answer"})
	propConfig.update(bindings)
	return {"custom": {"item": copy.deepcopy(field["custom"]["item"])}, "meta": copy.deepcopy(meta),
		"position": copy.deepcopy(position), "propConfig": propConfig,
		"props": {"params": params, "path": path, "style": style, "useDefaultViewHeight": False, "useDefaultViewWidth": False},
		"type": "ia.display.view"}


def _cellStyle(field, parent, grand):
	"""Layout of an object in a grid cell: keep width/margins and fill the cell."""
	style = {k: v for k, v in ((field.get("props") or {}).get("style") or {}).items() if k != "classes"}
	parentProps = parent.get("props", {})
	stretches = parentProps.get("alignItems", "stretch") == "stretch"
	if parentProps.get("direction", "row") != "column":
		if not stretches:
			style["alignSelf"] = "stretch"
		if not parent.get("position", {}).get("basis") and (grand or {}).get("props", {}).get("direction") == "column":
			style["minHeight"] = "32px"
	elif not stretches:
		style.setdefault("width", "100%")
	return style


def _optionQuestion(group):
	"""(params, bindings, shown) of the question of an option group: its label, static or the item description."""
	labels = [c for c in group.get("children", []) if c.get("type") == "ia.display.label"]
	if not labels:
		return {"question": ""}, {}, False
	binding = labels[0].get("propConfig", {}).get("props.text", {}).get("binding")
	if len(labels) > 1:
		return None
	if not binding:
		return {"question": (labels[0].get("props") or {}).get("text", "") or ""}, {}, True
	transforms = binding.get("transforms", [])
	if (binding.get("type") == "property" and binding.get("config") == {"path": "parent.custom.item.papoItemID"}
			and len(transforms) == 1 and DESCRIPTION_QUERY in _code(transforms[0])):
		return {"question": ""}, _itemID(), True
	return None


def fieldEmbed(field, parent, grand, rule, stats):
	"""Object for a field in a cell (the cell keeps its layout), or None when the field stays native."""
	local = collections.Counter()
	result = objectParams(field, rule, local)
	if result is None:
		return None
	params, bindings = result
	if field["type"] == "ia.input.checkbox":
		text = checkboxText(field, False)
		if text is None:
			return None
		params.update(text[0])
		bindings.update(text[1])
	elif rule["kind"] == "options":
		question = _optionQuestion(field)
		if question is None:
			return None
		params.update(question[0], showQuestion=question[2])
		bindings.update(question[1])
		# The question keeps the width of the original label, so the options start where the checkboxes did
		basis = str(([c for c in field.get("children", []) if c.get("type") == "ia.display.label"] or [{}])[0].get("position", {}).get("basis", ""))
		if basis.endswith("px") or basis.endswith("%"):
			params["questionBasis"] = basis
	else:
		params["showQuestion"] = False
	local[OBJECTS[field["type"]]] += 1
	stats.update(local)
	return _embed(field, field["meta"], field.get("position", {}), _cellStyle(field, parent, grand), params, bindings, OBJECTS[field["type"]])


def rowEmbed(row, field, question, rule, stats):
	"""Object for a whole list row (question inside), or None when the row is not converted as a row."""
	moved = field is not row
	local = collections.Counter()
	result = objectParams(field, rule, local, moved)
	if result is None:
		return None
	params, bindings = result
	kind, value = question
	if kind == "checkbox":
		text = checkboxText(field, moved)
		if text is None:
			return None
		params.update(text[0])
		bindings.update(text[1])
	elif kind == "text":
		params["question"] = value
	elif kind == "item":
		params.update(question="", papoItemID=value)
	else:
		params["question"] = ""
		bindings.update(_itemID())
	if field["type"] != "ia.input.checkbox":
		# A row without a question keeps the field at full width
		params["showQuestion"] = question != ("text", "")
	basis = str(row.get("position", {}).get("basis", ""))
	height = int(float(basis[:-2])) if basis.endswith("px") else 0
	position = {"basis": "{}px".format(max(height, ROW_BASIS)), "shrink": 0}
	local["filas de lista"] += 1
	local[OBJECTS[field["type"]]] += 1
	stats.update(local)
	return _embed(field, row["meta"], position, {}, params, bindings, OBJECTS[field["type"]])


def _registerTypes(ids):
	"""RegisterTypeID of papoitems (SELECT on the test database)."""
	env = dict(os.environ)
	for line in open(qa.DB_ENV):
		k, _, v = line.strip().partition("=")
		env[k] = v
	q = "SET NOCOUNT ON; SELECT ID, RegisterTypeID FROM papoitem WHERE ID IN ({}) FOR JSON PATH".format(",".join(str(int(i)) for i in ids))
	r = subprocess.run(["docker", "exec", "-e", "SQLCMDUSER", "-e", "SQLCMDPASSWORD", "mssql", "/opt/mssql-tools18/bin/sqlcmd",
		"-S", "localhost", "-d", "cla-db-papo", "-C", "-y", "0", "-Q", q], capture_output=True, text=True, env=env)
	rows = json.loads("".join(l for l in r.stdout.splitlines() if not l.startswith("JSON_")) or "[]")
	return {row["ID"]: row["RegisterTypeID"] for row in rows}


def repeaterBlock(repeater, stats):
	"""Container with one Objects/Checkbox per instance of a Fundamental Views/Checkbox repeater."""
	props = repeater.get("props") or {}
	instances = props.get("instances") or []
	ids = [inst.get("papoItemID", (inst.get("item") or {}).get("papoItemID")) for inst in instances]
	types = _registerTypes(ids) if ids else {}
	if any(i not in types for i in ids):
		return None
	children = []
	for n, (inst, pid) in enumerate(zip(instances, ids), 1):
		item = {"papoItemID": pid, "registerTypeID": types[pid]}
		node = {"custom": {"item": item}, "meta": {"name": "Item{}".format(n)}, "propConfig": {}, "props": {}, "type": "ia.input.checkbox"}
		# Unmounted, the original read the answer stored in the instance; mounted, the checkbox starts unchecked
		stored = (inst.get("item") or {}).get("answer") or "No Cumple"
		params = {"question": "", "trueValue": "Cumple", "falseValue": "No Cumple", "value": False, "answer": stored}
		children.append(_embed(node, node["meta"], props.get("elementPosition", {}), {}, params,
			{"props.params.papoItemID": _prop("this.custom.item.papoItemID")}, "Objects/Checkbox"))
		stats["Objects/Checkbox"] += 1
	stats["repeaters"] += 1
	return {"children": children, "meta": copy.deepcopy(repeater["meta"]), "position": copy.deepcopy(repeater.get("position", {})),
		"props": {"direction": props.get("direction", "row"), "style": copy.deepcopy(props.get("style", {}))}, "type": "ia.container.flex"}


# ==================== LEGACY HANDLERS ====================

_SENT = None


def sentMessages():
	"""Message types sent anywhere in the project (literal names in views and the Project Library)."""
	global _SENT
	if _SENT is None:
		_SENT = set()
		patterns = (r"sendMessage\(\s*(?:messageType\s*=\s*)?\\?[\"']([^\"'\\]+)", r"btnActionPrimary\s*=\s*\\?[\"']([^\"'\\]+)")
		files = glob.glob(os.path.join(design.VIEWS_DIR, "**", "view.json"), recursive=True)
		files += glob.glob(os.path.join(design.REPO_ROOT, "cla-project", "ignition", "script-python", "**", "code.py"), recursive=True)
		for f in files:
			text = open(f, encoding="utf-8").read()
			for p in patterns:
				_SENT.update(re.findall(p, text))
	return _SENT


def dropLegacyAnswers(view, stats):
	"""Remove the reactive custom.answers of FlexContainerGroupN / FlexContainerSupervisor (v2, paso 4)."""
	references = view_refs.refs(view)
	for child in view["root"].get("children", []):
		name = child.get("meta", {}).get("name", "")
		if not GROUP.match(name) or ("answers" not in child.get("custom", {}) and "custom.answers" not in child.get("propConfig", {})):
			continue
		path = ("root", name)
		used = any(t == path and r.startswith("custom.answers") and o != path for o, t, r in references)
		if used:
			stats["custom.answers en uso: " + name] += 1
			continue
		child.get("custom", {}).pop("answers", None)
		child.get("propConfig", {}).pop("custom.answers", None)
		stats["custom.answers legacy quitados"] += 1


def dropLegacy(view, stats):
	"""Remove save handlers nobody sends (legacy duplicates of saveDataRoot)."""
	kept = []

	def walk(node, isRoot):
		scripts = node.get("scripts") or {}
		handlers = scripts.get("messageHandlers") or []
		keep = []
		for h in handlers:
			name, code = h.get("messageType"), h.get("script") or ""
			standard = isRoot and name == "saveDataRoot"
			legacySave = "registerhistory" in code.lower() or "papo_db" in code
			if not standard and legacySave and name not in sentMessages():
				stats["handlers legacy quitados"] += 1
			else:
				keep.append(h)
				if not standard:
					kept.append(name)
		if handlers:
			scripts["messageHandlers"] = keep
		for child in node.get("children", []):
			walk(child, False)
	walk(view["root"], True)
	return kept


# ==================== VIEW ====================

def _conflict(references, removed, keepItem):
	"""True when something outside the removed subtree references it (custom.item/meta/position allowed on keepItem)."""
	for owner, target, rest in references:
		if owner[:len(removed)] == removed or target[:len(removed)] != removed:
			continue
		if keepItem and target == removed and (rest.startswith("custom.item") or rest.split(".")[0] in ("meta", "position")):
			continue
		return True
	return False


def _pxSum(group):
	total = 0.0
	for child in group.get("children", []):
		basis = str(child.get("position", {}).get("basis", ""))
		if basis.endswith("px"):
			try:
				total += float(basis[:-2])
			except ValueError:
				pass
	return total


def _sectionHeights(view):
	"""Groups whose expanded height is fixed (custom.baseBasisPx, used by papo_core.ui.toggleSection)."""
	return {g["meta"]["name"]: g for g in view["root"].get("children", []) if GROUP.match(g.get("meta", {}).get("name", ""))
		and isinstance((g.get("custom") or {}).get("baseBasisPx"), (int, float)) and "custom.baseBasisPx" not in g.get("propConfig", {})}


def standardize(view, options, stats):
	"""Convert the view in place."""
	heights = {name: _pxSum(g) for name, g in _sectionHeights(view).items()}
	if options.get("legacy"):
		dropLegacyAnswers(view, stats)
		for name in dropLegacy(view, stats):
			stats["handlers no estándar que quedan: " + name] += 1
	references = view_refs.refs(view)

	def convertField(node, path, parent, grand):
		rule = answerRule(node)
		if rule is None:
			stats["nativos (lógica propia)"] += 1
			return node
		if _conflict(references, path, True):
			stats["nativos (referenciados)"] += 1
			return node
		embed = fieldEmbed(node, parent, grand, rule, stats)
		if embed is None:
			stats["nativos (propiedades sin parámetro)"] += 1
			return node
		return embed

	def walk(node, path, parent, grand):
		for i, child in enumerate(node.get("children", [])):
			childPath = path + (child.get("meta", {}).get("name", "?"),)
			if child.get("type") == "ia.display.flex-repeater":
				if options.get("repeaters") and (child.get("props") or {}).get("path") == REPEATER_VIEW and not _conflict(references, childPath, False):
					block = repeaterBlock(child, stats)
					if block:
						node["children"][i] = block
						continue
				stats["repeaters sin convertir"] += 1
				continue
			# Rows only in column groups; in row groups (FlexContainerSupervisor) each child is a cell
			if options.get("rows") and GROUP.match(node.get("meta", {}).get("name", "")) and (node.get("props") or {}).get("direction") == "column":
				candidate = rowCandidate(child)
				if candidate and answerRule(candidate[0]) and not _conflict(references, childPath, child is candidate[0]):
					embed = rowEmbed(child, candidate[0], candidate[1], answerRule(candidate[0]), stats)
					if embed is not None:
						node["children"][i] = embed
						continue
			if "item" in child.get("custom", {}) and child.get("type") in OBJECTS:
				node["children"][i] = convertField(child, childPath, node, parent)
				if node["children"][i] is not child or child.get("type") != "ia.container.flex":
					continue
			walk(child, childPath, node, parent)

	walk(view["root"], ("root",), None, None)
	# Rows taller than before: the expanded section grows by the same amount (otherwise its end is cut)
	for name, group in _sectionHeights(view).items():
		grown = _pxSum(group) - heights.get(name, 0)
		if name in heights and grown > 0:
			group["custom"]["baseBasisPx"] = int(round(group["custom"]["baseBasisPx"] + grown))
			stats["secciones con más alto"] += 1
	if options.get("formClass"):
		style = view["root"].setdefault("props", {}).setdefault("style", {})
		tokens = str(style.get("classes", "")).split()
		if "PAPO/Form" not in tokens and "props.style.classes" not in view["root"].get("propConfig", {}):
			style["classes"] = " ".join(tokens + ["PAPO/Form"])


def processView(path, apply, backupDir, stats, options):
	"""Convert one view. Returns (status, detail)."""
	view, usesCrlf, isCanonical = design.loadView(path)
	if not isCanonical:
		return "rechazada", "no es Gson canónico"
	before = copy.deepcopy(view)
	viewStats = collections.Counter()
	standardize(view, options, viewStats)
	if [qa._key(s) for s in qa.answerSources(before)] != [qa._key(s) for s in qa.answerSources(view)]:
		return "error", "cambió la recolección de respuestas"
	newBroken = view_refs.broken(view) - view_refs.broken(before)
	if newBroken:
		return "error", "referencias rotas nuevas: {}".format(sorted(newBroken)[:2])
	stats.update(viewStats)
	converted = sum(v for k, v in viewStats.items() if k.startswith("Objects/"))
	if view == before:
		return "sin cambios", ""
	if apply:
		target = os.path.join(backupDir, os.path.relpath(path, design.REPO_ROOT))
		os.makedirs(os.path.dirname(target), exist_ok=True)
		if not os.path.exists(target):
			shutil.copy2(path, target)
		design.writeView(path, view, usesCrlf)
	return ("aplicada" if apply else "aplicable"), "{} objetos, {} ítems iguales".format(converted, len(qa.answerSources(view)))


def main():
	parser = argparse.ArgumentParser(description="Formularios PAPO al estándar de objetos")
	parser.add_argument("--views", nargs="*")
	parser.add_argument("--all-forms", action="store_true")
	parser.add_argument("--apply", action="store_true")
	parser.add_argument("--backup", default=os.path.join(design.REPO_ROOT, ".claude", "backups",
		datetime.date.today().isoformat(), "papo-objects"))
	parser.add_argument("--no-rows", action="store_true")
	parser.add_argument("--no-repeaters", action="store_true")
	parser.add_argument("--legacy", action="store_true")
	parser.add_argument("--form-class", action="store_true")
	args = parser.parse_args()
	options = {"rows": not args.no_rows, "repeaters": not args.no_repeaters, "legacy": args.legacy, "formClass": args.form_class}

	stats = collections.Counter()
	results = collections.OrderedDict()
	for path in design.resolveViews(args):
		try:
			results[path] = processView(path, args.apply, args.backup, stats, options)
		except Exception as e:
			results[path] = ("error", "{}: {}".format(type(e).__name__, e))
	byStatus = collections.Counter(s for s, _ in results.values())
	print("papo-objects: {}".format("aplicado" if args.apply else "simulación (no se escribió nada)"))
	print("Vistas: " + ", ".join("{} {}".format(n, s) for s, n in byStatus.most_common()))
	print("Detalle: " + ", ".join("{} {}".format(n, k) for k, n in stats.most_common()))
	for path, (status, detail) in results.items():
		if status not in ("sin cambios",):
			print("- {} · {} · {}".format(os.path.relpath(os.path.dirname(path), design.VIEWS_DIR), status, detail))
	return 1 if byStatus.get("error") else 0


if __name__ == "__main__":
	sys.exit(main())
