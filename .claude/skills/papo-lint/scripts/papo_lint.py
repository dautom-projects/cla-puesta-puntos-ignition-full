"""
Read-only linter for PAPO Perspective views.

Walks the view.json files of cla-project and reports, per view, the patterns
that break the PAPO conventions (hardcoded connection, shift by getHour24,
last RegisterCode ordered by Timestamp, project.papo_core prefix, legacy
view.custom keys and missing papo_core wrappers in Form_* views). Writes a
Markdown report with a summary per pattern and the detail per view.

Version: 1.0.0

Changelog:
	2026-10-22 | William M. | v1.0.0 - Initial version

Args (CLI):
	--project (str): Ignition project folder. Default: <repo>/cla-project
	--out (str): Markdown report path. Default: <repo>/.claude/docs/LINT_REPORT.md
	--views (str...): Optional view paths (folder or view.json) to lint only those
	--stdout: Print the report instead of writing it

Returns:
	Exit code 0 always (report-only tool)
"""

import argparse
import collections
import datetime
import json
import os
import re
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
VIEWS_REL = os.path.join("com.inductiveautomation.perspective", "views")

LEGACY_KEYS = ("answers", "formato", "test", "flexGroupCount", "flexCount", "refreshSecond",
	"dsTable_v3", "dsTable_vJ", "changedRegister", "viewOn")

# Keys whose string values are code (scripts, transforms, expressions)
CODE_KEYS = ("script", "code", "expression")

PATTERNS = collections.OrderedDict([
	("hardcodedDb", '"papo_db" escrito en scripts o bindings'),
	("getHour24", "system.date.getHour24 / getHour24"),
	("registerCodeByTimestamp", "Último RegisterCode ordenado por Timestamp (o ID)"),
	("projectPrefix", "Llamada con prefijo project.papo_core"),
	("legacyKeys", "Claves legacy en view.custom"),
	("formOnStartup", "Form_*: onStartup sin papo_core.ui.initForm"),
	("formInsights", "Form_*: custom.insights sin preInsight"),
	("formToggleParams", "Form_*: toggleFlexRoot con params distintos de [sectionIndex]"),
	("formSaveDataRoot", "Form_*: saveDataRoot sin papo_core.register"),
	("formAnswerRecopile", "Form_*: answerRecopile sin papo_core.register"),
])

RE_DB = re.compile(r"""["']papo_db["']""")
RE_HOUR24 = re.compile(r"getHour24\s*\(")
RE_PREFIX = re.compile(r"\bproject\.papo_core\b")
RE_ORDER = re.compile(r"ORDER\s+BY\s+([\w\.\[\]]+)", re.IGNORECASE)
RE_DIRECTION = re.compile(r"\s+(ASC|DESC)\b", re.IGNORECASE)
RE_SELECT = re.compile(r"\bSELECT\b", re.IGNORECASE)
RE_FROM = re.compile(r"\bFROM\b", re.IGNORECASE)


def _iterCode(node, path):
	"""Yield (path, text) for every code string in the view tree."""
	if isinstance(node, dict):
		for key, value in node.items():
			childPath = path + [key]
			if key in CODE_KEYS and isinstance(value, str):
				yield childPath, value
			elif key == "binding" and isinstance(value, dict):
				# Binding configs can carry literal queries/paths besides transforms
				for cfgPath, text in _iterStrings(value.get("config", {}), childPath + ["config"]):
					yield cfgPath, text
				for subPath, text in _iterCode(value, childPath):
					yield subPath, text
			else:
				for subPath, text in _iterCode(value, childPath):
					yield subPath, text
	elif isinstance(node, list):
		for index, value in enumerate(node):
			for subPath, text in _iterCode(value, path + [index]):
				yield subPath, text


def _iterStrings(node, path):
	"""Yield (path, text) for every string under a node."""
	if isinstance(node, dict):
		for key, value in node.items():
			for subPath, text in _iterStrings(value, path + [key]):
				yield subPath, text
	elif isinstance(node, list):
		for index, value in enumerate(node):
			for subPath, text in _iterStrings(value, path + [index]):
				yield subPath, text
	elif isinstance(node, str):
		yield path, node


