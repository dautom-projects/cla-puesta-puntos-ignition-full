"""
PAPO design standard tool for Perspective Form views.

Applies the standard style classes (PAPO/Field/*) to the components that hold
custom.item, to the Observaciones TextField, and maps title colors to theme
tokens. Only props.style and props.textStyle change; custom.item, every
binding (propConfig), the component tree and the order of components stay
identical, so papo_core.register.recopile collects the same items in the same
order (SAT "Procedimiento de estandarizacion v2"). Dry run by default.

Version: 1.0.0

Changelog:
	2026-10-24 | William M. | v1.0.0 - Initial version (EA11-0901_1h pilot)

Args (CLI):
	--views (str...): View folders or view.json paths
	--all-forms: Every Form_* view of the project
	--apply: Write the changes (default: dry run, nothing is written)
	--backup (str): Backup folder for --apply. Default: <repo>/.claude/backups/<date>/papo-design
	--report (str): Optional Markdown report path

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
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
VIEWS_DIR = os.path.join(REPO_ROOT, "cla-project", "com.inductiveautomation.perspective", "views")
STYLES_DIR = os.path.join(REPO_ROOT, "cla-project", "com.inductiveautomation.perspective", "style-classes")
RULES = json.load(open(os.path.join(os.path.dirname(__file__), "rules.json"), encoding="utf-8"))

GSON_ESCAPES = (("=", "\\u003d"), ("<", "\\u003c"), (">", "\\u003e"), ("&", "\\u0026"), ("'", "\\u0027"))

# Paths that may change: the static style of a component
ALLOWED_DIFF = re.compile(r"\.props\.(style|textStyle)(\.|\[|$)")


# ==================== SERIALIZATION ====================

def gsonDump(obj):
	"""Serialize like the Ignition Designer (Gson: sorted keys, 2 spaces, HTML escapes)."""
	out = json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False)
	for char, escaped in GSON_ESCAPES:
		out = out.replace(char, escaped)
	return out


def loadView(path):
	"""Return (view, usesCrlf, isCanonical). isCanonical is False when rewriting would change bytes."""
	raw = open(path, encoding="utf-8", newline="").read()
	usesCrlf = "\r\n" in raw
	view = json.loads(raw)
	isCanonical = gsonDump(view) == (raw.replace("\r\n", "\n") if usesCrlf else raw)
	return view, usesCrlf, isCanonical


def writeView(path, view, usesCrlf):
	"""Write the view keeping its original line endings."""
	out = gsonDump(view)
	if usesCrlf:
		out = out.replace("\n", "\r\n")
	open(path, "w", encoding="utf-8", newline="").write(out)


# ==================== VERIFICATION ====================

def collectItems(component, path="root"):
	"""
	List the answer sources in the order papo_core.register._gatherItems visits them:
	custom.item (static part and its bindings), then Flex Repeater instances, then children.
	"""
	found = []
	custom = component.get("custom", {})
	if "item" in custom:
		bindings = {k: v for k, v in component.get("propConfig", {}).items() if k.startswith("custom.item")}
		found.append((path, json.dumps(custom["item"], sort_keys=True), json.dumps(bindings, sort_keys=True)))
	instances = component.get("props", {}).get("instances")
	if instances is not None:
		found.append((path + "#instances", json.dumps(instances, sort_keys=True), ""))
		return found
	for child in component.get("children", []):
		found.extend(collectItems(child, path + "/" + child.get("meta", {}).get("name", "?")))
	return found


def diffPaths(before, after, path=""):
	"""Return the JSON paths that differ between two values."""
	if isinstance(before, dict) and isinstance(after, dict):
		out = []
		for key in sorted(set(before) | set(after)):
			# A dict added on one side (e.g. props created to hold style) is compared against {}
			left = before.get(key, {} if isinstance(after.get(key), dict) else None)
			right = after.get(key, {} if isinstance(before.get(key), dict) else None)
			if key not in before and not isinstance(right, dict) or key not in after and not isinstance(left, dict):
				out.append(path + "." + key)
			else:
				out.extend(diffPaths(left, right, path + "." + key))
		return out
	if isinstance(before, list) and isinstance(after, list) and len(before) == len(after):
		out = []
		for i, (x, y) in enumerate(zip(before, after)):
			out.extend(diffPaths(x, y, "{}[{}]".format(path, i)))
		return out
	return [] if before == after else [path]


# ==================== RULES ====================

def _sameValue(value, allowed):
	"""True when value is one of the allowed values (numbers and strings compared as given)."""
	return any(value == a and type(value) == type(a) for a in allowed)


def _applyClass(component, targetClass, stats, role):
	"""Point the component style at targetClass and drop the inline keys the class already defines."""
	if "props.style.classes" in component.get("propConfig", {}):
		stats["skip: clases con binding"][role] += 1
		return False

	props = component.setdefault("props", {})
	style = dict(props.get("style") or {})
	tokens = str(style.get("classes", "")).split()
	if targetClass in tokens:
		stats["ya estándar"][role] += 1
		return False

	# Old classes are replaced; the layout they carried stays inline
	kept = []
	for token in tokens:
		if token in RULES["replacedClasses"]:
			for key, value in RULES["replacedClasses"][token].items():
				style.setdefault(key, value)
		else:
			kept.append(token)

	covered = RULES["covered"][targetClass]
	propConfig = component.get("propConfig", {})
	for key in list(style):
		if key == "classes":
			continue
		if key in covered and _sameValue(style[key], covered[key]):
			del style[key]
		elif "props.style." + key in propConfig:
			# Static value that its own binding overwrites at runtime
			del style[key]
			stats["estático pisado por binding"]["{} {}".format(role, key)] += 1

	style["classes"] = " ".join(kept + [targetClass])
	for key in style:
		if key != "classes":
			stats["inline que queda"]["{} {}".format(role, key)] += 1
	props["style"] = style
	stats["estandarizados"][role] += 1
	return True


def _applyTitle(component, stats):
	"""Map literal title colors to theme tokens (same color, now themable)."""
	textStyle = component.get("props", {}).get("textStyle") or {}
	changed = False
	for key, mapping in RULES["titles"]["textStyleValues"].items():
		if key in textStyle and textStyle[key] in mapping and "props.textStyle." + key not in component.get("propConfig", {}):
			textStyle[key] = mapping[textStyle[key]]
			changed = True
	if changed:
		stats["estandarizados"]["title"] += 1
	return changed


def standardize(root, stats):
	"""Apply the design rules to every component of the view tree."""
	insights = RULES["insightsField"]

	def walk(component, isRootChild):
		ctype = component.get("type", "")
		name = component.get("meta", {}).get("name", "")
		custom = component.get("custom", {})
		if "item" in custom and ctype in RULES["fieldClasses"]:
			_applyClass(component, RULES["fieldClasses"][ctype], stats, ctype.split(".")[-1])
		elif isRootChild and ctype == insights["type"] and name == insights["name"]:
			_applyClass(component, insights["class"], stats, "observaciones")
		elif ctype == "ia.display.label" and RULES["titles"]["class"] in str((component.get("props", {}).get("style") or {}).get("classes", "")).split():
			_applyTitle(component, stats)
		for child in component.get("children", []):
			walk(child, component is root)

	walk(root, False)


# ==================== MAIN ====================

def processView(path, apply, backupDir, stats):
	"""Standardize one view. Returns (status, detail)."""
	view, usesCrlf, isCanonical = loadView(path)
	if not isCanonical:
		return "rechazada", "reescribirla cambiaría bytes fuera del estilo (no es Gson canónico)"

	before = copy.deepcopy(view)
	viewStats = collections.defaultdict(collections.Counter)
	standardize(view["root"], viewStats)

	# Answer collection must be identical: same items, same bindings, same order
	if collectItems(before["root"]) != collectItems(view["root"]):
		return "error", "cambió la recolección de respuestas"
	outside = [p for p in diffPaths(before, view) if not ALLOWED_DIFF.search(p)]
	if outside:
		return "error", "cambios fuera de props.style/textStyle: {}".format(outside[:3])

	for group, counter in viewStats.items():
		stats[group].update(counter)
	changed = sum(viewStats["estandarizados"].values())
	items = len(collectItems(view["root"]))
	if not changed:
		return "sin cambios", "{} ítems".format(items)

	if apply:
		rel = os.path.relpath(path, REPO_ROOT)
		target = os.path.join(backupDir, rel)
		os.makedirs(os.path.dirname(target), exist_ok=True)
		if not os.path.exists(target):
			shutil.copy2(path, target)
		writeView(path, view, usesCrlf)
		reread, _, _ = loadView(path)
		if collectItems(reread["root"]) != collectItems(before["root"]):
			shutil.copy2(target, path)
			return "error", "verificación tras escribir falló; restaurado el backup"
	detail = ", ".join("{} {}".format(v, k) for k, v in sorted(viewStats["estandarizados"].items()))
	return ("aplicada" if apply else "aplicable"), "{} ({} ítems iguales)".format(detail, items)


def resolveViews(args):
	"""Return the view.json paths selected by the CLI arguments."""
	paths = []
	if args.all_forms:
		paths = [p for p in glob.glob(os.path.join(VIEWS_DIR, "**", "view.json"), recursive=True)
			if os.path.basename(os.path.dirname(p)).startswith("Form_")]
	for item in args.views or []:
		candidate = item if os.path.isabs(item) else os.path.join(REPO_ROOT, item)
		if not os.path.exists(candidate):
			candidate = os.path.join(VIEWS_DIR, item)
		if os.path.isdir(candidate):
			candidate = os.path.join(candidate, "view.json")
		paths.append(os.path.abspath(candidate))
	return sorted(set(paths))


def missingClasses():
	"""Return the standard classes used by the rules that do not exist in style-classes."""
	used = set(RULES["fieldClasses"].values()) | {RULES["insightsField"]["class"]}
	return sorted(c for c in used if not os.path.exists(os.path.join(STYLES_DIR, c, "style.json")))


def main():
	parser = argparse.ArgumentParser(description="Estándar de diseño PAPO para vistas Form_*")
	parser.add_argument("--views", nargs="*")
	parser.add_argument("--all-forms", action="store_true")
	parser.add_argument("--apply", action="store_true")
	parser.add_argument("--backup", default=os.path.join(REPO_ROOT, ".claude", "backups",
		datetime.date.today().isoformat(), "papo-design"))
	parser.add_argument("--report")
	args = parser.parse_args()

	missing = missingClasses()
	if missing:
		print("Faltan clases de estilo: {}".format(", ".join(missing)))
		return 1

	paths = resolveViews(args)
	stats = collections.defaultdict(collections.Counter)
	results = collections.OrderedDict()
	for path in paths:
		try:
			results[path] = processView(path, args.apply, args.backup, stats)
		except Exception as e:
			results[path] = ("error", str(e))

	lines = ["# papo-design: {}".format("aplicado" if args.apply else "simulación (no se escribió nada)"), "",
		"Generado: {} · Vistas: {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), len(paths)), ""]
	byStatus = collections.Counter(s for s, _ in results.values())
	lines.append("| Estado | Vistas |\n|---|:-:|")
	lines.extend("| {} | {} |".format(s, n) for s, n in byStatus.most_common())
	for group in ("estandarizados", "ya estándar", "skip: clases con binding", "estático pisado por binding", "inline que queda"):
		if stats[group]:
			lines.extend(["", "## {}".format(group.capitalize()), "", "| Rol / clave | Componentes |", "|---|:-:|"])
			lines.extend("| {} | {} |".format(k, v) for k, v in stats[group].most_common())
	lines.extend(["", "## Detalle por vista", ""])
	for path, (status, detail) in results.items():
		lines.append("- `{}` · {} · {}".format(os.path.relpath(os.path.dirname(path), VIEWS_DIR), status, detail))
	report = "\n".join(lines) + "\n"

	if args.report:
		open(args.report, "w", encoding="utf-8").write(report)
		print("Reporte: {}".format(args.report))
		print("\n".join(lines[:4 + len(byStatus) + 1]))
	else:
		print(report)
	return 1 if byStatus.get("error") else 0


if __name__ == "__main__":
	sys.exit(main())
