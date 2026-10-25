"""
Converts the interactive fields of PAPO Form views into embedded standard objects (Objects/*, v2).

The custom.item of each field stays on the form component (an ia.display.view at the same
position, inside the same FlexContainerGroupN). Its answer reads the object's output param
"answer"; papoItemID/registerTypeID and their bindings stay as they were, so
papo_core.register.recopile collects the same items in the same order. Fields whose answer has
logic of their own, and tag labels, stay native. Dry run by default.

Version: 1.0.0

Changelog:
	2026-10-24 | William M. | v1.0.0 - Initial version (EA11-0901_1h pilot)

Args (CLI):
	--views (str...): View folders or view.json paths
	--all-forms: Every Form_* view of the project
	--apply: Write the changes (default: dry run)
	--backup (str): Backup folder for --apply

Returns:
	Exit code 0 when every view passed verification, 1 otherwise
"""

import argparse
import collections
import copy
import datetime
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(__file__))
import papo_design as design

OBJECTS = {
	"ia.input.checkbox": "Objects/Checkbox",
	"ia.input.numeric-entry-field": "Objects/NumericField",
	"ia.input.text-field": "Objects/TextField",
	"ia.input.dropdown": "Objects/Dropdown",
}
VALUE_PROP = {
	"ia.input.checkbox": "this.props.selected",
	"ia.input.numeric-entry-field": "this.props.value",
	"ia.input.text-field": "this.props.text",
	"ia.input.dropdown": "this.props.value",
}
# Value and answer the form keeps while the object is not mounted (closed section)
DEFAULTS = {
	"Objects/NumericField": (None, None),
	"Objects/TextField": ("", ""),
}
RE_RANGE = re.compile(r"([\d.]+)\s*<=\s*value\s*<=\s*([\d.]+)")


def _prop(path):
	"""Property binding config."""
	return {"binding": {"config": {"path": path}, "type": "property"}}


def _isLabelLookup(transform):
	"""True for the dropdown script that answers with the label of the selected option."""
	code = transform.get("code") or ""
	return (transform.get("type") == "script" and "self.props.options" in code
		and 'item["label"]' in code and 'str(item["value"]) == str(value)' in code)


def convertible(component):
	"""True when the answer is the plain field value (checkbox: true/false map; dropdown: label lookup)."""
	binding = component.get("propConfig", {}).get("custom.item.answer", {}).get("binding")
	ctype = component.get("type")
	if not binding or binding.get("type") != "property" or binding["config"].get("path") != VALUE_PROP[ctype]:
		return False
	transforms = binding.get("transforms", [])
	if ctype == "ia.input.checkbox":
		return (len(transforms) == 1 and transforms[0].get("type") == "map"
			and {m.get("input") for m in transforms[0].get("mappings", [])} == {True, False})
	if ctype == "ia.input.dropdown" and len(transforms) == 1:
		return _isLabelLookup(transforms[0])
	return not transforms


def _rangeOf(component):
	"""Return (min, max) from custom.rang_down/rang_up or from the literal range of the color script."""
	custom = component.get("custom", {})
	if "rang_down" in custom and "rang_up" in custom:
		return custom["rang_down"], custom["rang_up"]
	color = component.get("propConfig", {}).get("custom.color")
	if color:
		match = RE_RANGE.search(color["binding"]["transforms"][0].get("code") or "")
		if match:
			return tuple(float(x) if "." in x else int(x) for x in match.groups())
	return None


