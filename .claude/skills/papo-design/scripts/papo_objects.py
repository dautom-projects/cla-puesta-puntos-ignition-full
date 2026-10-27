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

Version: 2.13.2

Changelog:
	2026-10-24 | William M. | v1.0.0 - Initial version (EA11-0901_1h pilot)
	2026-10-25 | William M. | v2.0.0 - Row and repeater modes, emptyAnswer, checkbox fallback,
		option groups, date-time, legacy cleanup, PAPO/Form, reference safety
	2026-10-25 | William M. | v2.1.0 - Carry every field prop (checkbox text and state text, question as
		placeholder, enabled, value/option bindings) or keep the field native; rows only in column
		groups; a row without a question takes the full width
	2026-10-25 | William M. | v2.2.0 - Section height (custom.baseBasisPx) grows with the rows; an option
		group keeps the width of its question label
	2026-10-26 | William M. | v2.3.0 - Questions always from papoItemID: a fixed question text of an item with a
		known papoItemID becomes the papoitem description (--questions-sql writes the UPDATE when the base
		differs); display transforms after the description query are dropped
	2026-10-26 | William M. | v2.4.0 - papoItemID fixed in custom.item (--static-ids): the runtime value of the
		basePapo + index (and similar) bindings is computed with item_ids.py and the binding removed
	2026-10-26 | William M. | v2.5.0 - Time fields: startNow instead of the value stored in the design (the native
		date-time input shows the time the form opens)
	2026-10-26 | William M. | v2.6.0 - Numeric range from the field's own color script (ranges.py): start +/- rang
		is carried, and a red that is not a closed range (only a lower bound) leaves the field native
	2026-10-26 | William M. | v2.7.0 - An item saved for several questions of a view (e.g. 207 in EA11-0901_2h: the
		1-hour section repeats 30-minute checks) keeps each fixed question; --questions-sql skips the items whose
		base text wins (docs/sql/preguntas_texto_base.json)
	2026-10-26 | William M. | v2.7.1 - A numeric field without a stored value starts with "" (what the native field
		saves when the operator does not touch it), not None
	2026-10-26 | William M. | v2.8.0 - No repeater container: each instance of a Fundamental Views/Checkbox repeater is a
		row of the group (Objects/Checkbox named like any component), like the list forms; the section height counts
		the repeater rows before the change
	2026-10-26 | William M. | v2.9.0 - Sections fit their rows (fitSections): an open group keeps its height
		(shrink 0) and custom.baseBasisPx is at least the rows plus their margins and the group padding, so no row is
		squeezed and the end of the section is not cut
	2026-10-26 | William M. | v2.9.1 - Hidden rows (position.display false) do not count in the section height
	2026-10-26 | William M. | v2.10.0 - Items of docs/sql/preguntas_texto_fijo.json keep their question written in
		the form (short texts under a heading)
	2026-10-26 | William M. | v2.10.1 - The legacy cleanup removes, with custom.answers, the group timer that only
		refreshed it (custom.refreshSecond: now(1000) + refreshBinding("custom.{}".format("answers"))); a group whose
		own scripts use custom.answers otherwise keeps it
	2026-10-26 | William M. | v2.11.0 - The legacy cleanup also removes the custom.answers collector of inner
		containers (rows of FU10-0202_dia): it read the field value and kept the field native as "referenced"
	2026-10-27 | William M. | v2.12.0 - Phase 5: ranges.py v1.1 (bounds computed by the script, "9999..." upper
		bound, only a minimum, getRangeColor with fixed bounds, never-red scripts); a field the rest of the view only
		reads in bindings (X.props.value, .selected, .text) becomes an object with the same name and those bindings
		read X.props.params.value; option groups answered by a chain of if() (empty answer from the chain); a
		checkbox that answers its own Sí / No text
	2026-10-27 | William M. | v2.13.0 - Bounds chosen by other fields (ranges.dynamicRange, EA11-2501_2h): minValue /
		maxValue bound to the same struct; numeric inputBounds carried to the object (Objects/NumericField v2.6)
	2026-10-27 | William M. | v2.13.1 - A label row without a px height counts the height of its text lines in the
		section (the general test found sections cut by "Referencia hora/hora" labels of 23 px counted as 0)
	2026-10-27 | William M. | v2.13.2 - fitSections also fits section groups without custom.baseBasisPx: their px
		position.basis is the expanded height toggleSection takes (general test of F&A: AC10-1101, CA02-2102, AC10 _end)

