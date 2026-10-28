"""
Shadow comparison of a report script against papo_core.report.build(), in the local gateway (temporary).

"on" wraps the report's current script in _old(data): the report keeps printing what it prints today, and right
after it runs _old and build(sections) on every cycle of that PAPO and logs the differences (logger
PAPO.report.shadow). "results" reads that log from the gateway container; "off" puts the original data.bin back
(byte for byte). Never commit a report with the shadow on.

Version: 1.0.0

Changelog:
	2026-10-27 | William M. | v1.0.0 - Initial version (pilot AC10-0202, AC10-0301, AC10-1101, CA02-2102)

Usage (CLI, from projects/):
	report_shadow.py on <Area/REF>... [--sections JSON]   sections default: read from the old script (F&A family)
	report_shadow.py results [--minutes N]                differences per report from the gateway log
	report_shadow.py off <Area/REF>...                    restore the original data.bin

Then open each report once in Gestion (any cycle of that PAPO, clones included) and run "results".
"""

import argparse
import collections
import datetime
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import report_bin as rb

REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
ROOT = os.path.join(REPO, "cla-project", "com.inductiveautomation.reporting", "reports", "Clarios", "Andina")
BACKUP = os.path.join(REPO, ".claude", "backups", "report-shadow")
CONTAINER = "PAPOS"
LOGS = "/usr/local/bin/ignition/logs/system_logs.idb"

SHADOW = u'''
	# ---- SHADOW (temporary): old script vs papo_core.report.build() on every cycle of this PAPO
	def _shadowValue(v):
		if v is None:
			return u""
		try:
			return unicode(v)
		except:
			return repr(v)
	def _shadowRows(ds):
		out = []
		for r in range(ds.getRowCount()):
			out.append(u" | ".join(_shadowValue(ds.getValueAt(r, c)) for c in range(ds.getColumnCount())))
		return out
	def _shadowCompare(data):
		sLogger = system.util.getLogger("PAPO.report.shadow")
		db = data.get('db', 'papo_db') or 'papo_db'
		sections = %(sections)s
		cycles = system.db.runPrepQuery("SELECT DISTINCT NodeID, RegisterCode FROM registerhistory WHERE PapoID = ? AND RegisterTypeID <> 12 ORDER BY NodeID, RegisterCode", [data.get('papoID')], db)
		diffs = []
		total = 0
		for r in range(cycles.getRowCount()):
			base = {'papoID': data.get('papoID'), 'db': db, 'nodeID': cycles.getValueAt(r, 0), 'registerCode': cycles.getValueAt(r, 1)}
			tag = u"{0}/{1}".format(base['nodeID'], base['registerCode'])
			a = dict(base)
			b = dict(base)
			try:
				_old(a)
			except Exception as e:
				diffs.append(tag + u" old error: " + unicode(e))
				continue
			papo_core.report.build(b, sections)
			total += 1
			for k in sorted(set(a.keys()) | set(b.keys())):
				if k in base or k == 'RegisterHistoryStation':
					continue
				va = a.get(k)
				vb = b.get(k)
				if isinstance(va, dict) or isinstance(vb, dict):
					va = va if isinstance(va, dict) else {}
					vb = vb if isinstance(vb, dict) else {}
					if k not in a or k not in b:
						diffs.append(u"{0} {1}: {2} != {3}".format(tag, k, "-" if k not in a else "{}", "-" if k not in b else "{}"))
					for sk in sorted(set(va.keys()) | set(vb.keys())):
						if _shadowValue(va.get(sk)) != _shadowValue(vb.get(sk)):
							diffs.append(u"{0} {1}.{2}: {3} != {4}".format(tag, k, sk, _shadowValue(va.get(sk)), _shadowValue(vb.get(sk))))
				elif _shadowValue(va) != _shadowValue(vb):
					diffs.append(u"{0} {1}: {2} != {3}".format(tag, k, _shadowValue(va), _shadowValue(vb)))
			# History list against the report query RegisterHistory
			hist = system.db.runPrepQuery("""SELECT rh.Timestamp AS Fecha, rh.[User] AS "Global ID", rh.Status AS "Estado", rt.Description AS "Tipo Registro", rh.RegisterTypeID FROM registerhistory rh INNER JOIN registertype rt ON rh.RegisterTypeID = rt.ID WHERE rh.PapoID = ? AND rh.NodeID = ? AND rh.RegisterCode = ? ORDER BY rh.Timestamp ASC""", [base['papoID'], base['nodeID'], base['registerCode']], db)
			if _shadowRows(hist) != _shadowRows(b['RegisterHistoryStation']):
				diffs.append(tag + u" RegisterHistoryStation distinto")
		sLogger.info(u"SHADOW %(ref)s ciclos={0} diferencias={1} :: {2}".format(total, len(diffs), u" || ".join(diffs[:300])))
	try:
		_shadowCompare(data)
	except Exception as e:
		system.util.getLogger("PAPO.report.shadow").error(u"SHADOW %(ref)s error: " + unicode(e))
'''



