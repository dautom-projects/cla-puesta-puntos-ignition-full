"""
Applies only the section-fit rule of papo_objects (fitSections) to views that are already standardized.

An open section keeps its height (FlexContainerGroupN with shrink 0) and custom.baseBasisPx reaches its rows, their
margins and the group padding: no row is squeezed and the end of the section is not cut. Nothing else changes; the
answer collection is checked before writing. Simulates by default.

Version: 1.0.0

Changelog:
	2026-10-26 | William M. | v1.0.0 - Initial version (squeezed rows in AC10-0201, PO11-0101-2, GR10-0501...)

Args (CLI):
	--views (str...): Form folders relative to views/ (default: every Form_* view with the PAPO/Form class, pilots included)
	--apply: Write the views (backup in .claude/backups/<date>/fit-sections/)

Returns:
	Exit code 0, or 1 when a view could not be written safely
"""

import argparse
import collections
import copy
import datetime
import glob
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import papo_design as design
import papo_objects as objects


def standardViews():
	"""Form_* views whose root has the PAPO/Form class (already standardized), pilots included."""
	out = []
	for path in sorted(glob.glob(os.path.join(design.VIEWS_DIR, "Page", "Embedded", "*", "Form_*", "view.json"))):
		text = open(path, encoding="utf-8").read()
		if "PAPO/Form" in text:
			out.append(os.path.relpath(os.path.dirname(path), design.VIEWS_DIR))
	return out


def main():
	parser = argparse.ArgumentParser(description="Secciones que alcanzan para sus filas (sin filas comprimidas)")
	parser.add_argument("--views", nargs="*")
	parser.add_argument("--apply", action="store_true")
	args = parser.parse_args()
	views = args.views or standardViews()
	backup = os.path.join(design.REPO_ROOT, ".claude", "backups", datetime.date.today().isoformat(), "fit-sections")
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
		objects.fitSections(view, stats)
		if not stats:
			continue
		if [objects.qa._key(s) for s in objects.qa.answerSources(before)] != [objects.qa._key(s) for s in objects.qa.answerSources(view)]:
			print("{} · error: cambió la recolección".format(rel))
			failed = True
			continue
		changed += 1
		total.update(stats)
		print("{} · {}".format(rel, ", ".join("{} {}".format(n, k) for k, n in stats.items())))
		if args.apply:
			target = os.path.join(backup, rel, "view.json")
			os.makedirs(os.path.dirname(target), exist_ok=True)
			shutil.copy2(path, target)
			design.writeView(path, view, crlf)
	print("{} vistas {} de {}: {}".format(changed, "ajustadas" if args.apply else "por ajustar", len(views),
		", ".join("{} {}".format(n, k) for k, n in total.items()) or "nada que ajustar"))
	return 1 if failed else 0


if __name__ == "__main__":
	sys.exit(main())
