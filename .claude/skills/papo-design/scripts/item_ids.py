"""
Runtime papoItemID of every answer source of a PAPO form, computed from the view JSON.

Many forms compute custom.item.papoItemID at runtime (basePapo + an index taken from the component name,
a parent custom.papoItemID, a sibling label...). This module evaluates those bindings the way Perspective
does: property paths (this., parent., ../, /root/), expression structures and expressions with {refs},
and script transforms run with a stand-in for self (meta, parent, custom, props, view, getChild, getSibling).
The standard keeps the resulting ID fixed in custom.item (one logic for every form).

Version: 1.0.0

Changelog:
	2026-10-26 | William M. | v1.0.0 - Initial version

Returns:
	resolve(view) -> {component path tuple: papoItemID or None (not computable)}
"""

import json
import re

import view_refs


class Unresolved(Exception):
	pass


class _Bag(object):
	"""Attribute access over a property group (custom, props, meta, params) of a component."""

	def __init__(self, evaluator, path, group):
		self._e, self._path, self._group = evaluator, path, group

	def __getattr__(self, name):
		if name.startswith("_"):
			raise AttributeError(name)
		return self._e.value(self._path, self._group + "." + name)

	def get(self, name, default=None):
		try:
			value = self.__getattr__(name)
		except (Unresolved, AttributeError):
			return default
		return default if value is None else value


class _Component(object):
	"""Stand-in for a Perspective component inside a script transform."""

	def __init__(self, evaluator, path):
		self._e, self._path = evaluator, path
		self.meta = _Bag(evaluator, path, "meta")
		self.custom = _Bag(evaluator, path, "custom")
		self.props = _Bag(evaluator, path, "props")
		self.view = _View(evaluator)

	@property
	def parent(self):
		if len(self._path) <= 1:
			raise Unresolved("sin parent")
		return _Component(self._e, self._path[:-1])

	def getChild(self, name):
		path = self._path + (name,)
		if path not in self._e.nodes:
			raise Unresolved("no existe " + "/".join(path))
		return _Component(self._e, path)

	def getSibling(self, name):
		return _Component(self._e, self._path[:-1]).getChild(name)


class _View(object):
	def __init__(self, evaluator):
		self.custom = _ViewBag(evaluator, "custom")
		self.params = _ViewBag(evaluator, "params")

	def getChild(self, name):
		raise Unresolved("view.getChild")


class _ViewBag(object):
	def __init__(self, evaluator, group):
		self._e, self._group = evaluator, group

	def __getattr__(self, name):
		if name.startswith("_"):
			raise AttributeError(name)
		if self._group + "." + name in self._e.view.get("propConfig", {}):
			raise Unresolved("view.{}.{} con binding".format(self._group, name))
		return (self._e.view.get(self._group) or {}).get(name)


class _Logger(object):
	def __getattr__(self, name):
		return lambda *args, **kwargs: None


class _System(object):
	"""Only system.util.getLogger exists inside the transforms that are evaluated."""

	class util(object):
		@staticmethod
		def getLogger(name):
			return _Logger()


def _python3(code):
	"""Jython 2 script body as a Python 3 function body (print statements, except ..., e)."""
	code = re.sub(r"^(\s*)print\s+(?!\()(.*)$", r"\1pass", code, flags=re.M)
	code = re.sub(r"except\s+([\w.]+)\s*,\s*(\w+)\s*:", r"except \1 as \2:", code)
	return code.expandtabs(4)


