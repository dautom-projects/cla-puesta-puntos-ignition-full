"""
Edit the text records of an Ignition 8.1 report resource (data.bin) without the Designer.

data.bin is gzip of a binary stream with a fixed 16-byte magic header. Each text of the report (data source
scripts, queries, the base64 XML of the page template...) is one record: a 4-byte id, a marker byte and the
UTF-8 bytes, with the length after the marker (0: 2 bytes, as Java writeUTF; 1: 4 bytes, for long texts like the
template). Changing a text rewrites only that record and its length; every other byte is kept.

Version: 1.0.1

Changelog:
	2026-10-27 | William M. | v1.0.1 - A record must be followed by another record: a script under 256 bytes
		that starts with a line break was read past its end
	2026-10-27 | William M. | v1.0.0 - Initial version (report fixes found by the general test)

Usage (CLI):
	report_bin.py show <data.bin> [--script | --template]    print the data script or the template XML
	report_bin.py check <data.bin>                             round trip: decode and encode give the same bytes

Usage (Python):
	doc = ReportBin(path); doc.replaceScript(old, new); doc.replaceTemplate(old, new); doc.save()
"""

import base64
import gzip
import re
import struct
import sys

MAGIC = bytes.fromhex("98298faa43f74a4fb28dca3c4896afc9")
RE_B64 = re.compile(rb"PD94bWwg[A-Za-z0-9+/=\r\n]+")
RE_TEXT = re.compile(r"<text\b[^>]*>.*?</text>", re.S)
RE_ATTR = re.compile(r'([\w-]+)="([^"]*)"')


