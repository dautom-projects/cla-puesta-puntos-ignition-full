"""
Out-of-range color of a native numeric field, worked out by running its own color script.

The original forms paint a numeric field red with a script transform on custom.color / custom.borderColor or
on props.style.color / borderColor (several shapes: rang_down..rang_up, start +/- rang, only a lower bound).
Objects/NumericField paints with papo_core.items.getRangeColor(value, minValue, maxValue): red outside a closed
range, never red when a bound is missing. rangeOf() gives the closed range that paints exactly like the
original, or UNSUPPORTED when no closed range does (the field then stays native).

Version: 1.0.0

Changelog:
	2026-10-26 | William M. | v1.0.0 - Initial version

Returns:
	rangeOf(component) -> None (no color logic), (minValue, maxValue) or UNSUPPORTED
	isRed(component, value) -> True / False / None (no color logic or the script cannot run here)
	objectRed(minValue, maxValue, value) -> True / False, as getRangeColor does
"""

import json
import re

import item_ids

UNSUPPORTED = "no reproducible"
COLOR_ERROR = "#F70808"
COLOR_PROPS = ("custom.color", "custom.borderColor", "props.style.color", "props.style.borderColor")


class _Bag(object):
	def __init__(self, values):
		self.__dict__.update(values or {})

	def get(self, name, default=None):
		return self.__dict__.get(name, default)


class _Self(object):
	def __init__(self, component):
		self.custom = _Bag(component.get("custom"))
		self.props = _Bag(component.get("props"))


def colorScripts(component):
	"""Script transforms that compute a color from the field value."""
	out = []
	for prop in COLOR_PROPS:
		binding = (component.get("propConfig", {}).get(prop) or {}).get("binding") or {}
		path = (binding.get("config") or {}).get("path", "")
		transforms = binding.get("transforms") or []
		if path == "this.props.value" and len(transforms) == 1 and transforms[0].get("type") == "script":
			out.append(transforms[0].get("code") or "")
	return out


def _run(code, component, value):
	source = "def _t(self, value):\n" + "\n".join("    " + line for line in item_ids._python3(code).splitlines()) + "\n"
	scope = {"__builtins__": __builtins__}
	exec(compile(source, "<color>", "exec"), scope)
	return scope["_t"](_Self(component), value)


def isRed(component, value):
	scripts = colorScripts(component)
	if not scripts:
		return None
	try:
		return any(str(_run(code, component, value)).upper() == COLOR_ERROR for code in scripts)
	except Exception:
		return None


def objectRed(minValue, maxValue, value):
	if value is None or value == "" or minValue is None or maxValue is None:
		return False
	return not (float(minValue) <= float(value) <= float(maxValue))


def _numbers(component):
	text = json.dumps(component.get("custom") or {}) + " ".join(colorScripts(component))
	return {float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", text)}


def probes(component, extra=()):
	"""Values around every number of the field (custom values, bounds in its scripts) plus a few far ones."""
	custom = component.get("custom") or {}
	base = set(_numbers(component)) | set(extra) | {0.0, 7.0, -1.0, 1e6}
	if isinstance(custom.get("start"), (int, float)) and isinstance(custom.get("rang"), (int, float)):
		base |= {custom["start"] - custom["rang"], custom["start"] + custom["rang"]}
	out = set()
	for n in base:
		out |= {n, round(n - 0.01, 6), round(n + 0.01, 6), n - 1, n + 1}
	return sorted(out)


def _candidates(component):
	custom = component.get("custom") or {}
	out = []
	if "rang_down" in custom and "rang_up" in custom:
		out.append((custom["rang_down"], custom["rang_up"]))
	if isinstance(custom.get("start"), (int, float)) and isinstance(custom.get("rang"), (int, float)):
		out.append((round(custom["start"] - custom["rang"], 6), round(custom["start"] + custom["rang"], 6)))
	for code in colorScripts(component):
		for low, high in re.findall(r"(-?[\d.]+)\s*<=\s*value\s*<=\s*(-?[\d.]+)", code):
			out.append((float(low) if "." in low else int(low), float(high) if "." in high else int(high)))
	return out


def _otherColorBindings(component):
	"""A color binding that is neither a value script nor a link to custom.color / custom.borderColor."""
	for prop in COLOR_PROPS:
		binding = (component.get("propConfig", {}).get(prop) or {}).get("binding")
		if not binding:
			continue
		path = (binding.get("config") or {}).get("path", "")
		transforms = binding.get("transforms") or []
		if path in ("this.custom.color", "this.custom.borderColor") and not transforms:
			continue
		if path == "this.props.value" and len(transforms) == 1 and transforms[0].get("type") == "script":
			continue
		return True
	return False


def rangeOf(component):
	if _otherColorBindings(component):
		return UNSUPPORTED
	if not colorScripts(component):
		return None
	values = probes(component)
	for low, high in _candidates(component):
		if all(isRed(component, v) is objectRed(low, high, v) for v in values):
			return low, high
	return UNSUPPORTED
