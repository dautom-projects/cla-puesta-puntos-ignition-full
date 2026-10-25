"""
Component references inside a Perspective view.

Resolves property-binding paths, expression references {...} and script calls
(getChild / getSibling / parent) to the component they point at, so a tool can tell
whether replacing or removing a component breaks something else in the view.

Version: 1.0.0

Changelog:
	2026-10-25 | William M. | v1.0.0 - Initial version

Returns:
	refs(view) -> list of (owner path, target path, remainder); paths are tuples of names
"""

import json
import re

RE_BRACES = re.compile(r"\{([^{}]+)\}")
RE_SCRIPT = re.compile(r"self((?:\.parent)*)((?:\.get(?:Child|Sibling)\(\s*[\"'][^\"']+[\"']\s*\))+)")
RE_STEP = re.compile(r"\.get(Child|Sibling)\(\s*[\"']([^\"']+)[\"']\s*\)")
RE_VIEW_ROOT = re.compile(r"self\.view\.getChild\(\s*[\"']root[\"']\s*\)((?:\.getChild\(\s*[\"'][^\"']+[\"']\s*\))*)")
NON_COMPONENT = ("view.", "session.", "page.", "[")


def index(view):
	"""Map component path -> node."""
	nodes = {}

	def walk(node, path):
		nodes[path] = node
		for child in node.get("children", []):
			walk(child, path + (child.get("meta", {}).get("name", "?"),))
	walk(view["root"], ("root",))
	return nodes


def resolve(owner, ref):
	"""Return (target path, remainder) for a component reference from owner, or None."""
	ref = ref.strip()
	if not ref or ref.startswith(NON_COMPONENT):
		return None
	if ref.startswith("this."):
		return owner, ref[5:]
	if ref.startswith("parent."):
		return owner[:-1], ref[7:]
	if ref.startswith("/"):
		base, tail = (), ref[1:]
	else:
		match = re.match(r"^(\.+)/(.*)$", ref)
		if not match:
			return None
		up = len(match.group(1)) - 1
		base, tail = (owner[:len(owner) - up] if up else owner), match.group(2)
	segments = tail.split("/")
	last, _, rest = segments[-1].partition(".")
	return base + tuple(x for x in segments[:-1] if x) + (last,), rest


def _strings(value):
	if isinstance(value, str):
		yield value
	elif isinstance(value, dict):
		for v in value.values():
			for s in _strings(v):
				yield s
	elif isinstance(value, list):
		for v in value:
			for s in _strings(v):
				yield s


def _scriptRefs(owner, code):
	out = []
	for match in RE_SCRIPT.finditer(code or ""):
		path = owner[:len(owner) - match.group(1).count(".parent")]
		for kind, name in RE_STEP.findall(match.group(2)):
			path = (path + (name,)) if kind == "Child" else (path[:-1] + (name,))
		out.append((path, "script"))
	for match in RE_VIEW_ROOT.finditer(code or ""):
		out.append((("root",) + tuple(n for _, n in RE_STEP.findall(match.group(1))), "script"))
	return out


def refs(view):
	"""All component references of the view: (owner, target, remainder)."""
	out = []
	for owner, node in index(view).items():
		for key, cfg in (node.get("propConfig") or {}).items():
			binding = cfg.get("binding") or {}
			config = binding.get("config") or {}
			if binding.get("type") == "property" and config.get("path"):
				r = resolve(owner, config["path"])
				if r:
					out.append((owner, r[0], r[1]))
			for text in _strings({k: v for k, v in config.items() if k != "path"}):
				for ref in RE_BRACES.findall(text):
					r = resolve(owner, ref)
					if r:
						out.append((owner, r[0], r[1]))
			for t in binding.get("transforms", []):
				for target, rest in _scriptRefs(owner, t.get("code")):
					out.append((owner, target, rest))
				if t.get("expression"):
					for ref in RE_BRACES.findall(t["expression"]):
						r = resolve(owner, ref)
						if r:
							out.append((owner, r[0], r[1]))
			if cfg.get("onChange"):
				for target, rest in _scriptRefs(owner, cfg["onChange"].get("script")):
					out.append((owner, target, rest))
		scripts = [e.get("config", {}).get("script") for evs in (node.get("events") or {}).values() if isinstance(evs, dict)
			for e in (evs.values() if isinstance(evs, dict) else []) if isinstance(e, dict)]
		scripts += [m.get("script") for m in (node.get("scripts") or {}).get("customMethods", [])]
		scripts += [m.get("script") for m in (node.get("scripts") or {}).get("messageHandlers", [])]
		for code in scripts:
			for target, rest in _scriptRefs(owner, code):
				out.append((owner, target, rest))
	return out


def broken(view):
	"""References whose target component does not exist."""
	nodes = index(view)
	return {(o, t, r) for o, t, r in refs(view) if t not in nodes}
