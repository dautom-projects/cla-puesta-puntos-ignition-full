"""
Creates a pilot copy of a form (<Form>_PruebaPiloto), applies the full standard and runs QA.

Steps: copy view.json/thumbnail -> papo_design -> papo_objects (--legacy --form-class) ->
papo_qa against the original (stages 1-7) -> report in .claude/docs/qa/piloto-<form>.md.

Version: 1.1.0

Changelog:
	2026-10-25 | William M. | v1.0.0 - Initial version
	2026-10-25 | William M. | v1.1.0 - --rebuild regenerates an existing pilot (backup first)

Args (CLI):
	form (str): Form folder relative to views/ (e.g. "Page/Embedded/F&A/Form_AC10-0201_start")
	--rebuild: Regenerate the pilot when it exists (refused if it has changes not committed)

Returns:
	Exit code of the QA (0 = passes)
"""

import argparse
import collections
import datetime
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "papo-design", "scripts"))
import papo_design as design
import papo_objects as objects

RESOURCE = ('{\n  "scope": "G",\n  "version": 1,\n  "restricted": false,\n  "overridable": true,\n'
	'  "files": [\n    "view.json",\n    "thumbnail.png"\n  ],\n  "attributes": {\n    "lastModification": {\n'
	'      "actor": "external",\n      "timestamp": "2026-10-25T00:00:00Z"\n    }\n  }\n}')


def main():
	parser = argparse.ArgumentParser(description="Crea o regenera la copia piloto de un formulario")
	parser.add_argument("form")
	parser.add_argument("--rebuild", action="store_true")
	args = parser.parse_args()
	form = args.form.strip("/")
	source = os.path.join(design.VIEWS_DIR, form)
	target = source + "_PruebaPiloto"
	if os.path.exists(target):
		if not args.rebuild:
			print("Ya existe: {} (usar --rebuild)".format(target))
			return 1
		rel = os.path.relpath(target, design.REPO_ROOT)
		if subprocess.run(["git", "-C", design.REPO_ROOT, "status", "--porcelain", "--", rel], capture_output=True, text=True).stdout.strip():
			print("El piloto tiene cambios sin commit (guardados del Designer): commitealos antes")
			return 1
		backup = os.path.join(design.REPO_ROOT, ".claude", "backups", datetime.date.today().isoformat(), "make-pilot", rel)
		os.makedirs(os.path.dirname(backup), exist_ok=True)
		shutil.copy2(os.path.join(target, "view.json"), os.path.join(os.path.dirname(backup), os.path.basename(rel) + ".view.json"))
	else:
		os.makedirs(target)
	shutil.copy2(os.path.join(source, "view.json"), os.path.join(target, "view.json"))
	if os.path.exists(os.path.join(source, "thumbnail.png")):
		shutil.copy2(os.path.join(source, "thumbnail.png"), os.path.join(target, "thumbnail.png"))
	if not os.path.exists(os.path.join(target, "resource.json")):
		open(os.path.join(target, "resource.json"), "w").write(RESOURCE)

	path = os.path.join(target, "view.json")
	view, crlf, canonical = design.loadView(path)
	if not canonical:
		print("El original no es Gson canónico")
		return 1
	stats = collections.defaultdict(collections.Counter)
	design.standardize(view["root"], stats)
	design.writeView(path, view, crlf)
	counts = collections.Counter()
	status, detail = objects.processView(path, True, os.path.join(target, ".bk"), counts,
		{"rows": True, "repeaters": True, "legacy": True, "formClass": True, "staticIDs": True})
	shutil.rmtree(os.path.join(target, ".bk"), ignore_errors=True)
	print("{} · {} · {}".format(form, status, detail))
	print("Detalle: " + ", ".join("{} {}".format(n, k) for k, n in counts.most_common()))
	name = os.path.basename(form)
	report = os.path.join(design.REPO_ROOT, ".claude", "docs", "qa", "piloto-{}.md".format(name))
	return subprocess.call([sys.executable, os.path.join(HERE, "papo_qa.py"), "--pair", path, os.path.join(source, "view.json"),
		"--graph", "--report", report])


if __name__ == "__main__":
	sys.exit(main())