class Evaluator(object):
	def __init__(self, view):
		self.view = view
		self.nodes = view_refs.index(view)
		self._stack = set()

	def _static(self, path, prop):
		value = self.nodes[path]
		for part in prop.split("."):
			if part == "meta" and isinstance(value, dict) and "meta" not in value:
				return None
			value = value.get(part) if isinstance(value, dict) else None
		return value

	def value(self, path, prop):
		"""Value of a component property: its binding when it has one, else the stored value."""
		if path not in self.nodes:
			raise Unresolved("no existe " + "/".join(path))
		node = self.nodes[path]
		propConfig = node.get("propConfig", {})
		key = (path, prop)
		if key in self._stack:
			raise Unresolved("binding circular")
		# The binding can be on the property itself or on a parent object (custom.item -> custom.item.papoItemID)
		parts = prop.split(".")
		for i in range(len(parts), 0, -1):
			owner = ".".join(parts[:i])
			binding = (propConfig.get(owner) or {}).get("binding")
			# A disabled binding does not run: the stored value stays
			if binding and binding.get("enabled") is not False:
				self._stack.add(key)
				try:
					value = self.binding(path, binding)
				finally:
					self._stack.discard(key)
				for part in parts[i:]:
					value = value.get(part) if isinstance(value, dict) else None
				return value
		return self._static(path, prop)

	def reference(self, owner, ref):
		if ref.startswith("view."):
			group, _, name = ref[5:].partition(".")
			if "{}.{}".format(group, name.split(".")[0]) in self.view.get("propConfig", {}):
				raise Unresolved(ref + " con binding")
			value = self.view.get(group) or {}
			for part in name.split("."):
				value = value.get(part) if isinstance(value, dict) else None
			return value
		resolved = view_refs.resolve(owner, ref)
		if not resolved:
			raise Unresolved("referencia " + ref)
		target, rest = resolved
		if not rest:
			raise Unresolved("referencia a un componente completo: " + ref)
		return self.value(target, rest)

	def expression(self, owner, text):
		"""A {ref} or a simple arithmetic expression of {refs} and numbers."""
		refs = re.findall(r"\{([^{}]+)\}", text)
		if text.strip() == "{" + (refs[0] if refs else "") + "}" and refs:
			return self.reference(owner, refs[0])
		code = text
		for ref in refs:
			code = code.replace("{" + ref + "}", repr(self.reference(owner, ref)))
		# Only numbers, strings and arithmetic (no names or calls)
		bare = re.sub(r"'(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\"|None|True|False", "0", code)
		if not re.fullmatch(r"[\d\s+\-*/().]*", bare):
			raise Unresolved("expresión " + text[:60])
		return eval(code, {"__builtins__": {}}, {})

	def binding(self, owner, binding):
		kind = binding.get("type")
		config = binding.get("config", {})
		if kind == "property":
			value = self.reference(owner, config.get("path", ""))
		elif kind == "expr-struct":
			value = {k: self.expression(owner, e) for k, e in (config.get("struct") or {}).items()}
		elif kind == "expr":
			value = self.expression(owner, config.get("expression", ""))
		else:
			raise Unresolved("binding " + str(kind))
		for transform in binding.get("transforms", []):
			value = self.transform(owner, transform, value)
		return value

	def transform(self, owner, transform, value):
		kind = transform.get("type")
		if kind == "script":
			code = transform.get("code") or ""
			# Only pure scripts: a logger is allowed, the database, tags or other system calls are not
			if re.search(r"system\.(?!util\.getLogger)|runPrep|runNamed|import\s+(?!re\b)", code):
				raise Unresolved("script con sistema o base de datos")
			source = "def _t(self, value):\n" + "\n".join("    " + line for line in _python3(code).splitlines()) + "\n"
			scope = {"re": re, "system": _System(), "__builtins__": __builtins__}
			try:
				exec(compile(source, "<transform>", "exec"), scope)
				return scope["_t"](_Component(self, owner), value)
			except Unresolved:
				raise
			except Exception as e:
				raise Unresolved("script: {}: {}".format(type(e).__name__, e))
		if kind == "map":
			for m in transform.get("mappings", []):
				if m.get("input") == value:
					return m.get("output")
			return transform.get("fallback")
		if kind == "expression":
			return self.expression(owner, transform.get("expression", "").replace("{value}", repr(value)))
		raise Unresolved("transform " + str(kind))


def resolve(view):
	"""{component path: runtime papoItemID or None} for every component with a custom.item."""
	evaluator = Evaluator(view)
	out = {}
	for path, node in evaluator.nodes.items():
		if "item" not in (node.get("custom") or {}):
			continue
		try:
			value = evaluator.value(path, "custom.item.papoItemID")
			out[path] = int(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else value
		except Unresolved as e:
			out[path] = None
			evaluator.lastError = str(e)
	return out


def explain(view, path):
	"""Why one papoItemID cannot be computed (for reports)."""
	try:
		return Evaluator(view).value(path, "custom.item.papoItemID")
	except Unresolved as e:
		return "no calculable: " + str(e)
