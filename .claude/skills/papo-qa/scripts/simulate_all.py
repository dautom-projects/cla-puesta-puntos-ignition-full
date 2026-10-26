"""
Simulates the full standard (papo_design + papo_objects) on every Form_* view and runs QA against the original.

The originals are read from a git commit (default HEAD), so an active pilot swap or a Designer save does not
change the result. Nothing in the project is written: converted views go to a temp folder.

Version: 1.0.0

Changelog:
	2026-10-25 | William M. | v1.0.0 - Initial version

Args (CLI):
	--baseline (str): Git commit of the originals. Default: HEAD
	--views (str...): Only these form folders (default: every Form_* view, pilots excluded)

Returns:
	Exit code 0 when every simulated form passes stages 1-6, 1 otherwise
"""

import argparse
import collections
import copy
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "papo-design", "scripts"))
import papo_design as design
import papo_objects as objects
import papo_qa as qa

OPTIONS = {"rows": True, "repeaters": True, "legacy": True, "formClass": True}


def _forms(ref):
	"""Form_* view.json paths (relative to the repo) at the baseline commit, pilots excluded."""
	views = os.path.relpath(design.VIEWS_DIR, design.REPO_ROOT)
	out = subprocess.run(["git", "-C", design.REPO_ROOT, "ls-tree", "-r", "--name-only", ref, "--", views],
		capture_output=True, text=True).stdout.splitlines()
	return [p for p in out if p.endswith("/view.json") and os.path.basename(os.path.dirname(p)).startswith("Form_")
		and not os.path.dirname(p).endswith("_PruebaPiloto")]


def main():
	parser = argparse.ArgumentParser(description="Simulación del estándar en todos los formularios")
	parser.add_argument("--baseline", default="HEAD")
	parser.add_argument("--views", nargs="*")
	args = parser.parse_args()
	tmp = tempfile.mkdtemp(prefix="papo-sim-")
	forms = _forms(args.baseline)
	if args.views:
		wanted = {v.strip("/") for v in args.views}
		forms = [f for f in forms if os.path.relpath(os.path.dirname(f), os.path.relpath(design.VIEWS_DIR, design.REPO_ROOT)) in wanted]
	stats, fails, examples = collections.Counter(), collections.Counter(), collections.defaultdict(list)
	passed = rejected = 0
	for rel in forms:
		raw = subprocess.run(["git", "-C", design.REPO_ROOT, "show", "{}:{}".format(args.baseline, rel)], capture_output=True).stdout.decode("utf-8")
		out = os.path.join(tmp, rel)
		os.makedirs(os.path.dirname(out), exist_ok=True)
		open(out, "w", encoding="utf-8", newline="").write(raw)
		view, crlf, canonical = design.loadView(out)
		if not canonical:
			rejected += 1
			continue
		base = {"view": json.loads(raw), "crlf": "\r\n" in raw}
		design.standardize(view["root"], collections.defaultdict(collections.Counter))
		objects.standardize(view, dict(OPTIONS), stats)
		design.writeView(out, view, crlf)
		results, _, _ = qa.checkView(out, base)
		bad = {k: v for k, v in results.items() if v}
		passed += not bad
		name = os.path.relpath(os.path.dirname(rel), os.path.relpath(design.VIEWS_DIR, design.REPO_ROOT))
		for stage, problems in bad.items():
			fails[stage] += 1
			if len(examples[stage]) < 10:
				examples[stage].append("{} · {}".format(name, problems[0][:160]))
	print("Simulados: {} · pasan: {} · rechazados (no canónicos): {}".format(len(forms) - rejected, passed, rejected))
	for stage in sorted(fails):
		print("Etapa {} {}: falla en {}".format(stage, qa.STAGES[stage], fails[stage]))
		for e in examples[stage]:
			print("    " + e)
	print("Detalle: " + ", ".join("{} {}".format(n, k) for k, n in stats.most_common()))
	return 1 if fails else 0


if __name__ == "__main__":
	sys.exit(main())