class ReportBin(object):
	def __init__(self, path):
		self.path = path
		self.raw = gzip.decompress(open(path, "rb").read())
		if self.raw[:16] != MAGIC:
			raise ValueError("{}: cabecera desconocida".format(path))

	# ---- records -----------------------------------------------------------------------------------------
	def _record(self, pos):
		"""(start of the length field, text start, text end, long) of the record holding byte pos."""
		for s in range(pos - 3, max(15, pos - 70000), -1):
			marker = self.raw[s]
			if marker == 0:
				size, head = struct.unpack(">H", self.raw[s + 1:s + 3])[0], 3
			elif marker == 1 and s + 5 <= len(self.raw):
				size, head = struct.unpack(">I", self.raw[s + 1:s + 5])[0], 5
			else:
				continue
			start, end = s + head, s + head + size
			if start <= pos and end >= pos and end <= len(self.raw) and self._isText(start, end) and start == self._textStart(pos, start) \
					and self._nextIsRecord(end):
				return s, start, end, marker == 1
		raise ValueError("no se encontró el registro del texto en {}".format(pos))

	def _textStart(self, pos, start):
		return start

	def _nextIsRecord(self, end):
		"""A text record is followed by the next record's 4-byte id (small, so it starts with 0x00 0x00) or the
		end of the stream. Rejects a false header read from a short text's own length bytes plus its first char."""
		return end == len(self.raw) or self.raw[end:end + 2] == b"\x00\x00"

	def _isText(self, start, end):
		try:
			self.raw[start:end].decode("utf-8")
		except UnicodeDecodeError:
			return False
		# a record is preceded by its 4-byte id (big endian, small numbers)
		return self.raw[start - 7 if self.raw[start - 3] == 0 else start - 9] == 0

	def _find(self, needle, label):
		positions = [m.start() for m in re.finditer(re.escape(needle), self.raw)]
		if len(positions) != 1:
			raise ValueError("{}: {} apariciones de {!r}".format(label, len(positions), needle[:60]))
		return positions[0]

	def _replaceRecord(self, s, start, end, long, text):
		data = text.encode("utf-8")
		if not long and len(data) > 0xFFFF:
			raise ValueError("el texto supera 65535 bytes")
		length = struct.pack(">I", len(data)) if long else struct.pack(">H", len(data))
		self.raw = self.raw[:s + 1] + length + data + self.raw[end:]

	# ---- data script ------------------------------------------------------------------------------------
	def scripts(self):
		"""Data source scripts: records whose text has Python code (def / import / data[...])."""
		out = []
		for m in re.finditer(rb"\n\t+(?:from |import |def |data\[|papo_core\.)", self.raw):
			s, start, end, long = self._record(m.start())
			if not out or out[-1][1] != start:
				out.append((s, start, end, long))
		return out

	def script(self, index=0):
		s, start, end, long = self.scripts()[index]
		return self.raw[start:end].decode("utf-8")

	def replaceScript(self, old, new, index=0):
		"""Replace one exact text of the data script (it must appear once)."""
		s, start, end, long = self.scripts()[index]
		text = self.raw[start:end].decode("utf-8")
		if text.count(old) != 1:
			raise ValueError("script: {} apariciones de {!r}".format(text.count(old), old[:80]))
		self._replaceRecord(s, start, end, long, text.replace(old, new))

	# ---- page template ------------------------------------------------------------------------------------
	def _templateRecord(self):
		"""The template is a long record (marker 1 + 4-byte length) right before its base64 ("PD94bWwg" = "<?xml")."""
		m = RE_B64.search(self.raw)
		if not m:
			raise ValueError("sin plantilla")
		s = m.start() - 5
		size = struct.unpack(">I", self.raw[s + 1:s + 5])[0]
		if self.raw[s] != 1 or size != m.end() - m.start():
			raise ValueError("la plantilla no ocupa todo su registro ({} frente a {})".format(size, m.end() - m.start()))
		return s, m.start(), m.end(), True

	def template(self):
		s, start, end, long = self._templateRecord()
		return base64.b64decode(self.raw[start:end]).decode("utf-8")

	def _encodeTemplate(self, xml):
		"""base64 with the same line wrapping as the original (76 characters and \\n in most reports)."""
		s, start, end, long = self._templateRecord()
		original = self.raw[start:end]
		data = base64.b64encode(xml.encode("utf-8"))
		if b"\n" in original:
			width = original.index(b"\n")
			data = b"\n".join(data[i:i + width] for i in range(0, len(data), width))
			if original.endswith(b"\n"):
				data += b"\n"
		return data.decode("ascii")

	def replaceTemplate(self, old, new, count=1):
		"""Replace an exact text of the template XML; count = how many times it must appear."""
		xml = self.template()
		if xml.count(old) != count:
			raise ValueError("plantilla: {} apariciones de {!r} (se esperaban {})".format(xml.count(old), old[:80], count))
		self.setTemplate(xml.replace(old, new))

	def patchTexts(self, edit):
		"""Edit <text> shapes of the template one by one: edit(attrs, element) returns the new element text or None
		(attrs has x, y, width, height... as strings). Returns how many shapes changed."""
		xml = self.template()
		changes = []
		for m in RE_TEXT.finditer(xml):
			element = m.group(0)
			attrs = dict(RE_ATTR.findall(element[:element.index(">")]))
			new = edit(attrs, element)
			if new is not None and new != element:
				changes.append((m.start(), m.end(), new))
		for start, end, new in reversed(changes):
			xml = xml[:start] + new + xml[end:]
		if changes:
			self.setTemplate(xml)
		return len(changes)

	def setTemplate(self, xml):
		s, start, end, long = self._templateRecord()
		self._replaceRecord(s, start, end, long, self._encodeTemplate(xml))

	# ---- write --------------------------------------------------------------------------------------------
	def bytes(self):
		return gzip.compress(self.raw, mtime=0)

	def save(self, path=None):
		open(path or self.path, "wb").write(self.bytes())


def roundTrip(path):
	"""Re-encode the script and template with the same text: the stream must not change."""
	doc = ReportBin(path)
	before = doc.raw
	for i, (s, start, end, long) in enumerate(doc.scripts()):
		text = doc.raw[start:end].decode("utf-8")
		doc._replaceRecord(s, start, end, long, text)
	doc.setTemplate(doc.template())
	return doc.raw == before, len(doc.scripts())


if __name__ == "__main__":
	cmd, path = sys.argv[1], sys.argv[2]
	if cmd == "check":
		same, n = roundTrip(path)
		print("ida y vuelta {} · {} scripts".format("igual" if same else "DISTINTA", n))
		sys.exit(0 if same else 1)
	doc = ReportBin(path)
	if cmd == "show":
		print(doc.template() if "--template" in sys.argv else doc.script())