def sectionsOf(old):
	"""build() sections read from an old script of the F&A family (types, name, reprocessed ids)."""
	out = []
	for block in re.split(r"(?=\n\tsql\s*=)", old)[1:]:
		t = re.search(r"RegisterTypeID\s*(?:=|IN)\s*\(?([\d, ]+)\)?", block)
		name = re.search(r"name\s*=\s*'(\w+?)\{\}'\.format", block)
		if not t or not name:
			continue
		sec = {"types": [int(x) for x in t.group(1).replace(" ", "").split(",") if x], "name": name.group(1)}
		rep = re.search(r"rango\w*\s*=\s*\[([\d, ]+)\]", block)
		repName = re.search(r"name_reprocesed\s*=\s*'(\w+?)\{\}'\.format", block)
		if rep and repName:
			sec["reprocessedIds"] = [int(x) for x in rep.group(1).replace(" ", "").split(",") if x]
			sec["reprocessedName"] = repName.group(1)
		out.append(sec)
	return out


def on(ref, sections=None):
	path = os.path.join(ROOT, ref, "data.bin")
	backup = os.path.join(BACKUP, ref, "data.bin")
	os.makedirs(os.path.dirname(backup), exist_ok=True)
	if not os.path.exists(backup):
		shutil.copy2(path, backup)
	doc = rb.ReportBin(backup)
	old = doc.script()
	sections = sections or sectionsOf(old)
	body = u"\n".join((u"\t" + l) if l.strip() else l for l in old.split(u"\n"))
	new = u"\n\tdef _old(data):\n" + body + u"\n\t_old(data)\n" + SHADOW % {"sections": repr(sections), "ref": ref.split("/")[-1]}
	doc.path = path
	doc.replaceScript(old, new)
	doc.save()
	print("{} · sombra activa · {}".format(ref, json.dumps(sections)))


def off(ref):
	backup = os.path.join(BACKUP, ref, "data.bin")
	shutil.copy2(backup, os.path.join(ROOT, ref, "data.bin"))
	os.remove(backup)
	print("{} · restaurado".format(ref))


def results(minutes):
	"""Latest shadow line per report, grouped by kind of difference."""
	folder = tempfile.mkdtemp(prefix="report-shadow-")
	local = os.path.join(folder, "logs.idb")
	subprocess.check_call(["docker", "cp", "{}:{}".format(CONTAINER, LOGS), local], stdout=subprocess.DEVNULL)
	since = (datetime.datetime.now() - datetime.timedelta(minutes=minutes)).timestamp() * 1000
	rows = sqlite3.connect(local).execute("SELECT timestmp, formatted_message FROM logging_event WHERE logger_name = "
		"'PAPO.report.shadow' AND timestmp > ? ORDER BY timestmp DESC", (since,)).fetchall()
	seen = set()
	for ts, msg in rows:
		m = re.match(r"SHADOW (\S+) ciclos=(\d+) diferencias=(\d+) :: (.*)", msg, re.S)
		if not m:
			print(msg[:300])
			continue
		if m.group(1) in seen:
			continue
		seen.add(m.group(1))
		diffs = [d for d in m.group(4).split(" || ") if d]
		kinds = collections.Counter(re.sub(r"\d+", "N", re.match(r"\S+ ([^:]+)", d).group(1)) for d in diffs)
		print("{} · {} ciclos · {} diferencias".format(m.group(1), m.group(2), m.group(3)))
		for kind, n in kinds.most_common():
			print("    {} {}".format(n, kind))
		for d in diffs[:5]:
			print("      p. ej. {}".format(d[:160]))


def main():
	parser = argparse.ArgumentParser(description="Comparación en sombra de un reporte contra papo_core.report.build()")
	parser.add_argument("action", choices=("on", "off", "results"))
	parser.add_argument("refs", nargs="*")
	parser.add_argument("--sections")
	parser.add_argument("--minutes", type=int, default=30)
	args = parser.parse_args()
	if args.action == "results":
		results(args.minutes)
	for ref in args.refs:
		if args.action == "on":
			on(ref, json.loads(args.sections) if args.sections else None)
		elif args.action == "off":
			off(ref)
	return 0


if __name__ == "__main__":
	sys.exit(main())
