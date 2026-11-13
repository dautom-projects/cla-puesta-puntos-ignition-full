"""
SQL scripts that cannot be broken by the encoding of the tool that runs them.

A script saved as UTF-8 without BOM and opened as Windows-1252 (SSMS without UTF-8 detection, sqlcmd without
-f 65001) turns every accent into two symbols: N'Verificación' is written as N'VerificaciÃ³n'. These are the
"weird symbols" of papoitem in production. Two tools:

  ascii <file.sql> [...]      rewrite the scripts in place with only ASCII: every non-ASCII character of a string
                              literal becomes NCHAR(code) (N'Verificaci' + NCHAR(243) + N'n') and comments are
                              transliterated; checks that every literal keeps exactly the same text
  repair > <file.sql>         print the production repair of papoitem.Description and registertype.Description:
                              diagnosis, backup table, REPLACE of the UTF-8 sequences read as Windows-1252 or
                              Latin-1, and the rows left to check by hand (texts damaged twice, with '?')

Version: 1.0.0

Changelog:
	2026-11-13 | William M. | v1.0.0 - Initial version (weird symbols in papoitem in production)
"""

import re
import sys
import unicodedata

# Characters of the forms whose UTF-8 sequences, read with the wrong encoding, become the weird symbols: all of
# Latin-1 (accents, signs, non-breaking space) and the punctuation and arrows used in the questions
TARGETS = u"".join(chr(c) for c in range(0xA0, 0x100)) + u"–—‘’“”•…€™←↑→↓"
CP1252_UNDEFINED = (0x81, 0x8D, 0x8F, 0x90, 0x9D)
# REPLACE calls per UPDATE (one statement does not nest them all)
CHUNK = 25
RE_LITERAL = re.compile(r"N?'(?:[^']|'')*'")


def misread(ch, encoding):
	"""Text of ch after its UTF-8 bytes are read as encoding (undefined Windows-1252 bytes keep their code)."""
	out = []
	for b in ch.encode("utf-8"):
		if encoding == "cp1252" and b in CP1252_UNDEFINED:
			out.append(chr(b))
		else:
			out.append(bytes([b]).decode(encoding))
	return "".join(out)


def patterns():
	"""(damaged text, good character), longest first so a 3-byte sequence goes before its 2-byte prefix."""
	pairs = {}
	for ch in TARGETS:
		for enc in ("cp1252", "latin-1"):
			bad = misread(ch, enc)
			if bad != ch:
				pairs[bad] = ch
	return sorted(pairs.items(), key=lambda p: (-len(p[0]), p[0]))


def nexpr(text):
	"""T-SQL expression for text using only ASCII: N'abc' + NCHAR(243) + N'def'."""
	parts, run = [], []
	for c in text:
		if ord(c) < 128:
			run.append(c)
		else:
			if run:
				parts.append("N'" + "".join(run).replace("'", "''") + "'")
				run = []
			parts.append("NCHAR({0})".format(ord(c)))
	if run or not parts:
		parts.append("N'" + "".join(run).replace("'", "''") + "'")
	return " + ".join(parts)


def literal_text(lit):
	"""Text of a SQL literal N'..' or '..'."""
	body = lit[2:-1] if lit.startswith("N") else lit[1:-1]
	return body.replace("''", "'")


def ascii_comment(text):
	"""Comment without accents (it only has to be readable, not exact)."""
	out = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
	return out


def to_ascii(sql):
	"""Script with only ASCII; raises if a literal does not keep its text."""
	out = []
	for line in sql.split("\n"):
		code, comment = line, ""
		# Split a trailing comment that is not inside a literal
		pos, inLit = 0, False
		for i, c in enumerate(line):
			if c == "'":
				inLit = not inLit
			elif c == "-" and not inLit and line[i:i + 2] == "--":
				code, comment = line[:i], line[i:]
				break
		def repl(m):
			lit = m.group(0)
			text = literal_text(lit)
			if all(ord(c) < 128 for c in text):
				return lit
			return "(" + nexpr(text) + ")"
		code = RE_LITERAL.sub(repl, code)
		out.append(code + ascii_comment(comment))
	result = "\n".join(out)
	if any(ord(c) > 127 for c in result):
		raise ValueError("quedó texto no ASCII")
	return result


def evaluate(expr):
	"""Text of an expression made of N'..' literals and NCHAR(n) joined by +."""
	text = []
	for m in re.finditer(r"N'((?:[^']|'')*)'|NCHAR\((\d+)\)", expr):
		text.append(m.group(1).replace("''", "'") if m.group(1) is not None else chr(int(m.group(2))))
	return "".join(text)


def chains(col):
	"""REPLACE expressions of the repair, CHUNK patterns each, to apply in order (one UPDATE each)."""
	pats = patterns()
	out = []
	for i in range(0, len(pats), CHUNK):
		expr = "{0} COLLATE Latin1_General_BIN2".format(col)
		for bad, good in pats[i:i + CHUNK]:
			expr = "REPLACE({0}, {1}, {2})".format(expr, nexpr(bad), nexpr(good))
		out.append(expr)
	return out


