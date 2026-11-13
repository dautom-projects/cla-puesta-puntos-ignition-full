"""
Temporary swap of a pilot into the path of its original form, to test saving from the real flow.

Digitalizacion_Template opens each form by a path built from the PAPO (Page/Embedded/<area>/Form_<ref>_<type>),
so a _PruebaPiloto copy is never opened at runtime. "on" puts the pilot content in the original view.json
(backup first) on the local gateway; "off" restores the original byte for byte. Nothing is renamed or moved,
Digitalizacion_Template is not touched. Never commit while a swap is active (papo_qa warns about it).

Version: 1.0.1

Changelog:
	2026-10-25 | William M. | v1.0.0 - Initial version
	2026-10-26 | William M. | v1.0.1 - Warn not to edit the swapped views while the gateway rewrites them

Args (CLI):
	on <form>...: swap each pilot in (form = view folder, e.g. "Page/Embedded/F&A/Form_AC10-0201_start")
	off <form>... | off --all: restore the originals
	status: list active swaps

Returns:
	Exit code 0, or 1 when a swap could not be done or undone safely
"""

import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "papo-design", "scripts"))
import papo_design as design

REPO = design.REPO_ROOT
VIEWS = design.VIEWS_DIR
SUFFIX = "_PruebaPiloto"
STATE = os.path.join(REPO, ".claude", "backups", "pilot-swap", "state.json")


def _load():
	return json.load(open(STATE, encoding="utf-8")) if os.path.exists(STATE) else {}


def _save(state):
	os.makedirs(os.path.dirname(STATE), exist_ok=True)
	open(STATE, "w", encoding="utf-8").write(json.dumps(state, indent=2, ensure_ascii=False, sort_keys=True))


def activeSwaps():
	"""Forms whose pilot is in place of the original (used by papo_qa to warn)."""
	return sorted(_load())


def _form(name):
	name = name.strip("/")
	if name.startswith(os.path.relpath(VIEWS, REPO)):
		name = os.path.relpath(os.path.join(REPO, name), VIEWS)
	if name.endswith("/view.json"):
		name = os.path.dirname(name)
	return name[:-len(SUFFIX)] if name.endswith(SUFFIX) else name


def _read(path):
	return open(path, "rb").read()


def swapOn(form, state):
	original = os.path.join(VIEWS, form, "view.json")
	pilot = os.path.join(VIEWS, form + SUFFIX, "view.json")
	if form in state:
		return "ya estaba intercambiado"
	if not os.path.exists(original) or not os.path.exists(pilot):
		return "no existe el original o el piloto"
	rel = os.path.relpath(original, REPO)
	dirty = subprocess.run(["git", "-C", REPO, "status", "--porcelain", "--", rel], capture_output=True, text=True).stdout.strip()
	if dirty:
		return "el original tiene cambios sin commit (guardados del Designer): commitealos antes"
	backup = os.path.join(REPO, ".claude", "backups", "pilot-swap", datetime.date.today().isoformat(), rel)
	os.makedirs(os.path.dirname(backup), exist_ok=True)
	shutil.copy2(original, backup)
	open(original, "wb").write(_read(pilot))
	state[form] = {"backup": os.path.relpath(backup, REPO), "since": datetime.datetime.now().isoformat(timespec="seconds")}
	return None


def swapOff(form, state):
	if form not in state:
		return "no estaba intercambiado"
	original = os.path.join(VIEWS, form, "view.json")
	pilot = os.path.join(VIEWS, form + SUFFIX, "view.json")
	backup = os.path.join(REPO, state[form]["backup"])
	if not os.path.exists(backup):
		return "no se encontró el backup {}".format(state[form]["backup"])
	if _read(original) != _read(pilot):
		# Saved from the Designer while swapped: keep that content apart before restoring
		kept = backup + ".designer"
		shutil.copy2(original, kept)
		print("  aviso: el original cambió durante el intercambio; copia en {}".format(os.path.relpath(kept, REPO)))
	open(original, "wb").write(_read(backup))
	del state[form]
	return None


def main():
	parser = argparse.ArgumentParser(description="Intercambio temporal de un piloto con su formulario original")
	parser.add_argument("action", choices=("on", "off", "status"))
	parser.add_argument("forms", nargs="*")
	parser.add_argument("--all", action="store_true")
	args = parser.parse_args()
	state = _load()
	if args.action == "status":
		for form in sorted(state):
			print("{} · intercambiado desde {}".format(form, state[form]["since"]))
		print("{} intercambios activos".format(len(state)))
		return 0
	forms = sorted(state) if args.action == "off" and args.all else [_form(f) for f in args.forms]
	failed = False
	for form in forms:
		problem = (swapOn if args.action == "on" else swapOff)(form, state)
		_save(state)
		print("{} · {}".format(form, problem or ("piloto en la ruta del original" if args.action == "on" else "original restaurado")))
		failed = failed or bool(problem)
	if forms:
		print("Espera ~10 s (escaneo del gateway) y, en el Designer, Project → Update Project si tenías la vista abierta.")
		# The gateway rewrites the whole resource when it picks up an external change: an edit made before
		# that can be overwritten with the content it read
		print("No edites esas vistas en los próximos ~15 s: el gateway reescribe el recurso con lo que leyó.")
	return 1 if failed else 0


if __name__ == "__main__":
	sys.exit(main())
