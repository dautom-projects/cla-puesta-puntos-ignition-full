"""
SQL scripts of papoitem without accents or ñ, and with only ASCII.

The questions of papoitem go without accents or ñ (user decision, 2026-11-13): a script saved as UTF-8 and opened
as Windows-1252 (SSMS, sqlcmd without -f 65001) turned every accent into two weird symbols (VerificaciÃ³n).

  plain <file.sql> [...]      rewrite the scripts in place: the text of every SET Description loses its accents and
                              ñ (Verificación -> Verificacion, Daño -> Dano) and the file keeps only ASCII (any other
                              symbol of a literal, like ± or °, becomes NCHAR(code)); the WHERE keeps its text

Version: 1.1.0

Changelog:
	2026-11-13 | William M. | v1.1.0 - Texts without accents or ñ (decision of the user); no production repair
	2026-11-13 | William M. | v1.0.0 - Initial version (weird symbols in papoitem in production)
"""

import re
import sys
import unicodedata

RE_LITERAL = re.compile(r"N?'(?:[^']|'')*'")
RE_EXPR = r"\((?:N'(?:[^']|'')*'|NCHAR\(\d+\))(?: \+ (?:N'(?:[^']|'')*'|NCHAR\(\d+\)))*\)|N'(?:[^']|'')*'"
RE_SET = re.compile(r"(SET Description = )(" + RE_EXPR + r")")


def plain(text):
	"""Text without accents or ñ: a letter with a mark becomes the letter (á -> a, Ñ -> N); other symbols stay."""
	out = []
	for c in text:
		d = unicodedata.normalize("NFD", c)
		marked = len(d) > 1 and d[0].isascii() and d[0].isalpha() and all(unicodedata.combining(x) for x in d[1:])
		out.append(d[0] if marked else c)
	return "".join(out)


def nexpr(text):
	"""T-SQL expression for text using only ASCII: N'abc' + NCHAR(176) + N'def'."""
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


def evaluate(expr):
	"""Text of an expression made of N'..' literals and NCHAR(n) joined by +."""
	text = []
	for m in re.finditer(r"N'((?:[^']|'')*)'|NCHAR\((\d+)\)", expr):
		text.append(m.group(1).replace("''", "'") if m.group(1) is not None else chr(int(m.group(2))))
	return "".join(text)


def literal_text(lit):
	"""Text of a SQL literal N'..' or '..'."""
	body = lit[2:-1] if lit.startswith("N") else lit[1:-1]
	return body.replace("''", "'")


def split_comment(line):
	"""(code, comment) of a line: a -- outside a literal starts the comment."""
	inLit = False
	for i, c in enumerate(line):
		if c == "'":
			inLit = not inLit
		elif c == "-" and not inLit and line[i:i + 2] == "--":
			return line[:i], line[i:]
	return line, ""


def to_ascii(sql):
	"""Script with only ASCII: SET texts without accents or ñ, other literals with NCHAR, comments transliterated."""
	out = []
	for line in sql.split("\n"):
		code, comment = split_comment(line)
		code = RE_SET.sub(lambda m: m.group(1) + nexpr(plain(evaluate(m.group(2)) if m.group(2).startswith("(") else literal_text(m.group(2)))), code)
		code = RE_LITERAL.sub(lambda m: m.group(0) if all(ord(c) < 128 for c in m.group(0)) else "(" + nexpr(literal_text(m.group(0))) + ")", code)
		comment = unicodedata.normalize("NFKD", comment).encode("ascii", "ignore").decode("ascii")
		out.append(code + comment)
	result = "\n".join(out)
	if any(ord(c) > 127 for c in result):
		raise ValueError("quedó texto no ASCII")
	return result


def main(argv):
	if len(argv) >= 3 and argv[1] == "plain":
		for path in argv[2:]:
			original = open(path, encoding="utf-8").read()
			converted = to_ascii(original)
			open(path, "w", encoding="ascii", newline="").write(converted)
			print("{0}: {1} SET sin tildes".format(path, len(RE_SET.findall(converted))))
		return 0
	print(__doc__)
	return 1


if __name__ == "__main__":
	sys.exit(main(sys.argv))
