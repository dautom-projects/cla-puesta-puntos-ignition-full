"""
Standardizes whole families of one area, one commit per family (phase 3 of the plan).

For each family: papo_design --apply -> papo_objects --apply (--legacy --form-class --static-ids, with the
question SQL check) -> papo_qa against HEAD with the graph (stages 1-7) -> row in DEPLOY_INVENTORY.md ->
commit "refactor: estándar en <family>" with the views, the QA report and the inventory. It stops at the first
family that fails (nothing of that family is committed; its views stay converted for review). Families of one
area run in order, so each one is compared with the commit of the previous one.

Before running it: the question SQL of the area applied in cla-db-papo (a pending UPDATE stops the family), no
pilot swap active and no Designer changes without commit.

Version: 1.1.0

Changelog:
	2026-10-26 | William M. | v1.0.0 - Initial version (used for the Ensamble area)
	2026-10-27 | William M. | v1.1.0 - --phase 5: converts the fields that stayed native in families already
		standardized (views without changes are fine; a family with no change is skipped); its own report
		(<family>-fase5.md), inventory row and commit message

Args (CLI):
	area (str): Folder under Page/Embedded (e.g. "Ensamble", "F&A")
	families (str...): Family references (e.g. "EA11-1101"): every Form_<family>_* view of the area, pilots excluded
	--dry-run: Only list the views of each family
	--phase (int): 3 (default, first standardization) or 5 (native fields left by phase 3)

Returns:
	Exit code 0 when every family was committed, 1 at the first failure
"""

import argparse
import datetime
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "papo-design", "scripts"))
import papo_design as design
import pilot_swap

REPO = design.REPO_ROOT
INVENTORY = os.path.join(REPO, ".claude", "docs", "DEPLOY_INVENTORY.md")
SUFFIX = "_PruebaPiloto"


def _run(args):
	r = subprocess.run(args, cwd=REPO, capture_output=True, text=True)
	return r.returncode, r.stdout + r.stderr


def familyViews(area, family):
	"""Form_<family>_<type> views of the area (relative to views/), pilots excluded.

	Digitalizacion_Template opens Form_<reference>_<type> with a type without spaces (start, 30min, SKU...): copies
	such as "Form_AC10-0201_30min D" are never opened and are left out.
	"""
	folder = os.path.join(design.VIEWS_DIR, "Page", "Embedded", area)
	pattern = re.compile(r"^Form_{}_[^ ]+$".format(re.escape(family)))
	return sorted("Page/Embedded/{}/{}".format(area, d) for d in os.listdir(folder)
		if pattern.match(d) and not d.endswith(SUFFIX))


def _objectsVersion():
	text = open(os.path.join(HERE, "..", "..", "papo-design", "scripts", "papo_objects.py"), encoding="utf-8").read()
	match = re.search(r"Version: ([\d.]+)", text)
	return match.group(1) if match else "?"


def _inventoryRow(family, views, summary, natives, report, phase=3):
	if phase == 5:
		return ("| {date} | nativos a objetos en la familia {family} (fase 5) | {views} | papo_objects v{version} "
			"(`--legacy --form-class --static-ids`) sobre la vista ya estandarizada: {summary} más; {natives} campos siguen "
			"nativos (lógica propia, leídos por scripts o rango no reproducible). QA 1–7 contra el commit anterior: pasa "
			"(`{report}`) | No: QA 1–7 |").format(date=datetime.date.today().isoformat(), family=family,
			views=", ".join("`{}`".format(v) for v in views), version=_objectsVersion(), summary=summary or "sin objetos",
			natives=natives, report=report)
	return ("| {date} | estándar en la familia {family} (fase 3) | {views} | papo-design + papo_objects v{version} "
		"(`--legacy --form-class --static-ids`): {summary}; {natives} campos quedan nativos (lógica propia, referenciados o "
		"propiedades sin parámetro). QA 1–7 contra el commit anterior: pasa (`{report}`) | No: etapas 8–9 solo en la primera "
		"familia del área |").format(date=datetime.date.today().isoformat(),
		family=family, views=", ".join("`{}`".format(v) for v in views), version=_objectsVersion(),
		summary=summary or "sin objetos", natives=natives, report=report)


def _addInventoryRow(row):
	lines = open(INVENTORY, encoding="utf-8").read().split("\n")
	rows = [i for i, l in enumerate(lines) if re.match(r"^\| \d{4}-\d{2}-\d{2} \|", l)]
	lines.insert((rows[-1] + 1) if rows else len(lines), row)
	open(INVENTORY, "w", encoding="utf-8").write("\n".join(lines))


