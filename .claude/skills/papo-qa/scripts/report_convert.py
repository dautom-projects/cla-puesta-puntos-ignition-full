"""
Proposes the papo_core.report.build() call of an old report script (data.bin), block by block.

Each query block of the old script is recognized as a section: one key per record ('name{}'.format(k+1)) or one
merged key (fillDataFromRegisterhistoryDataset(ds, data, name)), its normalization (normalizar_dict, _yn, _ok) and
its reprocessed marks (extract_and_classify_items, _quality, _yn, _ok, _bad). The comment block and the signature
block give the signature style. Anything else is returned as "unknown" lines: those reports need a few lines after
build() or a new engine option, and the comparison with the old script (report_shadow.py) decides.

Version: 1.0.0

Changelog:
	2026-10-27 | William M. | v1.0.0 - Initial version (migration of the report scripts to build())

Usage (CLI, from projects/):
	report_convert.py <Area/REF>...      proposal and unknown lines per report

Usage (Python):
	options, unknown = convert(script)   options = {"sections": [...], "signatures": ..., ...}
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import report_bin as rb

REPORTS = os.path.join(HERE, "..", "..", "..", "..", "cla-project", "com.inductiveautomation.reporting", "reports", "Clarios")

NORMALIZERS = {"normalizar_dict": "check", "normalizar_dict_yn": "yn", "normalizar_dict_ok": "ok"}
CLASSIFIERS = {"extract_and_classify_items": "check", "extract_and_classify_items_quality": "quality",
	"extract_and_classify_items_yn": "yn", "extract_and_classify_items_ok": "ok", "extract_and_classify_items_bad": "number"}

# Lines of a query block that carry no logic of their own
BORING = [r"^(from|import) ", r"^logger\s*=", r"^(papoID|nodeID|registerCode|db)\s*=\s*data\.get", r"^params\s*=\s*\[papoID,\s*nodeID,\s*registerCode(,\s*registerTypeID)?\]$",
	r"^ds\s*=\s*system\.db\.runPrepQuery\(sql,\s*params,\s*db\)$", r"^rowCount\s*=\s*ds\.getRowCount\(\)$", r"^colCount\s*=\s*ds\.getColumnCount\(\)$",
	r"^headers\s*=\s*\[ds\.getColumnName\(i\) for i in range\(colCount\)\]$", r"^for k in range\(rowCount\):$",
	r"^values\s*=\s*\[ds\.getValueAt\(k, i\) for i in range\(colCount\)\]$", r"^oneByN\s*=\s*system\.dataset\.toDataSet\(headers, \[values\]\)$",
	r"^registerTypeID\s*=\s*\d+$"]


def _ids(expr, block):
	"""Item IDs of a reprocessed list: a literal list, list(range(a, b)), appends and a variable defined in the block."""
	expr = expr.strip()
	if re.match(r"^\w+$", expr) and not expr.isdigit():
		m = re.search(r"(?m)^\s*" + expr + r"\s*=\s*(.+)$", block)
		if not m:
			return None
		ids = _ids(m.group(1), block)
		if ids is None:
			return None
		for a in re.findall(r"(?m)^\s*" + expr + r"\.append\((\d+)\)", block):
			ids.append(int(a))
		return ids
	total = []
	for part in re.split(r"\s*\+\s*", expr):
		m = re.match(r"^(?:list\()?range\((\d+),\s*(\d+)\)\)?$", part)
		if m:
			total += list(range(int(m.group(1)), int(m.group(2))))
			continue
		m = re.match(r"^\[([\d,\s]*)\]$", part)
		if m:
			total += [int(x) for x in m.group(1).replace(" ", "").split(",") if x]
			continue
		return None
	return total


def _blocks(script):
	"""Query blocks of the main part (helpers removed)."""
	body = re.sub(r"(?s)\n\tdef \w+\(.*?(?=\n\t\S)", "\n", script)
	return re.split(r"(?=\n\tsql\s*=)", body)[1:]


def _signatureStyle(script):
	block = script[script.find("RegisterTypeID = 10"):] if "RegisterTypeID = 10" in script else script
	if "admin_idx" in block:
		return {"signatures": "role"}
	if "supervisorRoles" in block:
		return {"signatures": "roleLast", "signatureRoles": ["Supervisor_PAPO", "Administrator", "INTEGRADOR"]}
	return {"signatures": "roleLast"}


def _sections(block):
	"""(sections, unknown lines) of one query block; a block may fill one merged key and one key per record."""
	types = re.search(r"RegisterTypeID\s*(?:=|IN)\s*\(?\s*(\d[\d,\s]*)\)?", block)
	if not types and re.search(r"RegisterTypeID\s*=\s*\?", block):
		types = re.search(r"(?m)^\s*registerTypeID\s*=\s*(\d+)", block)
	code = re.sub(r"(?s)(sql\s*=\s*)'''.*?'''", r"\1'''", block)
	lines = [l.strip() for l in code.splitlines() if l.strip() and not l.strip().startswith("#")]
	if not types:
		return [], lines
	typeIDs = [int(x) for x in types.group(1).replace(" ", "").split(",") if x]
	single, record, unknown = None, None, []
	names = {}          # variable -> (base, numbered)
	groups = []         # {"var", "ids", "mode", "on": "ds" | "oneByN"}
	for l in lines:
		if any(re.match(p, l) for p in BORING) or re.match(r"^sql\s*=", l) or l == "'''":
			continue
		m = re.match(r"^(\w+)\s*=\s*'(\w+?)(\{\})?'(?:\.format\(k\s*\+\s*1\))?$", l)
		if m:
			names[m.group(1)] = (m.group(2), bool(m.group(3)))
			continue
		m = re.match(r"^fillDataFromRegisterhistoryDataset\(\s*(ds|oneByN)\s*,\s*data\s*,\s*(?:\"(\w+)\"|'(\w+)'|(\w+))\s*\)$", l)
		if m:
			base = m.group(2) or m.group(3) or names.get(m.group(4), (None, False))[0]
			if m.group(1) == "ds":
				single = {"types": typeIDs, "name": base, "slot": "single", "_norm": None, "_groups": []}
			else:
				record = {"types": typeIDs, "name": base, "_norm": None, "_groups": []}
			continue
		m = re.match(r"^(?:data\[(\w+)\]|data\['(\w+)'\]|result)\s*=\s*(normalizar_dict\w*)\(data\[(?:(\w+)|'(\w+)')\]\)$", l)
		if m and m.group(3) in NORMALIZERS:
			src = m.group(5) or names.get(m.group(4), (None, False))[0]
			target = single if single and single["name"] == src else record if record and record["name"] == src else None
			if target is not None:
				target["_norm"] = NORMALIZERS[m.group(3)]
				continue
		if re.match(r"^data\['\w+'\]\s*=\s*result$", l):
			continue
		m = re.match(r"^(\w+)\s*=\s*(extract_and_classify_items\w*)\(\s*(ds|oneByN)\s*,\s*(?:allowed_ids\s*=\s*)?(.+?)\s*\)$", l)
		if m and m.group(2) in CLASSIFIERS:
			ids = _ids(m.group(4), code)
			if ids is None:
				unknown.append(l)
				continue
			groups.append({"var": m.group(1), "ids": ids, "mode": CLASSIFIERS[m.group(2)], "on": m.group(3)})
			continue
		if re.match(r"^\w+\s*=\s*(list\(range|\[)", l) or re.match(r"^\w+\.append\(\d+\)$", l):
			continue
		m = re.match(r"^data\[(?:(\w+)|'(\w+)')\]\s*=\s*(normalizar_dict\w*)\((\w+)\)$", l)
		g = next((x for x in groups if m and x["var"] == m.group(4)), None) if m else None
		if g is not None:
			g["name"] = m.group(2) or names.get(m.group(1), (None, False))[0]
			g["normalize"] = NORMALIZERS.get(m.group(3), "check")
			continue
		unknown.append(l)
	out = []
	for sec in (single, record):
		if sec is None:
			continue
		on = "ds" if sec.get("slot") == "single" else "oneByN"
		norm = sec.pop("_norm")
		sec.pop("_groups")
		if norm is None:
			unknown.append("(sin normalizar: build() normaliza " + str(sec["name"]) + ")")
		elif norm != "check":
			sec["normalize"] = norm
		marks = []
		for g in groups:
			if g["on"] != on:
				continue
			if not g.get("name"):
				unknown.append("(marcas sin destino: " + g["var"] + ")")
				continue
			item = {"ids": g["ids"], "name": g["name"]}
			if g["mode"] != "check":
				item["mode"] = g["mode"]
			if g.get("normalize", norm or "check") != (norm or "check"):
				item["normalize"] = g["normalize"]
			marks.append(item)
		if marks:
			sec["reprocessed"] = marks
		out.append(sec)
	if not out:
		return [], lines
	return out, unknown


def _universal(script):
	"""The 'universal' script (SINGLE_TYPES / MULTI_TYPES lists)."""
	single = re.search(r"SINGLE_TYPES\s*=\s*\[(.*?)\]", script, re.S)
	multi = re.search(r"MULTI_TYPES\s*=\s*\[(.*?)\]", script, re.S)
	sections = [{"types": [int(t)], "name": n, "slot": "single"} for t, n in re.findall(r"\((\d+),\s*'(\w+)'\)", single.group(1))]
	sections += [{"types": [int(t)], "name": n} for t, n in re.findall(r"\((\d+),\s*'(\w+)'\)", multi.group(1))]
	return sections


def _inlineTypeVariable(script):
	"""RegisterTypeID = ? with params [..., registerTypeID]: put the value of the last registerTypeID = N before it."""
	out, last, pos = [], None, 0
	for m in re.finditer(r"(?m)^\s*registerTypeID\s*=\s*(\d+)\s*$|RegisterTypeID\s*=\s*\?", script):
		if m.group(1):
			last = m.group(1)
			continue
		if last is not None:
			out.append(script[pos:m.start()] + "RegisterTypeID = " + last)
			pos = m.end()
	out.append(script[pos:])
	return "".join(out)


def _dedent(script):
	"""Scripts whose body is indented with two tabs (TR11-0101, CU11-0101...) read as one tab."""
	lines = [l for l in script.split("\n") if l.strip()]
	if lines and sum(1 for l in lines if l.startswith("\t\t")) > 0.9 * len(lines):
		return "\n".join(l[1:] if l.startswith("\t") else l for l in script.split("\n"))
	return script


def convert(script):
	script = _inlineTypeVariable(_dedent(script))
	options = _signatureStyle(script)
	unknown = []
	if "SINGLE_TYPES" in script and "MULTI_TYPES" in script:
		options["sections"] = _universal(script)
		return options, unknown
	sections = []
	for block in _blocks(script):
		if "insights_list" in block or "insightsList" in block:
			continue
		if "firmaAdministrator" in block or "firmaOperator" in block:
			continue
		found, lines = _sections(block)
		sections += found
		unknown += lines
	options["sections"] = sections
	return options, unknown


def original(ref):
	"""data.bin of a report as it is in the repo, or its backup while report_shadow.py has the shadow on."""
	shadow = os.path.join(HERE, "..", "..", "..", "backups", "report-shadow", ref, "data.bin")
	return shadow if os.path.exists(shadow) else os.path.join(REPORTS, ref, "data.bin")


def main():
	for ref in sys.argv[1:]:
		path = original(ref)
		options, unknown = convert(rb.ReportBin(path).script())
		print("== {} · {}".format(ref, json.dumps({k: v for k, v in options.items() if k != "sections"})))
		for s in options["sections"]:
			print("    " + json.dumps(s, ensure_ascii=False))
		for u in unknown:
			print("    ?? " + u[:140])
	return 0


if __name__ == "__main__":
	sys.exit(main())