Args (CLI):
	--views (str...) / --all-forms: views to convert
	--apply: write (default: dry run)  --backup (str): backup folder
	--no-rows, --no-repeaters: disable those modes
	--legacy: remove dead legacy save handlers  --form-class: add PAPO/Form to the root
	--questions-sql (str): write the UPDATE papoitem script for fixed questions that differ from the base
	--static-ids: papoItemID fixed in custom.item instead of computed (one logic for every form)

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
import item_ids
import ranges
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
# Value and answer of a field without a stored value (the native component saves "" when nobody touches it)
DEFAULTS = {"Objects/NumericField": ("", ""), "Objects/TextField": ("", "")}
GROUP = re.compile(r"^(FlexContainerGroup\d+|FlexContainerSupervisor)$")
DESCRIPTION_QUERY = "SELECT Description FROM papoitem WHERE ID = ?"
# Field props each object takes as a param (static value or binding)
FIELD_PARAMS = {
	"ia.input.checkbox": {"selected": "value", "enabled": "enabled"},
	"ia.input.numeric-entry-field": {"value": "value", "placeholder": "placeholder", "enabled": "enabled", "inputBounds": "inputBounds"},
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
		return {"kind": "options", "options": options, "empty": qa.optionEmpty(component)} if options else None
	state = qa.checkboxTextAnswer(component)
	if state:
		# The answer is the checkbox text, mapped from its state (Sí / No): same values as trueValue / falseValue
		return {"kind": "checkbox", "true": state[0], "false": state[1]}
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
	"""Closed range that paints like the field's own color script (ranges.rangeOf), None or ranges.UNSUPPORTED."""
	return ranges.rangeOf(component)


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
		empty = rule.get("empty", "-")
		params.update(options=rule["options"], emptyAnswer=empty, value=chosen[0] if chosen else None,
			answer=chosen[0] if chosen else empty)
		return params, bindings
	elif kind == "time":
		# The native field opens with the current time (not the value stored in the design): startNow
		params.update(pickerType=props.get("pickerType", "time"), format="h:mm:ss a", value=None, answer=None)
		if "props.value" not in propConfig:
			params["startNow"] = True
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
		if limits == ranges.UNSUPPORTED:
			dynamic = ranges.dynamicRange(component)
			if dynamic is None:
				# Its red is not a closed range (e.g. two valid ranges): the field keeps its own color logic
				stats["numéricos nativos (color fuera de rango propio)"] += 1
				return None
			for param, code in (("minValue", dynamic["minCode"]), ("maxValue", dynamic["maxCode"])):
				config = {"struct": dynamic["struct"]}
				if dynamic["waitOnAll"] is not None:
					config["waitOnAll"] = dynamic["waitOnAll"]
				binding = {"config": config, "transforms": [{"code": code, "type": "script"}], "type": "expr-struct"}
				if not _portable(binding, moved):
					return None
				bindings["props.params." + param] = {"binding": binding}
			stats["numéricos con rango según otro campo"] += 1
			limits = None
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
	"""True when the binding shows the description of the field's own papoItemID (papoitem query).

	Display transforms after the query (e.g. dropping a prefix) are not kept: the standard question is the
	papoitem description as it is.
	"""
	transforms = (binding or {}).get("transforms", [])
	if not binding or binding.get("type") != "property" or not transforms or DESCRIPTION_QUERY not in _code(transforms[0]):
		return False
	path = binding.get("config", {}).get("path")
	if path == "this.custom.item.papoItemID":
		return True
	item = component.get("propConfig", {}).get("custom.item.papoItemID", {}).get("binding") or _FIXED_FROM.get(id(component)) or {}
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


def _staticItemID(component):
	"""papoItemID of the component when it is fixed in custom.item (not bound)."""
	value = ((component.get("custom") or {}).get("item") or {}).get("papoItemID")
	return value if isinstance(value, int) and "custom.item.papoItemID" not in component.get("propConfig", {}) else None


# Items of the view being converted that are saved for more than one question (see standardize)
_SHARED = set()


def _fixedQuestion(component, text, texts):
	"""A fixed question of an item with a known papoItemID reads papoitem; the text goes to texts for the base."""
	pid = _staticItemID(component)
	if not text or pid is None:
		return {"question": text or ""}, {}
	if pid in _SHARED or pid in qa.FIXED_TEXTS:
		# One papoItemID for several questions of the view, or a short text under a heading: the text stays
		return {"question": text}, {}
	if texts is not None:
		texts.append({"papoItemID": pid, "text": text})
	return {"question": ""}, _itemID()


def checkboxText(component, moved, texts=None):
	"""Params and bindings that show the checkbox text on the object, or None when it cannot be carried."""
	config = component.get("propConfig", {}).get("props.text") or {}
	binding = config.get("binding")
	if set(config) - {"binding", "persistent"}:
		return None
	if not binding:
		return _fixedQuestion(component, (component.get("props") or {}).get("text", "") or "", texts)
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
	bounds = props.get("inputBounds")
	if bounds is not None:
		# Only the limits are a param (the invalid style stays the component's)
		if not isinstance(bounds, dict) or set(bounds) - {"minimum", "maximum"}:
			return None
		params["inputBounds"] = {"maximum": bounds.get("maximum"), "minimum": bounds.get("minimum")}
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
	if binding.get("type") != "property" or not transforms or DESCRIPTION_QUERY not in " ".join((transforms[0].get("code") or "").split()):
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


def _optionQuestion(group, texts=None):
	"""(params, bindings, shown) of the question of an option group: its label, static or the item description."""
	labels = [c for c in group.get("children", []) if c.get("type") == "ia.display.label"]
	if not labels:
		return {"question": ""}, {}, False
	binding = labels[0].get("propConfig", {}).get("props.text", {}).get("binding")
	if len(labels) > 1:
		return None
	if not binding:
		fixed = _fixedQuestion(group, (labels[0].get("props") or {}).get("text", "") or "", texts)
		return fixed[0], fixed[1], True
	transforms = binding.get("transforms", [])
	if (binding.get("type") == "property" and binding.get("config") == {"path": "parent.custom.item.papoItemID"}
			and len(transforms) == 1 and DESCRIPTION_QUERY in _code(transforms[0])):
		return {"question": ""}, _itemID(), True
	return None


def fieldEmbed(field, parent, grand, rule, stats, texts=None):
	"""Object for a field in a cell (the cell keeps its layout), or None when the field stays native."""
	local = collections.Counter()
	result = objectParams(field, rule, local)
	if result is None:
		return None
	params, bindings = result
	if field["type"] == "ia.input.checkbox":
		text = checkboxText(field, False, texts)
		if text is None:
			return None
		params.update(text[0])
		bindings.update(text[1])
	elif rule["kind"] == "options":
		question = _optionQuestion(field, texts)
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


def rowEmbed(row, field, question, rule, stats, texts=None):
	"""Object for a whole list row (question inside), or None when the row is not converted as a row."""
	moved = field is not row
	local = collections.Counter()
	result = objectParams(field, rule, local, moved)
	if result is None:
		return None
	params, bindings = result
	kind, value = question
	if kind == "checkbox":
		text = checkboxText(field, moved, texts)
		if text is None:
			return None
		params.update(text[0])
		bindings.update(text[1])
	elif kind == "text":
		fixed = _fixedQuestion(field, value, texts)
		params.update(fixed[0])
		bindings.update(fixed[1])
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


def _freeName(base, taken):
	"""First free component name in the Perspective way: Checkbox, Checkbox_0, Checkbox_1..."""
	name, n = base, 0
	while name in taken:
		name, n = "{}_{}".format(base, n), n + 1
	taken.add(name)
	return name


def _rowPosition(props):
	"""Row of a repeater instance: its element position when it has a px height, else the standard list row (50 px)."""
	position = props.get("elementPosition") or {}
	if str(position.get("basis", "")).endswith("px"):
		return position
	return {"basis": "{}px".format(ROW_BASIS), "shrink": 0}


def repeaterRows(repeater, stats, taken):
	"""One Objects/Checkbox row per instance of a Fundamental Views/Checkbox repeater (no container, like a list)."""
	props = repeater.get("props") or {}
	instances = props.get("instances") or []
	ids = [inst.get("papoItemID", (inst.get("item") or {}).get("papoItemID")) for inst in instances]
	types = _registerTypes(ids) if ids else {}
	if any(i not in types for i in ids):
		return None
	children = []
	for n, (inst, pid) in enumerate(zip(instances, ids), 1):
		item = {"papoItemID": pid, "registerTypeID": types[pid]}
		node = {"custom": {"item": item}, "meta": {"name": _freeName("Checkbox", taken)}, "propConfig": {}, "props": {}, "type": "ia.input.checkbox"}
		# Unmounted, the original read the answer stored in the instance; mounted, the checkbox starts unchecked
		stored = (inst.get("item") or {}).get("answer") or "No Cumple"
		params = {"question": "", "trueValue": "Cumple", "falseValue": "No Cumple", "value": False, "answer": stored}
		children.append(_embed(node, node["meta"], _rowPosition(props), {}, params,
			{"props.params.papoItemID": _prop("this.custom.item.papoItemID")}, "Objects/Checkbox"))
		stats["Objects/Checkbox"] += 1
	stats["repeaters"] += 1
	return children


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


_REFRESH_ONLY = {"answers", "custom.{}", "custom.answers"}


def _answerScripts(group):
	"""(refreshers, otherUse): custom props whose change script only refreshes custom.answers (the legacy timer), and
	whether another script of the group mentions answers (then custom.answers stays)."""
	refreshers, otherUse = [], False
	for prop, config in (group.get("propConfig") or {}).items():
		code = ((config.get("onChange") or {}).get("script") or "") if isinstance(config.get("onChange"), dict) else ""
		if "answers" not in code:
			continue
		if prop.startswith("custom.") and "refreshBinding" in code and set(re.findall(r'"([^"]*)"', code)) <= _REFRESH_ONLY:
			refreshers.append(prop)
		else:
			otherUse = True
	return refreshers, otherUse


def dropLegacyAnswers(view, stats):
	"""Remove the reactive custom.answers of FlexContainerGroupN / FlexContainerSupervisor (v2, paso 4), with the
	group timer that only refreshed it."""
	references = view_refs.refs(view)
	for child in view["root"].get("children", []):
		name = child.get("meta", {}).get("name", "")
		if not GROUP.match(name) or ("answers" not in child.get("custom", {}) and "custom.answers" not in child.get("propConfig", {})):
			continue
		path = ("root", name)
		refreshers, otherUse = _answerScripts(child)
		used = otherUse or any(t == path and r.startswith("custom.answers") and o != path for o, t, r in references)
		used = used or any(t == path and o != path and any(r.startswith(p) for p in refreshers) for o, t, r in references)
		if used:
			stats["custom.answers en uso: " + name] += 1
			continue
		child.get("custom", {}).pop("answers", None)
		child.get("propConfig", {}).pop("custom.answers", None)
		stats["custom.answers legacy quitados"] += 1
		for prop in refreshers:
			child.get("custom", {}).pop(prop.split(".", 1)[1], None)
			child.get("propConfig", {}).pop(prop, None)
			stats["temporizadores de custom.answers quitados"] += 1


def _isCollector(binding):
	"""The legacy custom.answers binding that gathers the custom.item of the container (gather_items)."""
	code = json.dumps((binding or {}).get("transforms", []))
	return "gather_items" in code or "recolecta los custom.item" in code


def dropNestedLegacyAnswers(view, stats):
	"""Remove the legacy custom.answers collector of inner containers (rows), with its timer, when nothing reads it.

	The save flow collects custom.item with papo_core.register.recopile; this per-row copy only read the field value
	and made the converter keep the field native (referenced by its row)."""
	references = view_refs.refs(view)

	def walk(node, path):
		for child in node.get("children", []):
			childPath = path + (child.get("meta", {}).get("name", "?"),)
			config = (child.get("propConfig") or {}).get("custom.answers") or {}
			if len(childPath) > 2 and _isCollector(config.get("binding")):
				refreshers, otherUse = _answerScripts(child)
				used = otherUse or any(t == childPath and o != childPath and (r.startswith("custom.answers")
					or any(r.startswith(p) for p in refreshers)) for o, t, r in references)
				if used:
					stats["custom.answers de fila en uso"] += 1
				else:
					child.get("custom", {}).pop("answers", None)
					child["propConfig"].pop("custom.answers", None)
					for prop in refreshers:
						child.get("custom", {}).pop(prop.split(".", 1)[1], None)
						child["propConfig"].pop(prop, None)
					if not child["propConfig"]:
						child.pop("propConfig")
					stats["custom.answers de fila quitados"] += 1
			walk(child, childPath)

	walk(view["root"], ("root",))


def dropOrphanRefreshers(view, stats):
	"""Group timers left behind by an earlier cleanup: they refresh a custom.answers that no longer exists."""
	references = view_refs.refs(view)
	for child in view["root"].get("children", []):
		name = child.get("meta", {}).get("name", "")
		if not GROUP.match(name) or "answers" in child.get("custom", {}) or "custom.answers" in child.get("propConfig", {}):
			continue
		path = ("root", name)
		refreshers, otherUse = _answerScripts(child)
		for prop in refreshers:
			if any(t == path and o != path and r.startswith(prop) for o, t, r in references):
				continue
			child.get("custom", {}).pop(prop.split(".", 1)[1], None)
			child.get("propConfig", {}).pop(prop, None)
			stats["temporizadores de custom.answers quitados"] += 1


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

# Value prop of a field that other components read; the object exposes it as props.params.value (inout)
VALUE_READ = {
	"ia.input.checkbox": "props.selected",
	"ia.input.numeric-entry-field": "props.value",
	"ia.input.text-field": "props.text",
	"ia.input.dropdown": "props.value",
	"ia.input.date-time-input": "props.value",
}
OBJECT_VALUE = "props.params.value"


def _valueReadsOnly(references, path, ctype):
	"""True when everything outside the field that references it only reads its value in a binding."""
	found = False
	for owner, target, rest in references:
		if owner[:len(path)] == path or target[:len(path)] != path:
			continue
		if target == path and (rest.startswith("custom.item") or rest.split(".")[0] in ("meta", "position")):
			continue
		# Script references come as "script": those keep the field native
		if target != path or rest != VALUE_READ.get(ctype):
			return False
		found = True
	return found


def redirectValueReads(view, targets, stats):
	"""Bindings that read a converted field's value (X.props.value...) read the object's X.props.params.value."""
	wanted = {tuple(path): rest for path, rest in targets}

	def fix(owner, ref):
		r = view_refs.resolve(owner, ref)
		if not r or wanted.get(tuple(r[0])) != r[1] or not ref.strip().endswith(r[1]):
			return None
		stats["referencias al valor redirigidas al objeto"] += 1
		return ref.strip()[:-len(r[1])] + OBJECT_VALUE

	def braces(owner, text):
		def sub(match):
			new = fix(owner, match.group(1))
			return "{" + new + "}" if new else match.group(0)
		return view_refs.RE_BRACES.sub(sub, text)

	def strings(owner, value):
		if isinstance(value, str):
			return braces(owner, value)
		if isinstance(value, dict):
			return {k: strings(owner, v) for k, v in value.items()}
		if isinstance(value, list):
			return [strings(owner, v) for v in value]
		return value

	for owner, node in view_refs.index(view).items():
		for key, cfg in (node.get("propConfig") or {}).items():
			binding = cfg.get("binding") or {}
			config = binding.get("config") or {}
			if binding.get("type") == "property" and config.get("path"):
				new = fix(owner, config["path"])
				if new:
					config["path"] = new
			for k in [k for k in config if k != "path"]:
				config[k] = strings(owner, config[k])
			for transform in binding.get("transforms", []):
				if transform.get("expression"):
					transform["expression"] = braces(owner, transform["expression"])


def _conflict(references, removed, keepItem):
	"""True when something outside the removed subtree references it (custom.item/meta/position allowed on keepItem)."""
	for owner, target, rest in references:
		if owner[:len(removed)] == removed or target[:len(removed)] != removed:
			continue
		if keepItem and target == removed and (rest.startswith("custom.item") or rest.split(".")[0] in ("meta", "position")):
			continue
		return True
	return False


# Line height of a label without a fixed height: the forms use view.custom.fontSize (17 px -> 23 px rows)
DEFAULT_FONT_PX = 17
LINE_FACTOR = 1.35


def _labelHeight(child):
	"""Rendered height of a label row with an automatic height: its text lines at its font size."""
	props = child.get("props") or {}
	size = ((props.get("textStyle") or {}).get("fontSize") or (props.get("style") or {}).get("fontSize"))
	try:
		size = float(str(size).replace("px", "")) if size else DEFAULT_FONT_PX
	except ValueError:
		size = DEFAULT_FONT_PX
	lines = max(1, str(props.get("text", "") or "").count("\n") + 1)
	return -(-size * LINE_FACTOR * lines // 1)


def _pxSum(group):
	total = 0.0
	for child in group.get("children", []):
		if child.get("position", {}).get("display") is False and "position.display" not in child.get("propConfig", {}):
			# A hidden row takes no height
			continue
		basis = str(child.get("position", {}).get("basis", ""))
		if child.get("type") == "ia.display.flex-repeater":
			# A repeater takes its instances' rows when they have a px height, else its own height
			props = child.get("props") or {}
			element = str((props.get("elementPosition") or {}).get("basis", ""))
			if element.endswith("px"):
				basis = "{}px".format(float(element[:-2]) * len(props.get("instances") or []))
		if basis.endswith("px"):
			try:
				total += float(basis[:-2])
			except ValueError:
				pass
		elif child.get("type") == "ia.display.label" and (basis in ("", "auto") or basis.startswith("-")):
			# No height, or an invalid negative basis the browser treats as auto
			total += _labelHeight(child)
	return total


def _vertical(style, side):
	"""Top or bottom margin/padding of a style in px (own side first, then the shorthand number)."""
	style = style or {}
	for key in (side, side.rstrip("TopBottom")):
		value = style.get(key)
		if isinstance(value, (int, float)):
			return float(value)
		if isinstance(value, str) and value.endswith("px"):
			try:
				return float(value[:-2])
			except ValueError:
				return 0.0
	return 0.0


def _rowsHeight(group):
	"""Height the rows of a group need: their px heights, their margins and the group padding and border."""
	total = _pxSum(group)
	for child in group.get("children", []):
		if child.get("position", {}).get("display") is False and "position.display" not in child.get("propConfig", {}):
			continue
		style = (child.get("props") or {}).get("style") or {}
		total += _vertical(style, "marginTop") + _vertical(style, "marginBottom")
	style = (group.get("props") or {}).get("style") or {}
	total += _vertical(style, "paddingTop") + _vertical(style, "paddingBottom")
	total += _vertical(style, "borderTopWidth") + _vertical(style, "borderBottomWidth")
	return total


def fitSections(view, stats):
	"""An open section keeps its height and fits its rows (no squeezed row, no cut end).

	papo_core.ui.toggleSection opens a group with the fixed height custom.baseBasisPx. A group that can shrink is
	squeezed to the visible height of the form, and a height below its rows compresses them.
	"""
	for name, group in list(_sectionHeights(view).items()) + list(_basisHeights(view).items()):
		position = group.setdefault("position", {})
		if position.get("shrink", 1) != 0:
			position["shrink"] = 0
			stats["secciones que ya no se encogen"] += 1
		needed = int(-(-_rowsHeight(group) // 1))
		if isinstance((group.get("custom") or {}).get("baseBasisPx"), (int, float)):
			if needed > group["custom"]["baseBasisPx"]:
				group["custom"]["baseBasisPx"] = needed
				stats["secciones ajustadas a sus filas"] += 1
		elif needed > _px(position["basis"]):
			position["basis"] = "{}px".format(needed)
			stats["secciones ajustadas a sus filas"] += 1


def _sectionHeights(view):
	"""Groups whose expanded height is fixed (custom.baseBasisPx, used by papo_core.ui.toggleSection)."""
	return {g["meta"]["name"]: g for g in view["root"].get("children", []) if GROUP.match(g.get("meta", {}).get("name", ""))
		and isinstance((g.get("custom") or {}).get("baseBasisPx"), (int, float)) and "custom.baseBasisPx" not in g.get("propConfig", {})}


def _basisHeights(view):
	"""Section groups without custom.baseBasisPx: toggleSection takes their px position.basis as the expanded height
	the first time they open."""
	return {g["meta"]["name"]: g for g in view["root"].get("children", [])
		if re.match(r"^FlexContainerGroup\d+$", g.get("meta", {}).get("name", ""))
		and not isinstance((g.get("custom") or {}).get("baseBasisPx"), (int, float))
		and not {"custom.baseBasisPx", "position.basis"} & set(g.get("propConfig", {}))
		and _px((g.get("position") or {}).get("basis")) > 0}


def _px(basis):
	"""Pixels of a "<n>px" basis; 0 for any other basis."""
	match = re.match(r"^(\d+(?:\.\d+)?)px$", str(basis or ""))
	return float(match.group(1)) if match else 0


# Binding a fixed papoItemID came from (id(node) -> binding), so the description bindings that read the same
# source are still recognized as the item description after fixItemIDs
_FIXED_FROM = {}


def fixItemIDs(view, stats):
	"""papoItemID fixed in custom.item: computed bindings get their runtime value, disabled ones are removed."""
	_FIXED_FROM.clear()
	ids = item_ids.resolve(view)
	for path, node in view_refs.index(view).items():
		propConfig = node.get("propConfig") or {}
		config = propConfig.get("custom.item.papoItemID")
		item = (node.get("custom") or {}).get("item")
		if not config or not isinstance(item, dict) or set(config) - {"binding", "persistent"}:
			continue
		value = ids.get(path)
		disabled = (config.get("binding") or {}).get("enabled") is False
		if not isinstance(value, int) or isinstance(value, bool):
			stats["papoItemID sin calcular"] += 1
			continue
		item["papoItemID"] = value
		if not disabled:
			_FIXED_FROM[id(node)] = config.get("binding")
		del propConfig["custom.item.papoItemID"]
		if not propConfig:
			node.pop("propConfig")
		stats["papoItemID fijados" + (" (binding desactivado)" if disabled else "")] += 1


def standardize(view, options, stats):
	"""Convert the view in place."""
	global _SHARED
	if "sharedItems" not in options:
		# First pass on a copy: items whose fixed questions have more than one text in this view
		found = []
		standardize(copy.deepcopy(view), dict(options, questionTexts=found, sharedItems=set()), collections.Counter())
		byID = collections.defaultdict(set)
		for entry in found:
			byID[entry["papoItemID"]].add(entry["text"].strip())
		options = dict(options, sharedItems={pid for pid, texts in byID.items() if len(texts) > 1})
	_SHARED = options["sharedItems"]
	if _SHARED:
		stats["ítems con varias preguntas (texto fijo)"] += len(_SHARED)
	if options.get("staticIDs"):
		fixItemIDs(view, stats)
	heights = {name: _pxSum(g) for name, g in _sectionHeights(view).items()}
	if options.get("legacy"):
		dropLegacyAnswers(view, stats)
		dropNestedLegacyAnswers(view, stats)
		dropOrphanRefreshers(view, stats)
		for name in dropLegacy(view, stats):
			stats["handlers no estándar que quedan: " + name] += 1
	references = view_refs.refs(view)
	redirects = []

	def convertField(node, path, parent, grand):
		rule = answerRule(node)
		if rule is None:
			stats["nativos (lógica propia)"] += 1
			return node
		readOnly = False
		if _conflict(references, path, True):
			readOnly = _valueReadsOnly(references, path, node.get("type"))
			if not readOnly:
				stats["nativos (referenciados)"] += 1
				return node
		embed = fieldEmbed(node, parent, grand, rule, stats, options.get("questionTexts"))
		if embed is None:
			stats["nativos (propiedades sin parámetro)"] += 1
			return node
		if readOnly:
			# Same name and place: the bindings that read its value are pointed at the object after the walk
			redirects.append((path, VALUE_READ[node["type"]]))
			stats["campos leídos por otros convertidos"] += 1
		return embed

	def walk(node, path, parent, grand):
		for i, child in enumerate(node.get("children", [])):
			childPath = path + (child.get("meta", {}).get("name", "?"),)
			if child.get("type") == "ia.display.flex-repeater":
				if options.get("repeaters") and (child.get("props") or {}).get("path") == REPEATER_VIEW and not _conflict(references, childPath, False):
					taken = {c.get("meta", {}).get("name") for c in node.get("children", []) if c is not child}
					rows = repeaterRows(child, stats, taken)
					if rows:
						# Replaced by its rows after the loop (the list keeps the position of the repeater)
						node["children"][i] = rows
						continue
				stats["repeaters sin convertir"] += 1
				continue
			# Rows only in column groups; in row groups (FlexContainerSupervisor) each child is a cell
			if options.get("rows") and GROUP.match(node.get("meta", {}).get("name", "")) and (node.get("props") or {}).get("direction") == "column":
				candidate = rowCandidate(child)
				if candidate and answerRule(candidate[0]) and not _conflict(references, childPath, child is candidate[0]):
					embed = rowEmbed(child, candidate[0], candidate[1], answerRule(candidate[0]), stats, options.get("questionTexts"))
					if embed is not None:
						node["children"][i] = embed
						continue
			if "item" in child.get("custom", {}) and child.get("type") in OBJECTS:
				node["children"][i] = convertField(child, childPath, node, parent)
				if node["children"][i] is not child or child.get("type") != "ia.container.flex":
					continue
			walk(child, childPath, node, parent)
		if any(isinstance(c, list) for c in node.get("children", [])):
			node["children"] = [row for c in node["children"] for row in (c if isinstance(c, list) else [c])]

	walk(view["root"], ("root",), None, None)
	if redirects:
		redirectValueReads(view, redirects, stats)
	# Rows taller than before: the expanded section grows by the same amount (otherwise its end is cut)
	for name, group in _sectionHeights(view).items():
		grown = _pxSum(group) - heights.get(name, 0)
		if name in heights and grown > 0:
			group["custom"]["baseBasisPx"] = int(round(group["custom"]["baseBasisPx"] + grown))
			stats["secciones con más alto"] += 1
	fitSections(view, stats)
	if options.get("formClass"):
		style = view["root"].setdefault("props", {}).setdefault("style", {})
		tokens = str(style.get("classes", "")).split()
		if "PAPO/Form" not in tokens and "props.style.classes" not in view["root"].get("propConfig", {}):
			style["classes"] = " ".join(tokens + ["PAPO/Form"])


def _descriptions(ids):
	"""papoitem.Description by ID (SELECT on the test database)."""
	env = dict(os.environ)
	for line in open(qa.DB_ENV):
		k, _, v = line.strip().partition("=")
		env[k] = v
	q = "SET NOCOUNT ON; SELECT ID, Description FROM papoitem WHERE ID IN ({}) FOR JSON PATH, INCLUDE_NULL_VALUES".format(",".join(str(int(i)) for i in ids))
	r = subprocess.run(["docker", "exec", "-e", "SQLCMDUSER", "-e", "SQLCMDPASSWORD", "mssql", "/opt/mssql-tools18/bin/sqlcmd",
		"-S", "localhost", "-d", "cla-db-papo", "-C", "-y", "0", "-Q", q], capture_output=True, text=True, env=env)
	rows = json.loads("".join(l for l in r.stdout.splitlines() if not l.startswith("JSON_")) or "[]")
	return {row["ID"]: row["Description"] for row in rows}


def _sql(text):
	return "NULL" if text is None else "N'" + text.replace("'", "''") + "'"


def writeQuestionsSql(found, path):
	"""UPDATE papoitem for fixed questions whose text differs from the base; conflicts are reported, not written."""
	byID = collections.OrderedDict()
	for entry in found:
		byID.setdefault(entry["papoItemID"], []).append(entry)
	current = _descriptions(list(byID)) if byID else {}
	updates, conflicts, missing = [], [], []
	for pid, entries in byID.items():
		texts = sorted({e["text"].strip() for e in entries})
		if pid in qa.BASE_TEXTS:
			continue
		if pid not in current:
			missing.append(pid)
		elif len(texts) > 1:
			conflicts.append((pid, texts, sorted({e["view"] for e in entries})))
		elif texts[0] != (current[pid] or "").strip():
			updates.append((pid, texts[0], current[pid], sorted({e["view"] for e in entries})))
	lines = ["-- Preguntas fijas de los formularios -> papoitem.Description",
		"-- Generado por papo_objects.py --questions-sql el {}: el formulario lee la pregunta de papoItemID y".format(datetime.date.today().isoformat()),
		"-- la base queda con el texto que mostraba. Aplicar en cla-db-papo y luego en producción.", ""]
	if updates:
		lines += ["SET XACT_ABORT ON;", "BEGIN TRANSACTION;"]
		for pid, text, old, views in updates:
			lines.append("-- {} · antes: {}".format(", ".join(views), _sql(old)))
			lines.append("UPDATE papoitem SET Description = {} WHERE ID = {};".format(_sql(text), pid))
		lines += ["COMMIT;", "", "-- Rollback:"]
		lines += ["-- UPDATE papoitem SET Description = {} WHERE ID = {};".format(_sql(old), pid) for pid, _, old, _ in updates]
	else:
		lines.append("-- Sin diferencias: la base ya tiene el texto de cada pregunta.")
	for pid in sorted(qa.BASE_TEXTS & set(byID)):
		lines.append("-- TEXTO DE LA BASE {}: se queda el de papoitem (preguntas_texto_base.json)".format(pid))
	for pid, texts, views in conflicts:
		lines.append("-- CONFLICTO {}: textos distintos para el mismo ítem en {}: {}".format(pid, ", ".join(views), " | ".join(texts)))
	for pid in missing:
		lines.append("-- NO EXISTE en papoitem: {}".format(pid))
	os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
	open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
	return len(updates), conflicts, missing


def processView(path, apply, backupDir, stats, options):
	"""Convert one view. Returns (status, detail)."""
	view, usesCrlf, isCanonical = design.loadView(path)
	if not isCanonical:
		return "rechazada", "no es Gson canónico"
	before = copy.deepcopy(view)
	viewStats = collections.Counter()
	texts = []
	standardize(view, dict(options, questionTexts=texts), viewStats)
	if [qa._key(s) for s in qa.answerSources(before)] != [qa._key(s) for s in qa.answerSources(view)]:
		return "error", "cambió la recolección de respuestas"
	newBroken = view_refs.broken(view) - view_refs.broken(before)
	if newBroken:
		return "error", "referencias rotas nuevas: {}".format(sorted(newBroken)[:2])
	stats.update(viewStats)
	if texts:
		stats["preguntas fijas a papoItemID"] += len(texts)
		options.setdefault("questionsFound", []).extend(dict(t, view=os.path.relpath(os.path.dirname(path), design.VIEWS_DIR)) for t in texts)
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
	parser.add_argument("--questions-sql")
	parser.add_argument("--static-ids", action="store_true")
	args = parser.parse_args()
	options = {"rows": not args.no_rows, "repeaters": not args.no_repeaters, "legacy": args.legacy, "formClass": args.form_class,
		"staticIDs": args.static_ids}

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
	if args.questions_sql:
		updates, conflicts, missing = writeQuestionsSql(options.get("questionsFound", []), args.questions_sql)
		print("Preguntas: {} UPDATE en {} · {} conflictos · {} ítems inexistentes".format(updates, args.questions_sql, len(conflicts), len(missing)))
	return 1 if byStatus.get("error") else 0


if __name__ == "__main__":
	sys.exit(main())