def suspect(col):
	"""Condition of a damaged text: the first symbols of a UTF-8 sequence read as Windows-1252 or Latin-1."""
	marks = (u"\u00c3", u"\u00c2", u"\u00e2\u20ac", u"\u00e2\u2020", u"\u00e2\u0080", u"\u00e2\u0086", u"\ufffd")
	return " OR ".join("CHARINDEX({0}, {1} COLLATE Latin1_General_BIN2) > 0".format(nexpr(m), col) for m in marks)


def repair_script():
	"""Production repair of papoitem and registertype, only ASCII."""
	updates = []
	for table in ("papoitem", "registertype"):
		for expr in chains("Description"):
			updates.append("UPDATE {0} SET Description = {1} WHERE {2};".format(table, expr, suspect("Description")))
	lines = [
		"-- Reparacion de simbolos raros en papoitem.Description y registertype.Description (produccion)",
		"-- Generado por .claude/skills/papo-qa/scripts/sql_encoding.py repair el 2026-11-13.",
		"-- Causa: texto UTF-8 leido como Windows-1252 o Latin-1 (p. ej. un script .sql abierto sin detectar UTF-8):",
		"-- cada tilde queda como dos o tres simbolos (o con tilde -> A con tilde + superindice 3). El archivo es solo",
		"-- ASCII (NCHAR) para que la herramienta que lo ejecute no lo vuelva a danar.",
		"-- Paso 1 (solo lectura): diagnostico. Paso 2: copia de respaldo y reparacion en una transaccion.",
		"-- Paso 3: lo que queda sospechoso (texto danado dos veces, con '?') se corrige a mano.",
		"-- Deshacer: UPDATE p SET Description = b.Description FROM papoitem p JOIN papoitem_bak_20261113 b ON b.ID = p.ID;",
		"--           (igual con registertype y registertype_bak_20261113)",
		"",
		"-- Paso 1: diagnostico",
		"SELECT COUNT(*) AS papoitem_sospechosos FROM papoitem WHERE " + suspect("Description") + ";",
		"SELECT ID, PapoID, Description FROM papoitem WHERE " + suspect("Description") + " ORDER BY ID;",
		"SELECT ID, Description FROM registertype WHERE " + suspect("Description") + " ORDER BY ID;",
		"",
		"-- Paso 2: respaldo y reparacion",
		"SET XACT_ABORT ON;",
		"BEGIN TRANSACTION;",
		"IF OBJECT_ID('papoitem_bak_20261113') IS NULL",
		"\tSELECT ID, Description INTO papoitem_bak_20261113 FROM papoitem WHERE " + suspect("Description") + ";",
		"IF OBJECT_ID('registertype_bak_20261113') IS NULL",
		"\tSELECT ID, Description INTO registertype_bak_20261113 FROM registertype WHERE " + suspect("Description") + ";",
	] + updates + [
		"COMMIT TRANSACTION;",
		"",
		"-- Paso 3: antes y despues, y lo que queda para revisar a mano (vacio salvo textos danados dos veces)",
		"SELECT p.ID, b.Description AS antes, p.Description AS ahora FROM papoitem p JOIN papoitem_bak_20261113 b ON b.ID = p.ID ORDER BY p.ID;",
		"SELECT ID, PapoID, Description FROM papoitem WHERE " + suspect("Description") + " ORDER BY ID;",
		"SELECT ID, Description FROM registertype WHERE " + suspect("Description") + " ORDER BY ID;",
		"",
	]
	text = "\n".join(lines)
	assert all(ord(c) < 128 for c in text)
	return text


def main(argv):
	if len(argv) >= 2 and argv[1] == "repair":
		sys.stdout.write(repair_script())
		return 0
	if len(argv) >= 3 and argv[1] == "ascii":
		for path in argv[2:]:
			original = open(path, encoding="utf-8").read()
			converted = to_ascii(original)
			# Same literals: evaluate every replaced expression and compare it with the original literal
			before = [literal_text(m.group(0)) for m in RE_LITERAL.finditer(_code_only(original))]
			after = []
			for m in re.finditer(r"\((N'(?:[^']|'')*'|NCHAR\(\d+\))(?: \+ (?:N'(?:[^']|'')*'|NCHAR\(\d+\)))*\)|N?'(?:[^']|'')*'", _code_only(converted)):
				tok = m.group(0)
				after.append(evaluate(tok) if tok.startswith("(") else literal_text(tok))
			if before != after:
				raise SystemExit("{0}: los literales no coinciden".format(path))
			open(path, "w", encoding="ascii", newline="").write(converted)
			print("{0}: {1} literales, {2} con NCHAR".format(path, len(before), sum(1 for t in before if any(ord(c) > 127 for c in t))))
		return 0
	print(__doc__)
	return 1


def _code_only(sql):
	"""The script without its comments (a -- outside a literal starts one)."""
	out = []
	for line in sql.split("\n"):
		inLit = False
		for i, c in enumerate(line):
			if c == "'":
				inLit = not inLit
			elif c == "-" and not inLit and line[i:i + 2] == "--":
				line = line[:i]
				break
		out.append(line)
	return "\n".join(out)


if __name__ == "__main__":
	sys.exit(main(sys.argv))