def _allDone(out, views):
	"""Every view of the run is applied or unchanged (no error, no rejected view)."""
	states = re.findall(r"^- `?(.+?)`? · (aplicada|sin cambios|error|rechazada)", out, re.M)
	return len(states) == len(views) and all(s in ("aplicada", "sin cambios") for _, s in states)


def standardizeFamily(area, family, phase=3):
	"""Convert, check and commit one family. Returns (ok, message)."""
	views = familyViews(area, family)
	if not views:
		return False, "sin vistas"
	code, out = _run(["python3", os.path.join(HERE, "..", "..", "papo-design", "scripts", "papo_design.py"), "--views"] + views + ["--apply"])
	if code or not (("| aplicada | {} |".format(len(views)) in out) or (phase == 5 and _allDone(out, views))):
		return False, "papo-design: " + out[-1200:]
	check = os.path.join(tempfile.mkdtemp(prefix="papo-family-"), "preguntas.sql")
	code, out = _run(["python3", os.path.join(HERE, "..", "..", "papo-design", "scripts", "papo_objects.py"), "--views"] + views
		+ ["--legacy", "--form-class", "--static-ids", "--questions-sql", check, "--apply"])
	pending = re.search(r"Preguntas: (\d+) UPDATE", out)
	if code or not (("Vistas: {} aplicada".format(len(views)) in out) or (phase == 5 and _allDone(out, views))):
		return False, "papo_objects: " + out[-1200:]
	if pending and pending.group(1) != "0":
		return False, "faltan {} UPDATE de preguntas en la base (aplicar el SQL del área)".format(pending.group(1))
	detail = next((l for l in out.splitlines() if l.startswith("Detalle:")), "")
	files = [os.path.join("cla-project", "com.inductiveautomation.perspective", "views", v, "view.json") for v in views]
	if phase == 5 and not _run(["git", "status", "--porcelain", "--"] + files)[1].strip():
		return True, "sin cambios (nada que commitear)"
	report = ".claude/docs/qa/{}{}.md".format(family, "-fase5" if phase == 5 else "")
	code, out = _run(["python3", os.path.join(HERE, "papo_qa.py"), "--views"] + views + ["--baseline", "HEAD", "--graph", "--report", report])
	if "· PASA" not in out:
		return False, "QA: " + out[-2000:]
	objects = re.findall(r"(\d+) (Objects/\w+)", detail)
	summary = ", ".join("{} {}".format(n, o.replace("Objects/", "").lower()) for n, o in objects)
	natives = sum(int(n) for n in re.findall(r"(\d+) nativos", detail))
	_addInventoryRow(_inventoryRow(family, views, summary, natives, report, phase))
	files += [report, os.path.relpath(INVENTORY, REPO)]
	_run(["git", "add"] + files)
	if phase == 5:
		message = ("refactor: nativos a objetos en {} (fase 5)\n\nCampos que quedaron nativos en la fase 3 pasan a objetos "
			"estándar (papo_objects v{}): {}. Siguen nativos: {}. QA 1–7 pasa.\n\nCo-Authored-By: Claude Opus 5.5 "
			"<noreply@anthropic.com>").format(family, _objectsVersion(), summary or "sin objetos", natives)
	else:
		message = ("refactor: estándar en {}\n\n{} vistas con objetos estándar, clases PAPO/, preguntas desde papoItemID, papoItemID fijo "
			"y limpieza legacy. {}. QA 1–7 pasa.\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>").format(
			family, len(views), summary or "Sin objetos")
	code, out = _run(["git", "commit", "-q", "-m", message, "--"] + files)
	if code:
		return False, "commit: " + out
	commit = _run(["git", "log", "--oneline", "-1"])[1].strip()
	return True, "{} · {} · {} nativos".format(commit, summary or "sin objetos", natives)


def main():
	parser = argparse.ArgumentParser(description="Estandariza familias completas de un área, un commit por familia")
	parser.add_argument("area")
	parser.add_argument("families", nargs="+")
	parser.add_argument("--dry-run", action="store_true")
	parser.add_argument("--phase", type=int, choices=(3, 5), default=3)
	args = parser.parse_args()
	if pilot_swap.activeSwaps():
		print("hay intercambios de pilotos activos: pilot_swap.py off --all antes de convertir")
		return 1
	for family in args.families:
		views = familyViews(args.area, family)
		print("== {} ({} vistas)".format(family, len(views)))
		if args.dry_run:
			for v in views:
				print("   " + v)
			continue
		ok, message = standardizeFamily(args.area, family, args.phase)
		print("   " + message)
		if not ok:
			return 1
	return 0


if __name__ == "__main__":
	sys.exit(main())