def _describe(view, path):
	"""Turn a JSON path into 'component > location' using meta.name."""
	names = []
	node = view
	location = []
	for step in path:
		node = node[step]
		if isinstance(node, dict) and isinstance(node.get("meta"), dict) and "name" in node["meta"]:
			names.append(node["meta"]["name"])
			location = []
		elif isinstance(node, dict) and isinstance(step, int) and (node.get("messageType") or node.get("name")):
			# Name handlers and custom methods instead of using their list index
			location.append(node.get("messageType") or node.get("name"))
		else:
			location.append(str(step))
	component = "/".join(names) if names else "(view)"
	return "{} · {}".format(component, ".".join(location))


def _lastRegisterCodeByTime(text):
	"""
	True when a query selects RegisterCode and orders by Timestamp/ID DESC first.

	Only the statement-level SELECT that owns each ORDER BY is considered (not a
	subquery), so queries that filter by RegisterCode = ? and sort rows by ID are
	not reported.
	"""
	if "registercode" not in text.lower():
		return False
	for match in RE_ORDER.finditer(text):
		firstKey = match.group(1).split(".")[-1].strip("[]").lower()
		if firstKey not in ("timestamp", "id"):
			continue
		direction = RE_DIRECTION.match(text, match.end())
		if not direction or direction.group(1).upper() != "DESC":
			continue
		select = _ownerSelect(text, match.start())
		if select is not None and "registercode" in select.lower():
			return True
	return False


def _ownerSelect(text, orderPos):
	"""Return the column list of the statement-level SELECT before orderPos."""
	candidates = [m for m in RE_SELECT.finditer(text, 0, orderPos)
		if not text[:m.start()].rstrip().endswith("(")]
	if not candidates:
		return None
	start = candidates[-1].end()
	fromMatch = RE_FROM.search(text, start, orderPos)
	return text[start:fromMatch.start()] if fromMatch else None


def _scriptOf(config):
	"""Return the script text of an event config (dict or list form)."""
	if isinstance(config, list):
		return "\n".join(_scriptOf(item) for item in config)
	if isinstance(config, dict):
		return (config.get("config") or {}).get("script", "") or ""
	return ""


def lintView(view, viewPath):
	"""
	Lint one parsed view.json.

	Args:
		view (dict): Parsed view.json
		viewPath (str): View path relative to the views folder

	Returns:
		list: (patternKey, detail) tuples
	"""
	findings = []
	seen = set()
	for path, text in _iterCode(view, []):
		where = _describe(view, path)
		checks = (
			("hardcodedDb", RE_DB.search(text)),
			("getHour24", RE_HOUR24.search(text)),
			("registerCodeByTimestamp", _lastRegisterCodeByTime(text)),
			("projectPrefix", RE_PREFIX.search(text)),
		)
		for key, hit in checks:
			if hit and (key, where) not in seen:
				seen.add((key, where))
				findings.append((key, where))

	custom = view.get("custom") or {}
	legacy = [key for key in LEGACY_KEYS if key in custom]
	if legacy:
		findings.append(("legacyKeys", ", ".join(legacy)))

	if os.path.basename(viewPath).startswith("Form_"):
		onStartup = ((view.get("events") or {}).get("system") or {}).get("onStartup")
		if onStartup is None:
			findings.append(("formOnStartup", "sin onStartup"))
		elif "papo_core.ui.initForm" not in _scriptOf(onStartup):
			findings.append(("formOnStartup", "onStartup sin initForm"))

		insights = (view.get("propConfig") or {}).get("custom.insights")
		transforms = ((insights or {}).get("binding") or {}).get("transforms") or []
		if not any("preInsight" in (t.get("code") or "") for t in transforms):
			findings.append(("formInsights", "sin binding" if insights is None else "binding sin preInsight"))

		scripts = (view.get("root") or {}).get("scripts") or {}
		methods = dict((m.get("name"), m) for m in scripts.get("customMethods") or [])
		handlers = dict((h.get("messageType"), h) for h in scripts.get("messageHandlers") or [])

		toggle = methods.get("toggleFlexRoot")
		if toggle is None:
			findings.append(("formToggleParams", "sin toggleFlexRoot"))
		elif toggle.get("params") != ["sectionIndex"]:
			findings.append(("formToggleParams", "params {}".format(toggle.get("params"))))

		for key, item, label in (("formSaveDataRoot", handlers.get("saveDataRoot"), "saveDataRoot"),
				("formAnswerRecopile", methods.get("answerRecopile"), "answerRecopile")):
			if item is None:
				findings.append((key, "sin {}".format(label)))
			elif "papo_core.register" not in (item.get("script") or ""):
				findings.append((key, "{} con lógica propia".format(label)))
	return findings


