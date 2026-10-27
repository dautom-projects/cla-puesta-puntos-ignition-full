"""
Out-of-range color of a native numeric field, worked out by running its own color script.

The original forms paint a numeric field red with a script transform on custom.color / custom.borderColor or
on props.style.color / borderColor (several shapes: rang_down..rang_up, start +/- rang, start * (1 +/- porc),
only a lower bound, papo_core.items.getRangeColor with fixed bounds). Objects/NumericField paints with
papo_core.items.getRangeColor(value, minValue, maxValue): red outside a closed range, never red when a bound is
missing. rangeOf() gives the closed range that paints exactly like the original, or UNSUPPORTED when no closed
range does (the field then stays native).

The scripts run as Jython 2 does: a number is always less than a text, so rang_up = "9999999999999999999999999"
(the forms' own way to say "no upper bound") is a closed range up to that number. A field valid only above a
minimum gets the same upper bound (NO_UPPER). A script that reads a custom property the field does not have fails
in Ignition and never paints the field: it has no range.

Version: 1.1.0

Changelog:
	2026-10-26 | William M. | v1.0.0 - Initial version
	2026-10-27 | William M. | v1.1.0 - Jython 2 comparisons (number < text), bounds computed by the script
		(minimo / maximo and the like), only a lower bound (upper bound NO_UPPER), getRangeColor with fixed bounds
		on custom.item.answer, and scripts that fail on a missing custom property (never red, no range)

Returns:
	rangeOf(component) -> None (no color logic or never red), (minValue, maxValue) or UNSUPPORTED
	isRed(component, value) -> True / False / None (no color logic or the script cannot run here)
	objectRed(minValue, maxValue, value) -> True / False, as getRangeColor does
"""

import itertools
import json
import re

import item_ids

UNSUPPORTED = "no reproducible"
COLOR_ERROR = "#F70808"
COLOR_PROPS = ("custom.color", "custom.borderColor", "props.style.color", "props.style.borderColor")
# Upper bound of a range that only has a minimum: the value the forms already use for "no upper bound"
NO_UPPER = "9999999999999999999999999"
VALUE_PATHS = ("this.props.value", "this.custom.item.answer")


class _Missing(AttributeError):
	"""A script read a custom property the component does not have (the binding fails in Ignition)."""


class _Py2Str(str):
	"""A text that compares like Jython 2: greater than any number."""
	def _other(self, other):
		return isinstance(other, (int, float)) and not isinstance(other, bool)

	def __lt__(self, other):
		return False if self._other(other) else str.__lt__(self, other)

	def __le__(self, other):
		return False if self._other(other) else str.__le__(self, other)

	def __gt__(self, other):
		return True if self._other(other) else str.__gt__(self, other)

	def __ge__(self, other):
		return True if self._other(other) else str.__ge__(self, other)

	__hash__ = str.__hash__


class _Bag(object):
	def __init__(self, values):
		self.__dict__.update({k: _Py2Str(v) if isinstance(v, str) else v for k, v in (values or {}).items()})

	def __getattr__(self, name):
		raise _Missing(name)

	def get(self, name, default=None):
		return self.__dict__.get(name, default)


class _Self(object):
	def __init__(self, component):
		self.custom = _Bag(component.get("custom"))
		self.props = _Bag(component.get("props"))


class _Items(object):
	@staticmethod
	def getRangeColor(value, minValue, maxValue, colorType="border"):
		return COLOR_ERROR if objectRed(minValue, maxValue, value) else "#C0C0C0"


class _PapoCore(object):
	items = _Items()


def _answerIsValue(component):
	"""custom.item.answer is the field value as it is (so a color bound to the answer reads the value)."""
	binding = (component.get("propConfig", {}).get("custom.item.answer") or {}).get("binding") or {}
	return (binding.get("config") or {}).get("path") == "this.props.value" and not binding.get("transforms")


def _valueBinding(component, binding):
	path = (binding.get("config") or {}).get("path", "")
	transforms = binding.get("transforms") or []
	if len(transforms) != 1 or transforms[0].get("type") != "script":
		return False
	return path == "this.props.value" or (path == "this.custom.item.answer" and _answerIsValue(component))


def colorScripts(component):
	"""Script transforms that compute a color from the field value."""
	out = []
	for prop in COLOR_PROPS:
		binding = (component.get("propConfig", {}).get(prop) or {}).get("binding") or {}
		if _valueBinding(component, binding):
			out.append(binding["transforms"][0].get("code") or "")
	return out


def _source(code, tail=""):
	return "def _t(self, value):\n" + "\n".join("    " + line for line in item_ids._python3(code).splitlines()) + "\n" + tail