def convert(component, parent, grand, stats):
	"""Return the ia.display.view that replaces one native field."""
	ctype = component["type"]
	path = OBJECTS[ctype]
	propConfig = component.get("propConfig", {})
	props = component.get("props", {})
	params = {}
	newPropConfig = {"custom.item.answer": _prop("this.props.params.answer"),
		"props.params.fontSize": _prop("view.custom.fontSize")}
	# Other custom.item bindings (papoItemID, registerTypeID) stay on the form component
	newPropConfig.update({k: copy.deepcopy(v) for k, v in propConfig.items()
		if k.startswith("custom.item") and k != "custom.item.answer"})

	if ctype == "ia.input.checkbox":
		mappings = propConfig["custom.item.answer"]["binding"]["transforms"][0]["mappings"]
		outputs = {m["input"]: m["output"] for m in mappings}
		params.update(question=props.get("text", ""), trueValue=outputs[True], falseValue=outputs[False],
			value=False, answer=outputs[False])
	elif ctype == "ia.input.dropdown":
		labelMode = bool(propConfig["custom.item.answer"]["binding"].get("transforms"))
		params.update(showQuestion=False, value=None, answerFrom="label" if labelMode else "value",
			answer="" if labelMode else None)
		if "props.options" in propConfig:
			newPropConfig["props.params.options"] = copy.deepcopy(propConfig["props.options"])
		else:
			params["options"] = props.get("options", [])
		stats["dropdown " + params["answerFrom"]] += 1
	else:
		value, answer = DEFAULTS[path]
		params.update(showQuestion=False, value=value, answer=answer)
		limits = _rangeOf(component) if ctype == "ia.input.numeric-entry-field" else None
		if limits:
			params.update(minValue=limits[0], maxValue=limits[1])
			stats["numéricos con rango"] += 1

	# Layout stays on the form: keep width/margins and make the object fill its cell
	style = {k: v for k, v in (props.get("style") or {}).items() if k != "classes"}
	parentProps = parent.get("props", {})
	stretches = parentProps.get("alignItems", "stretch") == "stretch"
	if parentProps.get("direction", "row") != "column":
		if not stretches:
			style["alignSelf"] = "stretch"
		if not parent.get("position", {}).get("basis") and (grand or {}).get("props", {}).get("direction") == "column":
			style["minHeight"] = "32px"
	elif not stretches:
		style.setdefault("width", "100%")

	stats[path] += 1
	return {"custom": {"item": copy.deepcopy(component["custom"]["item"])}, "meta": copy.deepcopy(component["meta"]),
		"position": copy.deepcopy(component.get("position", {})), "propConfig": newPropConfig,
		"props": {"params": params, "path": path, "style": style, "useDefaultViewHeight": False,
			"useDefaultViewWidth": False},
		"type": "ia.display.view"}


def _itemKeys(view):
	"""Answer sources without the answer binding: what must not change."""
	keys = []
	for path, item, bindings in design.collectItems(view["root"]):
		other = {k: v for k, v in (json.loads(bindings) if bindings else {}).items() if k != "custom.item.answer"}
		keys.append((path, item, json.dumps(other, sort_keys=True)))
	return keys


def processView(path, apply, backupDir, stats):
	"""Convert one view. Returns (status, detail)."""
	view, usesCrlf, isCanonical = design.loadView(path)
	if not isCanonical:
		return "rechazada", "reescribirla cambiaría bytes (no es Gson canónico)"
	before = copy.deepcopy(view)
	viewStats = collections.Counter()

	def walk(component, parent):
		for i, child in enumerate(component.get("children", [])):
			if "item" in child.get("custom", {}) and child.get("type") in OBJECTS:
				if convertible(child):
					component["children"][i] = convert(child, component, parent, viewStats)
				else:
					viewStats["nativos (respuesta con lógica propia)"] += 1
			else:
				walk(child, component)

	walk(view["root"], None)
	if _itemKeys(before) != _itemKeys(view):
		return "error", "cambió la recolección de respuestas"
	stats.update(viewStats)
	converted = sum(v for k, v in viewStats.items() if k.startswith("Objects/"))
	if not converted:
		return "sin cambios", ""
	if apply:
		target = os.path.join(backupDir, os.path.relpath(path, design.REPO_ROOT))
		os.makedirs(os.path.dirname(target), exist_ok=True)
		if not os.path.exists(target):
			shutil.copy2(path, target)
		design.writeView(path, view, usesCrlf)
	return ("aplicada" if apply else "aplicable"), "{} objetos, {} ítems iguales".format(converted, len(_itemKeys(view)))


def main():
	parser = argparse.ArgumentParser(description="Campos de formularios PAPO como objetos estándar")
	parser.add_argument("--views", nargs="*")
	parser.add_argument("--all-forms", action="store_true")
	parser.add_argument("--apply", action="store_true")
	parser.add_argument("--backup", default=os.path.join(design.REPO_ROOT, ".claude", "backups",
		datetime.date.today().isoformat(), "papo-objects"))
	args = parser.parse_args()

	stats = collections.Counter()
	results = collections.OrderedDict()
	for path in design.resolveViews(args):
		try:
			results[path] = processView(path, args.apply, args.backup, stats)
		except Exception as e:
			results[path] = ("error", str(e))
	byStatus = collections.Counter(s for s, _ in results.values())
	print("papo-objects: {}".format("aplicado" if args.apply else "simulación (no se escribió nada)"))
	print("Vistas: " + ", ".join("{} {}".format(n, s) for s, n in byStatus.most_common()))
	print("Campos: " + ", ".join("{} {}".format(n, k) for k, n in stats.most_common()))
	for path, (status, detail) in results.items():
		if status != "sin cambios":
			print("- {} · {} · {}".format(os.path.relpath(os.path.dirname(path), design.VIEWS_DIR), status, detail))
	return 1 if byStatus.get("error") else 0


if __name__ == "__main__":
	sys.exit(main())