def _collectViews(viewsRoot, only):
	"""Return sorted view paths (relative) to lint."""
	if only:
		result = []
		for item in only:
			item = os.path.abspath(item)
			folder = os.path.dirname(item) if item.endswith("view.json") else item
			result.append(os.path.relpath(folder, viewsRoot))
		return sorted(result)
	result = []
	for folder, _dirs, files in os.walk(viewsRoot):
		if "view.json" in files:
			result.append(os.path.relpath(folder, viewsRoot))
	return sorted(result)


def buildReport(results, errors, scope):
	"""
	Build the Markdown report.

	Args:
		results (dict): viewPath -> list of (patternKey, detail)
		errors (dict): viewPath -> parse error message
		scope (str): Description of what was linted

	Returns:
		str: Markdown text
	"""
	lines = []
	lines.append("# PAPO lint")
	lines.append("")
	lines.append("Generado: {} · Alcance: {} · Vistas analizadas: {}".format(
		datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), scope, len(results) + len(errors)))
	lines.append("")
	lines.append("Generado por `.claude/skills/papo-lint/scripts/papo_lint.py` (solo lectura).")
	lines.append("")
	lines.append("## Resumen por patrón")
	lines.append("")
	lines.append("| Patrón | Vistas | Hallazgos |")
	lines.append("|---|:-:|:-:|")
	for key, label in PATTERNS.items():
		views = [v for v, f in results.items() if any(k == key for k, _d in f)]
		count = sum(1 for f in results.values() for k, _d in f if k == key)
		lines.append("| {} | {} | {} |".format(label, len(views), count))
	flagged = [v for v, f in results.items() if f]
	lines.append("")
	lines.append("Vistas con al menos un hallazgo: {}".format(len(flagged)))
	if errors:
		lines.append("")
		lines.append("## Vistas que no parsean ({})".format(len(errors)))
		lines.append("")
		for viewPath in sorted(errors):
			lines.append("- `{}` — {}".format(viewPath, errors[viewPath]))
	lines.append("")
	lines.append("## Detalle por vista")
	for viewPath in sorted(flagged, key=lambda v: (-len(results[v]), v)):
		lines.append("")
		lines.append("### `{}` ({})".format(viewPath, len(results[viewPath])))
		lines.append("")
		for key, detail in results[viewPath]:
			lines.append("- **{}**: {}".format(PATTERNS[key], detail))
	return "\n".join(lines) + "\n"


def main():
	"""Parse CLI args, lint the views and write or print the report."""
	parser = argparse.ArgumentParser(description="PAPO view linter (read-only)")
	parser.add_argument("--project", default=os.path.join(REPO_ROOT, "cla-project"))
	parser.add_argument("--out", default=os.path.join(REPO_ROOT, ".claude", "docs", "LINT_REPORT.md"))
	parser.add_argument("--views", nargs="*")
	parser.add_argument("--stdout", action="store_true")
	args = parser.parse_args()

	viewsRoot = os.path.join(os.path.abspath(args.project), VIEWS_REL)
	results = collections.OrderedDict()
	errors = {}
	for viewPath in _collectViews(viewsRoot, args.views):
		try:
			with open(os.path.join(viewsRoot, viewPath, "view.json"), encoding="utf-8") as handle:
				view = json.load(handle)
		except Exception as e:
			errors[viewPath] = str(e)
			continue
		results[viewPath] = lintView(view, viewPath)

	scope = "vistas indicadas" if args.views else "todo el proyecto"
	report = buildReport(results, errors, scope)
	if args.stdout or args.views:
		sys.stdout.write(report)
	else:
		with open(args.out, "w", encoding="utf-8") as handle:
			handle.write(report)
		print("Report written to {}".format(args.out))
	return 0


if __name__ == "__main__":
	sys.exit(main())
