"""
Tablet mode of the PAPO forms: marks the sections and rows with the PAPO/Tablet/* classes, whose only style lives in a
media query (max-width: 1300px), so a form looks exactly the same at 1920 x 1080 and adapts on a 10" tablet.

Per Form view:
	- SectionN and FlexContainerGroupN of the root get shrink 0 (without it the section headers squash when the form
	  is taller than the screen: EA11-1201_start at 1280 x 800)
	- FlexContainerGroupN gets PAPO/Tablet/Group and every component stacked in a column with a px height inside a
	  group is a row:
		group               -> PAPO/Tablet/Group      (tablet: min-height min-content, the open section grows with
		                                               its rows instead of cutting them)
		container or label  -> PAPO/Tablet/Row        (tablet: min-height min-content, the row keeps its px height
		                                               and grows when its text wraps or its field is taller)
	  and every embedded Objects/* view inside a group, stacked or inside a row:
		embedded Objects/*  -> PAPO/Tablet/ObjectRow  (tablet: min-height of a touch target; an embedded view has no
		                                               content height of its own, so the row around it grows with it)
	  A row without content height (spacer) keeps its px height.
	- FlexContainerSupervisor of the root gets PAPO/Tablet/Row and its embedded Objects/* PAPO/Tablet/ObjectRow (the
	  supervisor dropdown is 40 px in tablet and its 32 px container cut it); only layout classes, its options and
	  bindings are not touched
	The style lives in the gateway theme (gateway-themes/cla-*.css, block "MODO TABLET"): 8.1.19 style classes do not
	accept min-height, so the PAPO/Tablet/* classes are empty markers.
Nothing else changes: answer collection is checked before writing and the classes are only appended (a class with a
binding is left as it is and reported). Simulates by default.

Version: 1.2.0

Changelog:
	2026-11-14 | William M. | v1.0.0 - Initial version (tablet mode, plan of feature/tablet-responsive)
	2026-11-14 | William M. | v1.1.0 - Every embedded Objects/* view of a group is marked, also inside a row (EA11-1201:
		the numeric of a grid row kept the row at 27 px); style in the gateway theme
	2026-11-15 | William M. | v1.2.0 - FlexContainerSupervisor and its Objects/* dropdown are marked (the dropdown was cut
		by 8 px in tablet)

Args (CLI):
	--views (str...): Form folders relative to views/ (default: every Form_* view with the PAPO/Form class, pilots included)
	--apply: Write the views (backup in .claude/backups/<date>/tablet-rows/)

Returns:
	Exit code 0, or 1 when a view could not be written safely
"""

import argparse
import collections
import copy
import datetime
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import papo_design as design
import papo_objects as objects
from fit_sections import standardViews

GROUP_CLASS = "PAPO/Tablet/Group"
ROW_CLASS = "PAPO/Tablet/Row"
OBJECT_ROW_CLASS = "PAPO/Tablet/ObjectRow"
SECTION = re.compile(r"^Section\d+$")
GROUP = re.compile(r"^FlexContainerGroup\d+$")
SUPERVISOR = "FlexContainerSupervisor"


def _isColumn(node):
	return (node.get("props") or {}).get("direction") in ("column", "column-reverse")


def _addClass(node, cls, stats, key):
	"""Append cls to the static classes of node; a bound class is not touched."""
	if "props.style.classes" in (node.get("propConfig") or {}):
		stats["clase con binding (sin tocar)"] += 1
		return
	style = node.setdefault("props", {}).setdefault("style", {})
	tokens = str(style.get("classes", "")).split()
	if cls in tokens:
		return
	style["classes"] = " ".join(tokens + [cls])
	stats[key] += 1


def _isObject(node):
	return node.get("type") == "ia.display.view" and str((node.get("props") or {}).get("path", "")).startswith("Objects/")


def _markRows(container, stats):
	column = _isColumn(container)
	for child in container.get("children", []) or []:
		basis = str((child.get("position") or {}).get("basis", ""))
		if _isObject(child):
			_addClass(child, OBJECT_ROW_CLASS, stats, "objetos")
		elif column and basis.endswith("px") and child.get("type") != "ia.display.view":
			_addClass(child, ROW_CLASS, stats, "filas")
		if child.get("type") == "ia.container.flex":
			_markRows(child, stats)


def tabletRows(view, stats):
	"""Mark the sections and rows of one view (in place); stats counts what changed."""
	for child in view["root"].get("children", []) or []:
		name = child.get("meta", {}).get("name", "")
		if SECTION.match(name) or GROUP.match(name):
			position = child.setdefault("position", {})
			if position.get("shrink", 1) != 0:
				position["shrink"] = 0
				stats["shrink 0"] += 1
		if GROUP.match(name):
			_addClass(child, GROUP_CLASS, stats, "grupos")
			_markRows(child, stats)
		if name == SUPERVISOR and child.get("type") == "ia.container.flex":
			_addClass(child, ROW_CLASS, stats, "supervisor")
			for item in child.get("children", []) or []:
				if _isObject(item):
					_addClass(item, OBJECT_ROW_CLASS, stats, "supervisor objeto")


def main():
	parser = argparse.ArgumentParser(description="Clases del modo tablet en secciones y filas de los formularios")
	parser.add_argument("--views", nargs="*")
	parser.add_argument("--apply", action="store_true")
	args = parser.parse_args()
	views = args.views or standardViews()
	backup = os.path.join(design.REPO_ROOT, ".claude", "backups", datetime.date.today().isoformat(), "tablet-rows")
	total, changed, failed = collections.Counter(), 0, False
	for rel in views:
		path = os.path.join(design.VIEWS_DIR, rel, "view.json")
		view, crlf, canonical = design.loadView(path)
		if not canonical:
			print("{} · rechazada (no es Gson canónico)".format(rel))
			failed = True
			continue
		before = copy.deepcopy(view)
		stats = collections.Counter()
		tabletRows(view, stats)
		if not stats:
			continue
		if [objects.qa._key(s) for s in objects.qa.answerSources(before)] != [objects.qa._key(s) for s in objects.qa.answerSources(view)]:
			print("{} · error: cambió la recolección".format(rel))
			failed = True
			continue
		changed += 1
		total.update(stats)
		print("{} · {}".format(rel, ", ".join("{} {}".format(n, k) for k, n in sorted(stats.items()))))
		if args.apply:
			target = os.path.join(backup, rel, "view.json")
			os.makedirs(os.path.dirname(target), exist_ok=True)
			shutil.copy2(path, target)
			design.writeView(path, view, crlf)
	print("{} vistas {} de {}: {}".format(changed, "marcadas" if args.apply else "por marcar", len(views),
		", ".join("{} {}".format(n, k) for k, n in sorted(total.items())) or "nada que marcar"))
	return 1 if failed else 0


if __name__ == "__main__":
	sys.exit(main())