def _run(code, component, value):
	scope = {"__builtins__": __builtins__, "papo_core": _PapoCore()}
	exec(compile(_source(code), "<color>", "exec"), scope)
	return scope["_t"](_Self(component), value)


def isRed(component, value):
	scripts = colorScripts(component)
	if not scripts:
		return None
	try:
		return any(str(_run(code, component, value)).upper() == COLOR_ERROR for code in scripts)
	except _Missing:
		# The binding fails in Ignition: the color is never set, so the field is never red
		return False
	except Exception:
		return None


def _number(bound):
	return float(bound) if isinstance(bound, str) else bound


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
	base = set(_numbers(component)) | {_number(x) for x in extra} | {0.0, 7.0, -1.0, 1e6}
	if isinstance(custom.get("start"), (int, float)) and isinstance(custom.get("rang"), (int, float)):
		base |= {custom["start"] - custom["rang"], custom["start"] + custom["rang"]}
	out = set()
	for n in base:
		out |= {n, round(n - 0.01, 6), round(n + 0.01, 6), n - 1, n + 1}
	return sorted(out)


def _scriptBounds(code, component):
	"""Numbers the script computes before it looks at the value (minimo, maximo, inicio...), in order."""
	lines = item_ids._python3(code).splitlines()
	cut = next((i for i, line in enumerate(lines) if re.match(r"\s*if\b.*\bvalue\b", line)), len(lines))
	body = [line for line in lines[:cut] if line.strip() and not line.strip().startswith("return")]
	if not body:
		return []
	indent = re.match(r"\s*", body[0]).group(0)
	source = "def _t(self, value):\n" + "\n".join("    " + line for line in body) + "\n    " + indent + "return dict(locals())\n"
	scope = {"__builtins__": __builtins__, "papo_core": _PapoCore()}
	try:
		exec(compile(source, "<bounds>", "exec"), scope)
		found = scope["_t"](_Self(component), 0)
	except Exception:
		return []
	if not isinstance(found, dict):
		return []
	out = []
	for name, value in found.items():
		if name in ("self", "value"):
			continue
		if isinstance(value, bool):
			continue
		if isinstance(value, (int, float)):
			out.append((name, round(value, 6) if isinstance(value, float) else value))
		elif isinstance(value, str) and re.match(r"^-?\d+(\.\d+)?$", value):
			out.append((name, str(value)))
	return out


def _candidates(component):
	custom = component.get("custom") or {}
	out = []
	if "rang_down" in custom and "rang_up" in custom:
		out.append((custom["rang_down"], custom["rang_up"]))
	if isinstance(custom.get("start"), (int, float)) and isinstance(custom.get("rang"), (int, float)):
		out.append((round(custom["start"] - custom["rang"], 6), round(custom["start"] + custom["rang"], 6)))
	numbers = []
	for code in colorScripts(component):
		for low, high in re.findall(r"(-?[\d.]+)\s*<=\s*value\s*<=\s*(-?[\d.]+)", code):
			out.append((float(low) if "." in low else int(low), float(high) if "." in high else int(high)))
		for low, high in re.findall(r"getRangeColor\(\s*value\s*,\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)", code):
			out.append((float(low) if "." in low else int(low), float(high) if "." in high else int(high)))
		bounds = dict(_scriptBounds(code, component))
		if "minimo" in bounds and "maximo" in bounds:
			out.append((bounds["minimo"], bounds["maximo"]))
		numbers += [v for _, v in sorted(bounds.items())]
	numbers += [v for k, v in sorted(custom.items()) if k != "item" and (isinstance(v, (int, float)) and not isinstance(v, bool))]
	# Any pair of the numbers the field uses, then a range with only a minimum (upper bound NO_UPPER)
	unique = sorted({_number(n) for n in numbers if _number(n) is not None}, key=float)
	out += [(a, b) for a, b in itertools.combinations(unique, 2)]
	out += [(n, NO_UPPER) for n in unique if float(n) < float(NO_UPPER)]
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
		if _valueBinding(component, binding):
			continue
		return True
	return False


def rangeOf(component):
	if _otherColorBindings(component):
		return UNSUPPORTED
	if not colorScripts(component):
		return None
	candidates = _candidates(component)
	values = probes(component, [b for pair in candidates for b in pair if not (isinstance(b, str) and b == NO_UPPER)])
	reds = [isRed(component, v) for v in values]
	if None in reds:
		return UNSUPPORTED
	if not any(reds):
		# Never red (e.g. the script reads a custom property the field does not have): no range
		return None
	for low, high in candidates:
		if all(red is objectRed(low, high, v) for red, v in zip(reds, values)):
			return low, high
	return UNSUPPORTED
