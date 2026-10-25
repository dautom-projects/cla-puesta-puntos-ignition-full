"""
Creates a pilot copy of a form (<Form>_PruebaPiloto), applies the full standard and runs QA.

Steps: copy view.json/thumbnail -> papo_design -> papo_objects (--legacy --form-class) ->
papo_qa against the original (stages 1-7) -> report in .claude/docs/qa/piloto-<form>.md.

Version: 1.0.0

Changelog:
	2026-10-25 | William M. | v1.0.0 - Initial version

Args (CLI):
	form (str): Form folder relative to views/ (e.g. "Page/Embedded/F&A/Form_AC10-0201_start")

Returns:
	Exit code of the QA (0 = passes)
"""

import collections
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
	form = sys.argv[1].strip("/")
	source = os.path.join(design.VIEWS_DIR, form)
	target = source + "_PruebaPiloto"
	if os.path.exists(target):
		print("Ya existe: {}".format(target))
		return 1
	os.makedirs(target)
	shutil.copy2(os.path.join(source, "view.json"), os.path.join(target, "view.json"))
	if os.path.exists(os.path.join(source, "thumbnail.png")):
		shutil.copy2(os.path.join(source, "thumbnail.png"), os.path.join(target, "thumbnail.png"))
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
		{"rows": True, "repeaters": True, "legacy": True, "formClass": True})
	shutil.rmtree(os.path.join(target, ".bk"), ignore_errors=True)
	print("{} · {} · {}".format(form, status, detail))
	print("Detalle: " + ", ".join("{} {}".format(n, k) for k, n in counts.most_common()))
	name = os.path.basename(form)
	report = os.path.join(design.REPO_ROOT, ".claude", "docs", "qa", "piloto-{}.md".format(name))
	return subprocess.call([sys.executable, os.path.join(HERE, "papo_qa.py"), "--pair", path, os.path.join(source, "view.json"),
		"--graph", "--report", report])


if __name__ == "__main__":
	sys.exit(main())
