"""
QA pipeline for PAPO Form views (gate before every standardization commit).

Compares each view against its version in a baseline commit and runs the stages:
	1 Estructura      JSON parses, Gson-canonical, same line endings as the baseline
	2 Recolección     same custom.item (papoItemID, registerTypeID, bindings), same order and
	                  container (FlexContainerGroupN / FlexContainerSupervisor); insights intact
	3 Respuestas      every converted field answers like the original (sample values and the
	                  answer kept while the object is not mounted) and shows and does the same:
	                  question / checkbox text, placeholder, enabled, value and option bindings
	4 Flujo v2        standard wrappers, no legacy handlers, no new "papo_db"
	5 Diseño          PAPO/Form root, standard fields, no fixed px widths, no new missing classes,
	                  expanded sections as tall as their rows (custom.baseBasisPx)
	6 Contrato        params passed to Objects/* exist with the right direction
	7 Grafo           no new unresolved references or unbalanced messages (--graph)
	8 Datos           saved DataAnswer of two registerhistory rows (--compare-db, SELECT only)
	9 Visual          manual checklist written to the report

Version: 1.8.0

Changelog:
	2026-10-25 | William M. | v1.0.0 - Initial version
	2026-10-25 | William M. | v1.1.0 - emptyAnswer, Objects/OptionGroup and Objects/DateTime; new broken component references fail stage 2
	2026-10-25 | William M. | v1.2.0 - Stage 3 also compares the field props the operator sees (text, placeholder,
		enabled, bindings); an unknown prop of a converted field fails
	2026-10-25 | William M. | v1.3.0 - Stage 5: an expanded section must fit its rows as before (custom.baseBasisPx);
		stage 3: an option group keeps the width of its question
	2026-10-25 | William M. | v1.4.0 - --exact: stage 8 compares every answer (records saved with the same values
		by ui_check.js on the original and on the pilot)
	2026-10-26 | William M. | v1.5.0 - Stage 3: a fixed question may read papoItemID when papoitem.Description has
		the same text (SELECT); the description query with display transforms counts as the item description
	2026-10-26 | William M. | v1.6.0 - Stage 2 compares the runtime papoItemID (item_ids.py): a computed ID now
		fixed in custom.item with the same value collects the same item
	2026-10-26 | William M. | v1.7.0 - Time fields open with the current time: the object needs startNow; --exact
		compares times of day by format only (each save opens at another time)
	2026-10-26 | William M. | v1.8.0 - Stage 3: a converted numeric must turn red for the same values as the
		original's color script (ranges.py)

Args (CLI):
	--views (str...): View folders or view.json paths
	--all-forms: Every Form_* view
	--baseline (str): Git commit to compare against. Default: HEAD
	--pair (str str): Current view.json and baseline view.json (repeatable, for tests)
	--graph: Run stage 7 (rebuilds the dependency graph in a temp folder)
	--compare-db (int int): registerhistory IDs of the pilot and the original record
	--exact: with --compare-db, every answer must be equal (both saved with ui_check.js)
	--report (str): Markdown report path (default: print)

Returns:
	Exit code 0 when every stage passed, 1 otherwise
"""

import argparse
import collections
import datetime
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "papo-design", "scripts"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "papo-lint", "scripts"))
import item_ids
import papo_design as design
import papo_lint as lint
import pilot_swap
import ranges
import view_refs

REPO = design.REPO_ROOT
VIEWS = design.VIEWS_DIR
STYLES = design.STYLES_DIR
GRAPH_SCRIPT = os.path.expanduser("~/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/"
	"633c31c8-b0a2-47fe-b7be-af38b4898a5a/97e4ea7a-da70-497a-8659-a5b60afe96ca/skills/ignition-graph/scripts/build_graph.py")
DB_ENV = os.path.expanduser("~/.config/papo-sql/claude_ro.env")

GROUP = re.compile(r"^(FlexContainerGroup\d+|FlexContainerSupervisor)$")
V2_PATTERNS = ("formOnStartup", "formInsights", "formToggleParams", "formSaveDataRoot", "formAnswerRecopile")
VALUE_PROP = {"ia.input.checkbox": ("selected", False), "ia.input.numeric-entry-field": ("value", None),
	"ia.input.text-field": ("text", ""), "ia.input.dropdown": ("value", None)}
EMPTY_DASH = 'return value if value else "-"'
OPENS_NOW = "hora de apertura"
RE_TIME_OF_DAY = re.compile(r"^\d{1,2}:\d{2}:\d{2} [AP]M$")
DESCRIPTION_QUERY = "SELECT Description FROM papoitem WHERE ID = ?"
RE_DEFAULT_PLACEHOLDER = re.compile(r"^\s*esc?r?i?ba(\s+aqu[ií])?\s*$", re.I)
OWN_VALUE = {"ia.input.checkbox": "selected", "ia.input.numeric-entry-field": "value", "ia.input.text-field": "text",
	"ia.input.dropdown": "value", "ia.input.date-time-input": "value"}
# Props every object sets the same way for all forms (standard design or behavior)
STANDARD_PROPS = {"style", "checkedIcon", "uncheckedIcon", "direction", "align", "format", "spinner", "containerStyle",
	"borderColor", "spellcheck", "formattedValue", "pickerType"}
CARRIED_PROPS = {"text", "placeholder", "enabled", "options", "showClearIcon"}
# Object param -> field prop it carries, when the names differ
PARAM_PROPS = {"Objects/Checkbox": {"question": "text", "value": "selected"}, "Objects/TextField": {"value": "text"}}
STAGES = collections.OrderedDict([("1", "Estructura"), ("2", "Recolección"), ("3", "Respuestas"), ("4", "Flujo v2"),
	("5", "Diseño"), ("6", "Contrato de objetos"), ("7", "Grafo"), ("8", "Datos"), ("9", "Visual")])


# ==================== SOURCES OF ANSWERS ====================

def answerSources(view):
	"""List answer sources in recopile order with their container; repeater instances expanded.

	The id is the runtime papoItemID (item_ids.py) when it can be computed, so a computed ID and the same ID
	fixed in custom.item give the same source; the papoItemID binding then stays out of the bindings.
	"""
	out = []
	runtime = item_ids.resolve(view)

	def walk(node, group, path):
		name = node.get("meta", {}).get("name", "")
		if GROUP.match(name):
			group = name
		if "item" in node.get("custom", {}):
			item = node["custom"]["item"] if isinstance(node["custom"]["item"], dict) else {}
			others = {k: v for k, v in node.get("propConfig", {}).items() if k.startswith("custom.item") and k != "custom.item.answer"}
			pid = runtime.get(tuple(path.split("/")))
			if isinstance(pid, int) and not isinstance(pid, bool):
				others.pop("custom.item.papoItemID", None)
			else:
				pid = item.get("papoItemID")
			out.append({"id": pid, "type": item.get("registerTypeID"),
				"bindings": json.dumps(others, sort_keys=True), "group": group, "path": path, "node": node})
		props = node.get("props") or {}
		if node.get("type") == "ia.display.flex-repeater" and props.get("instances") is not None:
			for i, inst in enumerate(props["instances"]):
				item = inst.get("item") or {}
				out.append({"id": inst.get("papoItemID", item.get("papoItemID")), "type": item.get("registerTypeID"),
					"bindings": "{}", "group": group, "path": "{}#{}".format(path, i), "node": None,
					"instance": inst, "repeaterView": props.get("path")})
			return
		for child in node.get("children", []):
			walk(child, group, path + "/" + child.get("meta", {}).get("name", "?"))

	walk(view["root"], "root", "root")
	return out


def _key(source):
	return (source["id"], source["type"], source["bindings"], source["group"])


# ==================== ANSWER FUNCTIONS ====================

def _code(transform):
	return " ".join((transform.get("code") or "").split())


def _optionTexts(node):
	"""Texts of the checkboxes an option group answers with, in the order of its script."""
	binding = node.get("propConfig", {}).get("custom.item.answer", {}).get("binding") or {}
	code = (binding.get("transforms") or [{}])[0].get("code") or ""
	if binding.get("type") != "property" or "answerReturn[value.index(True)] if any(value) else \"-\"" not in code:
		return None
	children = {c.get("meta", {}).get("name"): c for c in node.get("children", [])}
	names = re.findall(r'getChild\("([^"]+)"\)', code)
	texts = [(children.get(n, {}).get("props") or {}).get("text") for n in names]
	return texts if names and None not in texts else None


def _formatTime(value):
	"""h:mm:ss a in the gateway time zone (America/Bogota) for a stored Perspective date."""
	if value is None:
		return None
	millis = value.get("$ts") if isinstance(value, dict) else value
	moment = datetime.datetime.fromtimestamp(millis / 1000.0, datetime.timezone(datetime.timedelta(hours=-5)))
	return moment.strftime("%I:%M:%S %p").lstrip("0")


def nativeAnswer(source):
	"""Return (fn, default) of the original field, or (None, reason) when its logic is not recognized."""
	if source.get("instance") is not None:
		if str(source.get("repeaterView", "")).endswith("Fundamental Views/Checkbox"):
			# Unmounted instance: recopile reads the answer stored in the instance
			stored = (source["instance"].get("item") or {}).get("answer")
			return (lambda v: "Cumple" if v else "No Cumple"), stored == "Cumple"
		return None, "repeater no reconocido"
	node = source["node"]
	ctype = node.get("type")
	if ctype == "ia.container.flex" and "checkboxAnswers" in node.get("custom", {}):
		options = _optionTexts(node)
		if options is None:
			return None, "grupo de opción no reconocido"
		answers = node["custom"].get("checkboxAnswers") or []
		chosen = [o for o, on in zip(options, answers) if on]
		return (lambda v: v if v else "-"), (chosen[0] if chosen else None)
	if ctype == "ia.input.date-time-input":
		b = node.get("propConfig", {}).get("custom.item.answer", {}).get("binding") or {}
		if b.get("config", {}).get("path") == "this.props.value" and any('SimpleDateFormat("h:mm:ss a"' in (t.get("code") or "") for t in b.get("transforms", [])):
			# The native date-time input opens with the current time, not the value stored in the design
			return _formatTime, (OPENS_NOW if "props.value" not in node.get("propConfig", {}) else (node.get("props") or {}).get("value"))
		return None, "fecha con lógica no reconocida"
	if ctype not in VALUE_PROP:
		return None, "tipo {}".format(ctype)
	prop, componentDefault = VALUE_PROP[ctype]
	binding = node.get("propConfig", {}).get("custom.item.answer", {}).get("binding") or {}
	if binding.get("type") != "property" or binding.get("config", {}).get("path") != "this.props." + prop:
		return None, "respuesta con binding propio"
	default = (node.get("props") or {}).get(prop, componentDefault)
	transforms = binding.get("transforms", [])
	if not transforms:
		return (lambda v: v), default
	if len(transforms) > 1:
		return None, "varias transformaciones"
	t = transforms[0]
	if t.get("type") == "map":
		table = [(m.get("input"), m.get("output")) for m in t.get("mappings", [])]
		fallback = t.get("fallback")

		def mapped(v):
			for k, out in table:
				if k == v:
					return out
			return fallback
		return mapped, default
	if t.get("type") == "script" and _code(t) == EMPTY_DASH:
		return (lambda v: v if v else "-"), default
	if t.get("type") == "script" and "self.props.options" in (t.get("code") or "") and 'item["label"]' in (t.get("code") or ""):
		options = (node.get("props") or {}).get("options") or []

		def label(v, opts=options):
			for o in opts:
				if str(o.get("value")) == str(v):
					return o.get("label")
			return ""
		return label, default
	return None, "script no reconocido"


def objectAnswer(node):
	"""Return (fn, default) for an embedded standard object, mirroring Objects/* answer bindings."""
	path = node["props"].get("path", "")
	p = node["props"].get("params", {})
	empty = p.get("emptyAnswer")

	def withEmpty(v):
		return v if empty is None else (v if v else empty)
	if path == "Objects/Checkbox":
		return (lambda v: p.get("trueValue") if v else p.get("falseValue")), p.get("answer")
	if path in ("Objects/NumericField", "Objects/TextField"):
		return withEmpty, p.get("answer")
	if path == "Objects/OptionGroup":
		return withEmpty, p.get("answer")
	if path == "Objects/DateTime":
		return (_formatTime if p.get("format") == "h:mm:ss a" else None), p.get("answer")
	if path == "Objects/Dropdown":
		if p.get("answerFrom") == "label":
			opts = p.get("options") or []

			def label(v):
				for o in opts:
					if str(o.get("value")) == str(v):
						return o.get("label")
				return withEmpty("")
			return label, p.get("answer")
		return withEmpty, p.get("answer")
	return None, None


def samplesFor(source, node):
	"""Sample field values to compare answers."""
	ctype = (source.get("node") or {}).get("type") or "ia.input.checkbox"
	if ctype == "ia.container.flex":
		return [None] + list(node["props"].get("params", {}).get("options") or [])
	if ctype == "ia.input.date-time-input":
		return [None, {"$ts": 1788367051480}, {"$ts": 1788300000000}]
	if ctype == "ia.input.checkbox" or source.get("instance") is not None:
		return [True, False]
	if ctype == "ia.input.numeric-entry-field":
		return [None, "", 0, 7.5, 42]
	if ctype == "ia.input.dropdown":
		opts = (node["props"].get("params", {}).get("options") or (source["node"].get("props") or {}).get("options") or [])
		return [None, ""] + [o.get("value") for o in opts]
	return [None, "", "ok"]


# ==================== STAGES ====================

def stageStructure(cur, base, curPath):
	_, crlf, canonical = design.loadView(curPath)
	problems = []
	if not canonical:
		problems.append("no es Gson canónico")
	if base is not None and crlf != base["crlf"]:
		problems.append("cambió el fin de línea")
	return problems


def stageCollection(cur, base):
	problems = []
	a, b = answerSources(base["view"]), answerSources(cur)
	if [_key(s) for s in a] != [_key(s) for s in b]:
		for i, (x, y) in enumerate(zip(a, b)):
			if _key(x) != _key(y):
				problems.append("ítem {}: antes {} en {}, ahora {} en {}".format(i, x["id"], x["group"], y["id"], y["group"]))
				break
		if len(a) != len(b):
			problems.append("{} ítems antes, {} ahora".format(len(a), len(b)))
	newBroken = view_refs.broken(cur) - view_refs.broken(base["view"])
	for owner, target, rest in sorted(newBroken)[:3]:
		problems.append("referencia rota nueva: {} → {}.{}".format("/".join(owner), "/".join(target), rest))
	if base["view"].get("propConfig", {}).get("custom.insights") != cur.get("propConfig", {}).get("custom.insights"):
		problems.append("cambió el binding de custom.insights")
	obs = [c for c in cur["root"].get("children", []) if c.get("meta", {}).get("name") == "TextField"]
	baseObs = [c for c in base["view"]["root"].get("children", []) if c.get("meta", {}).get("name") == "TextField"]
	if baseObs and (not obs or obs[0].get("type") != "ia.input.text-field"):
		problems.append("falta el TextField de Observaciones")
	return problems


def _rangeProblems(old, node, itemID):
	"""A converted numeric turns red (out of range) for the same values as the original color script."""
	native = old.get("node") or {}
	if native.get("type") != "ia.input.numeric-entry-field" or node["props"].get("path") != "Objects/NumericField":
		return []
	params = node["props"].get("params", {})
	low, high = params.get("minValue"), params.get("maxValue")
	if not ranges.colorScripts(native):
		return [] if low is None and high is None else ["{}: el original no se pinta por rango y el objeto tiene rango {}–{}".format(itemID, low, high)]
	for value in ranges.probes(native, [v for v in (low, high) if isinstance(v, (int, float))]):
		red = ranges.isRed(native, value)
		if red is None:
			return ["{}: no se pudo evaluar el color del original con {!r}".format(itemID, value)]
		if red != ranges.objectRed(low, high, value):
			return ["{}: con {!r} el original {} rojo y el objeto {} (rango {}–{})".format(itemID, value,
				"pinta" if red else "no pinta", "sí" if not red else "no", low, high)]
	return []


def stageAnswers(cur, base):
	problems = []
	checked = 0
	for old, new in zip(answerSources(base["view"]), answerSources(cur)):
		node = new.get("node")
		if not node or node.get("type") != "ia.display.view" or not str(node["props"].get("path", "")).startswith("Objects/"):
			continue
		if old.get("node") is not None and old["node"].get("type") == "ia.display.view":
			continue  # already an object in the baseline: stage 6 covers it
		fnOld, defOld = nativeAnswer(old)
		fnNew, defNew = objectAnswer(node)
		if fnOld is None:
			problems.append("{} ({}): el original tiene lógica no reconocida ({})".format(new["id"], new["path"], defOld))
			continue
		if fnNew is None:
			problems.append("{}: objeto sin regla de respuesta".format(new["id"]))
			continue
		problems += _rangeProblems(old, node, new["id"])
		for value in samplesFor(old, node):
			if fnOld(value) != fnNew(value):
				problems.append("{}: con valor {!r} el original responde {!r} y el objeto {!r}".format(new["id"], value, fnOld(value), fnNew(value)))
				break
		if defOld == OPENS_NOW:
			params = node["props"].get("params", {})
			if not params.get("startNow") or params.get("value") is not None:
				problems.append("{}: el campo abre con la hora actual y el objeto no tiene startNow".format(new["id"]))
			checked += 1
			continue
		expected = fnOld(defOld)
		if expected != defNew:
			problems.append("{}: respuesta sin abrir la sección {!r}, el original guardaba {!r}".format(new["id"], defNew, expected))
		checked += 1
	return problems, checked


# ==================== FIELD PROPS (what the operator sees and can do) ====================

# Runtime papoItemID of the components of the views being compared (id(node) -> value), see _runtimeIDs
_RUNTIME = {}


def _runtimeIDs(view):
	"""Remember the runtime papoItemID of every component of a view for _itemRef."""
	nodes = view_refs.index(view)
	for path, value in item_ids.resolve(view).items():
		if isinstance(value, int) and not isinstance(value, bool):
			_RUNTIME[id(nodes[path])] = value


def _itemRef(node):
	"""Identity of a component papoItemID: its runtime value when computable, else the static id or its binding."""
	if id(node) in _RUNTIME:
		return _RUNTIME[id(node)]
	b = node.get("propConfig", {}).get("custom.item.papoItemID")
	return json.dumps(b, sort_keys=True) if b else ((node.get("custom") or {}).get("item") or {}).get("papoItemID")


def _onValue(binding, ctype):
	"""Binding JSON with the field value prop written as the object value param."""
	prop = OWN_VALUE.get(ctype, "value")
	return re.sub(r"\b(this|self)\.props\.{}\b".format(prop), lambda m: m.group(1) + ".props.params.value", json.dumps(binding, sort_keys=True))


def _textOf(owner, prop, parent, ctype=None):
	"""What a text prop of a native component shows: ("text", s), ("item", ref), ("state", t, f) or ("binding", json)."""
	config = owner.get("propConfig", {}).get(prop) or {}
	b = config.get("binding")
	if not b:
		value = owner.get("props") or {}
		for part in prop.split(".")[1:]:
			value = value.get(part) if isinstance(value, dict) else None
		return ("text", value or "")
	t = b.get("transforms", [])
	path = b.get("config", {}).get("path")
	if b.get("type") == "property" and t and DESCRIPTION_QUERY in _code(t[0]) and path:
		item = owner.get("propConfig", {}).get("custom.item.papoItemID", {}).get("binding") or {}
		if path == "this.custom.item.papoItemID" or (item.get("config") == {"path": path} and not item.get("transforms")):
			return ("item", _itemRef(owner))
		if path == "parent.custom.item.papoItemID" and parent is not None:
			return ("item", _itemRef(parent))
		source = owner if path.startswith("this.custom.") else parent if path.startswith("parent.custom.") else None
		if source is not None and path.count(".") == 2:
			static = (source.get("custom") or {}).get(path.split(".")[2])
			if isinstance(static, int) and "custom." + path.split(".")[2] not in source.get("propConfig", {}):
				return ("item", static)
	if ctype and b.get("type") == "property" and b.get("config") == {"path": "this.props." + OWN_VALUE[ctype]} and len(t) == 1 and t[0].get("type") == "map":
		table = {m.get("input"): m.get("output") for m in t[0].get("mappings", [])}
		if set(table) == {True, False}:
			return ("state", table[True], table[False])
	return ("binding", _onValue(b, ctype))


def _objectQuestion(embed):
	"""What the object shows as its question (or checkbox text), in the terms of _textOf."""
	p = embed["props"].get("params", {})
	pc = embed.get("propConfig", {})
	if p.get("trueText") or p.get("falseText"):
		return ("state", p.get("trueText"), p.get("falseText"))
	if "props.params.question" in pc:
		return ("binding", json.dumps(pc["props.params.question"]["binding"], sort_keys=True))
	if p.get("question"):
		return ("text", p["question"])
	b = pc.get("props.params.papoItemID", {}).get("binding")
	if b and b.get("config") == {"path": "this.custom.item.papoItemID"} and not b.get("transforms"):
		return ("item", _itemRef(embed))
	if p.get("papoItemID") is not None:
		return ("item", p["papoItemID"])
	return ("text", "")


def _placeholderOf(node):
	ctype = node.get("type")
	if ctype == "ia.input.dropdown":
		text = ((node.get("props") or {}).get("placeholder") or {}).get("text")
		return ("text", "default") if not text or text == "Seleccionar" else ("text", text)
	if "props.placeholder" in node.get("propConfig", {}):
		return _textOf(node, "props.placeholder", None, ctype)
	text = (node.get("props") or {}).get("placeholder")
	return ("text", "default") if not text or RE_DEFAULT_PLACEHOLDER.match(text) else ("text", text)


def _objectPlaceholder(embed):
	p = embed["props"].get("params", {})
	pc = embed.get("propConfig", {})
	if p.get("questionAsPlaceholder"):
		return _objectQuestion(embed)
	if "props.params.placeholder" in pc:
		return ("binding", json.dumps(pc["props.params.placeholder"]["binding"], sort_keys=True))
	text = p.get("placeholder")
	return ("text", "default") if not text or RE_DEFAULT_PLACEHOLDER.match(text) or text == "Seleccionar" else ("text", text)


def _boundOrStatic(node, prop, default, ctype):
	cfg = node.get("propConfig", {}).get("props." + prop)
	if cfg and cfg.get("binding"):
		return ("binding", _onValue(cfg["binding"], ctype))
	value = (node.get("props") or {}).get(prop)
	return ("static", default if value is None else value)


def _objectBoundOrStatic(embed, param, default):
	cfg = embed.get("propConfig", {}).get("props.params." + param)
	if cfg and cfg.get("binding"):
		return ("binding", json.dumps(cfg["binding"], sort_keys=True))
	value = embed["props"].get("params", {}).get(param)
	return ("static", default if value is None else value)


_DESCRIPTIONS = {}


def _description(pid):
	"""papoitem.Description of one item (SELECT on the test database, cached)."""
	if pid not in _DESCRIPTIONS:
		env = dict(os.environ)
		for line in open(DB_ENV):
			k, _, v = line.strip().partition("=")
			env[k] = v
		q = "SET NOCOUNT ON; SELECT Description FROM papoitem WHERE ID = {} FOR JSON PATH, INCLUDE_NULL_VALUES".format(int(pid))
		r = subprocess.run(["docker", "exec", "-e", "SQLCMDUSER", "-e", "SQLCMDPASSWORD", "mssql", "/opt/mssql-tools18/bin/sqlcmd",
			"-S", "localhost", "-d", "cla-db-papo", "-C", "-y", "0", "-Q", q], capture_output=True, text=True, env=env)
		rows = json.loads("".join(l for l in r.stdout.splitlines() if not l.startswith("JSON_")) or "[]")
		_DESCRIPTIONS[pid] = rows[0]["Description"] if rows else None
	return _DESCRIPTIONS[pid]


def _sameQuestion(expected, shown):
	"""Equal question sources, or a fixed text now read from papoItemID whose description is that text."""
	if expected == shown:
		return True
	if expected[0] == "text" and expected[1] and shown[0] == "item" and isinstance(shown[1], int):
		return ((_description(shown[1]) or "").strip() == expected[1].strip())
	return False


def stageFieldProps(cur, base):
	"""Problems where a converted field no longer shows or does what the original did."""
	problems = []
	baseNodes = view_refs.index(base["view"])
	_RUNTIME.clear()
	_runtimeIDs(base["view"])
	_runtimeIDs(cur)
	for old, new in zip(answerSources(base["view"]), answerSources(cur)):
		embed, field = new.get("node"), old.get("node")
		if not embed or not field or embed.get("type") != "ia.display.view" or field.get("type") == "ia.display.view":
			continue
		if not str(embed["props"].get("path", "")).startswith("Objects/"):
			continue
		ctype = field.get("type")
		where = "{} ({})".format(new["id"], new["path"])
		oldPath, newPath = tuple(old["path"].split("/")), tuple(new["path"].split("/"))
		parent = baseNodes.get(oldPath[:-1])
		params = embed["props"].get("params", {})
		# Question or checkbox text
		if ctype == "ia.container.flex":
			labels = [c for c in field.get("children", []) if c.get("type") == "ia.display.label"]
			expected = _textOf(labels[0], "props.text", field) if labels else ("text", "")
			shown = _objectQuestion(embed) if params.get("showQuestion", True) else ("text", "")
		elif oldPath != newPath:
			row = baseNodes.get(newPath)
			labels = [c for c in (row or {}).get("children", []) if c.get("type") == "ia.display.label"]
			expected = _textOf(labels[0], "props.text", row) if labels else (_textOf(field, "props.text", parent, ctype) if ctype == "ia.input.checkbox" else ("text", ""))
			shown = _objectQuestion(embed) if ctype == "ia.input.checkbox" or params.get("showQuestion", True) else ("text", "")
		elif ctype == "ia.input.checkbox":
			expected, shown = _textOf(field, "props.text", parent, ctype), _objectQuestion(embed)
		else:
			expected = ("text", "")
			shown = _objectQuestion(embed) if params.get("showQuestion", True) else ("text", "")
		if not _sameQuestion(expected, shown):
			if expected[0] == "text" and shown[0] == "item" and isinstance(shown[1], int):
				problems.append("{}: papoitem {} dice {!r} y el formulario mostraba {!r} (aplicar el SQL de preguntas)".format(
					where, shown[1], (_description(shown[1]) or "")[:60], expected[1][:60]))
			else:
				problems.append("{}: la pregunta era {} y el objeto muestra {}".format(where, str(expected)[:90], str(shown)[:90]))
		if ctype == "ia.container.flex":
			width = str(labels[0].get("position", {}).get("basis", "")) if labels else ""
			if (width.endswith("px") or width.endswith("%")) and params.get("questionBasis") != width:
				problems.append("{}: la pregunta medía {} y ahora {}".format(where, width, params.get("questionBasis", "60%")))
			continue
		# Placeholder, enabled, value and option bindings
		if ctype in ("ia.input.numeric-entry-field", "ia.input.text-field", "ia.input.dropdown") and _placeholderOf(field) != _objectPlaceholder(embed):
			problems.append("{}: el placeholder era {} y ahora es {}".format(where, str(_placeholderOf(field))[:80], str(_objectPlaceholder(embed))[:80]))
		if _boundOrStatic(field, "enabled", True, ctype) != _objectBoundOrStatic(embed, "enabled", True):
			problems.append("{}: cambió enabled".format(where))
		valueBinding = field.get("propConfig", {}).get("props." + OWN_VALUE.get(ctype, "value"), {}).get("binding")
		objectValue = embed.get("propConfig", {}).get("props.params.value", {}).get("binding")
		if (valueBinding and _onValue(valueBinding, ctype)) != (objectValue and json.dumps(objectValue, sort_keys=True)):
			problems.append("{}: se perdió el binding del valor".format(where))
		if ctype == "ia.input.dropdown":
			if "props.options" in field.get("propConfig", {}) and _boundOrStatic(field, "options", [], ctype) != _objectBoundOrStatic(embed, "options", []):
				problems.append("{}: cambiaron las opciones".format(where))
			if bool((field.get("props") or {}).get("showClearIcon")) != bool(params.get("showClearIcon")):
				problems.append("{}: cambió showClearIcon".format(where))
		# Anything else the original field had
		known = STANDARD_PROPS | CARRIED_PROPS | {OWN_VALUE.get(ctype, "value")}
		extra = [k for k in (field.get("props") or {}) if k not in known]
		extra += [k for k, v in field.get("propConfig", {}).items() if k.startswith("props.") and k[6:].split(".")[0] not in known]
		extra += [k for k, v in field.get("propConfig", {}).items() if v.get("onChange") and not k.startswith("custom.item")]
		if field.get("events") or field.get("scripts"):
			extra.append("events/scripts")
		if extra:
			problems.append("{}: el campo tenía {} y el objeto no lo recibe".format(where, ", ".join(sorted(set(extra)))))
	return problems


def _isStandard(view):
	return "PAPO/Form" in str(((view["root"].get("props") or {}).get("style") or {}).get("classes", "")).split()


def _handlers(view):
	out = []

	def walk(node):
		for h in (node.get("scripts") or {}).get("messageHandlers", []):
			out.append((node.get("meta", {}).get("name"), h.get("messageType")))
		for c in node.get("children", []):
			walk(c)
	walk(view["root"])
	return out


def stageFlow(cur, base, rel):
	problems = []
	# Findings compared by location: a new one fails even if another one was removed
	# A binding moved to the object (props.X -> props.params.X) keeps its location
	def findings(view):
		nodes = {"/".join(k): v for k, v in view_refs.index(view).items()}

		def where(w):
			owner, _, location = w.partition(" · ")
			path = ((nodes.get(owner) or {}).get("props") or {}).get("path", "")
			for param, prop in PARAM_PROPS.get(path, {}).items():
				location = location.replace("props.params.{}.".format(param), "props.{}.".format(prop))
			return owner + (" · " + location.replace("props.params.", "props.") if location else "")
		return {(k, where(w)) for k, w in lint.lintView(view, rel)}
	now = findings(cur)
	before = findings(base["view"])
	for pattern, where in sorted(now):
		if pattern in V2_PATTERNS and ((pattern, where) not in before or _isStandard(cur)):
			problems.append("wrapper del v2: {} ({})".format(pattern, where))
		if pattern == "hardcodedDb" and (pattern, where) not in before:
			problems.append('"papo_db" nuevo en {}'.format(where))
	if _isStandard(cur):
		legacy = [m for owner, m in _handlers(cur) if not (owner == "root" and m == "saveDataRoot")]
		if legacy:
			problems.append("handlers legacy: {}".format(", ".join(sorted(set(legacy)))))
	return problems


def _classes(view):
	tokens = set()

	def walk(node):
		for t in str(((node.get("props") or {}).get("style") or {}).get("classes", "")).split():
			tokens.add(t)
		for c in node.get("children", []):
			walk(c)
	walk(view["root"])
	return tokens


def _classExists(name):
	return os.path.exists(os.path.join(STYLES, name, "style.json"))


def _rowsHeight(group):
	total = 0.0
	for child in group.get("children", []):
		basis = str(child.get("position", {}).get("basis", ""))
		if basis.endswith("px"):
			try:
				total += float(basis[:-2])
			except ValueError:
				pass
	return total


def _sectionOverflow(view):
	"""Per group with a fixed expanded height: px of rows beyond custom.baseBasisPx."""
	out = {}
	for g in view["root"].get("children", []):
		height = (g.get("custom") or {}).get("baseBasisPx")
		if GROUP.match(g.get("meta", {}).get("name", "")) and isinstance(height, (int, float)):
			out[g["meta"]["name"]] = _rowsHeight(g) - height
	return out


def stageDesign(cur, base):
	problems = []
	before = _sectionOverflow(base["view"])
	for name, overflow in sorted(_sectionOverflow(cur).items()):
		if overflow > max(0, before.get(name, 0)):
			problems.append("{}: las filas miden {:.0f} px más que la sección abierta (custom.baseBasisPx)".format(name, overflow))
	missingNow = {c for c in _classes(cur) if not _classExists(c)}
	missingBefore = {c for c in _classes(base["view"]) if not _classExists(c)}
	if missingNow - missingBefore:
		problems.append("clases inexistentes nuevas: {}".format(", ".join(sorted(missingNow - missingBefore))))
	if not _isStandard(cur):
		return problems + ["la raíz no tiene PAPO/Form"]
	for s in answerSources(cur):
		node = s.get("node")
		if node is None:
			problems.append("{}: sigue en un repeater".format(s["id"]))
			continue
		if node.get("type") == "ia.container.flex":
			continue  # containers with custom.item (empty legacy items, option groups with items inside) are not fields
		props = node.get("props") or {}
		style = props.get("style") or {}
		isObject = node.get("type") == "ia.display.view" and str(props.get("path", "")).startswith("Objects/")
		if not isObject and not any(c.startswith("PAPO/Field/") for c in str(style.get("classes", "")).split()):
			problems.append("{}: campo sin estándar ({})".format(s["id"], node.get("type")))
		width = str(style.get("width", ""))
		if width.endswith("px"):
			problems.append("{}: ancho fijo {}".format(s["id"], width))
	return problems


_OBJECT_CACHE = {}


def _objectView(path):
	if path not in _OBJECT_CACHE:
		p = os.path.join(VIEWS, path, "view.json")
		_OBJECT_CACHE[path] = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None
	return _OBJECT_CACHE[path]


def stageContract(cur):
	problems = []

	def walk(node):
		props = node.get("props") or {}
		if node.get("type") == "ia.display.view" and str(props.get("path", "")).startswith("Objects/"):
			obj = _objectView(props["path"])
			if obj is None:
				problems.append("{}: no existe".format(props["path"]))
			else:
				known = set(obj.get("params", {}))
				passed = set(props.get("params", {})) | {k.split(".", 2)[2] for k in node.get("propConfig", {}) if k.startswith("props.params.")}
				unknown = passed - known
				if unknown:
					problems.append("{} recibe parámetros que no existen: {}".format(props["path"], ", ".join(sorted(unknown))))
				directions = {k[len("params."):]: v.get("paramDirection") for k, v in obj.get("propConfig", {}).items() if k.startswith("params.")}
				if directions.get("answer") != "output":
					problems.append("{}: answer no es de salida".format(props["path"]))
				if "value" in known and directions.get("value") != "inout":
					problems.append("{}: value no es inout".format(props["path"]))
				if "item" in node.get("custom", {}):
					b = node.get("propConfig", {}).get("custom.item.answer", {}).get("binding", {})
					if b.get("config", {}).get("path") != "this.props.params.answer":
						problems.append("{}: custom.item.answer no lee params.answer".format(node["custom"]["item"].get("papoItemID")))
		for c in node.get("children", []):
			walk(c)
	walk(cur["root"])
	return sorted(set(problems))


def stageGraph(baseline):
	"""Rebuild the graph in a temp folder and compare unresolved references and messages with the baseline."""
	if not os.path.exists(GRAPH_SCRIPT):
		return ["no se encontró ignition-graph"]
	out = tempfile.mkdtemp(prefix="papo-qa-graph-")
	subprocess.run([sys.executable, GRAPH_SCRIPT, REPO, "--out", out], capture_output=True, text=True)
	now = json.load(open(os.path.join(out, "impact.json"), encoding="utf-8"))
	raw = subprocess.run(["git", "-C", REPO, "show", "{}:.claude/ignition-graph/impact.json".format(baseline)], capture_output=True, text=True)
	if raw.returncode:
		return ["el baseline no tiene grafo"]
	before = json.loads(raw.stdout)

	def refs(d):
		return {(kind, target, src) for kind, targets in d["unresolved"].items() for target, srcs in targets.items() for src in srcs}

	def msgs(d):
		return {(k, m) for k, v in d["analisis"]["mensajes"].items() for m in v}
	problems = ["referencia no resuelta nueva: {} {} desde {}".format(*r) for r in sorted(refs(now) - refs(before))]
	problems += ["mensaje desbalanceado nuevo: {} ({})".format(m, k) for k, m in sorted(msgs(now) - msgs(before))]
	return problems


def stageData(pilotID, originalID, exact=False):
	"""Compare the DataAnswer of two registerhistory rows (SELECT only)."""
	env = dict(os.environ)
	for line in open(DB_ENV):
		k, _, v = line.strip().partition("=")
		env[k] = v
	q = ("SET NOCOUNT ON; SELECT ID, PapoID, RegisterTypeID, DataAnswer FROM registerhistory WHERE ID IN ({}, {}) "
		"FOR JSON PATH").format(int(pilotID), int(originalID))
	r = subprocess.run(["docker", "exec", "-e", "SQLCMDUSER", "-e", "SQLCMDPASSWORD", "mssql", "/opt/mssql-tools18/bin/sqlcmd",
		"-S", "localhost", "-d", "cla-db-papo", "-C", "-y", "0", "-Q", q], capture_output=True, text=True, env=env)
	rows = {row["ID"]: row for row in json.loads("".join(l for l in r.stdout.splitlines() if not l.startswith("JSON_")) or "[]")}
	if len(rows) != 2:
		return ["no se encontraron los dos registros"]

	def items(row):
		return [i for i in json.loads(row["DataAnswer"])["items"] if "papoItemID" in i]

	def kind(v):
		if v in ("Cumple", "No Cumple", "No cumple", "-", ""):
			return repr(v) if v in ("", "-") else "cumple/no cumple"
		return type(v).__name__
	a, b = items(rows[int(pilotID)]), items(rows[int(originalID)])
	problems = []
	idsA, idsB = [i["papoItemID"] for i in a], [i["papoItemID"] for i in b]
	onlyA, onlyB = [i for i in idsA if i not in idsB], [i for i in idsB if i not in idsA]
	if onlyA or onlyB:
		problems.append("ítems solo en el piloto: {} · solo en el original: {} ({} contra {})".format(onlyA or "-", onlyB or "-", len(a), len(b)))
	if [i for i in idsA if i in idsB] != [i for i in idsB if i in idsA]:
		problems.append("los ítems comunes están en otro orden")
	# Same IDs in the same order: compare position by position (a repeated papoItemID keeps its own answer)
	if idsA == idsB:
		pairs = list(zip(a, b))
	else:
		byID = {i["papoItemID"]: i for i in b}
		pairs = [(x, byID[x["papoItemID"]]) for x in a if x["papoItemID"] in byID]
	for x, y in pairs:
		if x.get("registerTypeID") != y.get("registerTypeID"):
			problems.append("{}: registerTypeID {} contra {}".format(x["papoItemID"], x.get("registerTypeID"), y.get("registerTypeID")))
		if exact:
			times = [isinstance(v, str) and bool(RE_TIME_OF_DAY.match(v)) for v in (x.get("answer"), y.get("answer"))]
			if all(times):
				continue  # time of day: each save opened the form at another time
			if x.get("answer") != y.get("answer"):
				problems.append("{}: respuesta {!r} contra {!r}".format(x["papoItemID"], x.get("answer"), y.get("answer")))
			continue
		# Empty, unanswered option ("-") or unavailable (tag without value) answers depend on what was filled
		if kind(x.get("answer")) != kind(y.get("answer")) and not {x.get("answer"), y.get("answer")} & {None, "", "-"}:
			problems.append("{}: formato {} contra {}".format(x["papoItemID"], kind(x.get("answer")), kind(y.get("answer"))))
	return problems


CHECKLIST = """- [ ] Designer y Chrome se ven igual (Sections, botones, campos, valores de tag)
- [ ] Abrir la sección, llenar, cerrar y reabrir: los valores siguen
- [ ] Numérico fuera de rango en rojo
- [ ] Guardar un registro y correr `--compare-db <piloto> <original>`
- [ ] Reporte PDF del registro guardado
- [ ] Tiempo de apertura de la sección más grande (anotar segundos)"""


# ==================== MAIN ====================

def baselineOf(path, ref):
	rel = os.path.relpath(path, REPO)
	r = subprocess.run(["git", "-C", REPO, "show", "{}:{}".format(ref, rel)], capture_output=True)
	if r.returncode:
		return None
	raw = r.stdout.decode("utf-8")
	return {"view": json.loads(raw), "crlf": "\r\n" in raw}


def checkView(curPath, base):
	cur = json.load(open(curPath, encoding="utf-8"))
	rel = os.path.relpath(os.path.dirname(curPath), VIEWS)
	results = collections.OrderedDict()
	results["1"] = stageStructure(cur, base, curPath)
	if base is None:
		results["2"] = ["sin baseline (vista nueva): no se puede comparar"]
		base = {"view": cur, "crlf": False}
	else:
		results["2"] = stageCollection(cur, base)
	answers, checked = stageAnswers(cur, base)
	results["3"] = answers + stageFieldProps(cur, base)
	results["4"] = stageFlow(cur, base, rel)
	results["5"] = stageDesign(cur, base)
	results["6"] = stageContract(cur)
	return results, checked, len(answerSources(cur))


def main():
	parser = argparse.ArgumentParser(description="Pipeline de QA de formularios PAPO")
	parser.add_argument("--views", nargs="*")
	parser.add_argument("--all-forms", action="store_true")
	parser.add_argument("--baseline", default="HEAD")
	parser.add_argument("--pair", nargs=2, action="append", metavar=("ACTUAL", "BASELINE"))
	parser.add_argument("--graph", action="store_true")
	parser.add_argument("--compare-db", nargs=2, type=int, metavar=("PILOTO", "ORIGINAL"))
	parser.add_argument("--exact", action="store_true")
	parser.add_argument("--report")
	args = parser.parse_args()

	runs = []
	for path in design.resolveViews(args) if (args.views or args.all_forms) else []:
		runs.append((path, baselineOf(path, args.baseline)))
	for current, basePath in args.pair or []:
		raw = open(basePath, encoding="utf-8", newline="").read()
		runs.append((os.path.abspath(current), {"view": json.loads(raw), "crlf": "\r\n" in raw}))

	lines = ["# QA de formularios PAPO", "", "Generado: {} · Baseline: `{}` · Vistas: {}".format(
		datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), args.baseline, len(runs)), ""]
	failed = False
	swapped = pilot_swap.activeSwaps()
	if swapped:
		lines += ["⚠ Intercambio de pilotos activo (no commitear): {}. Restaurar con `pilot_swap.py off --all`.".format(", ".join(swapped)), ""]
		print("⚠ intercambio de pilotos activo: " + ", ".join(swapped))
	summary = collections.Counter()
	detail = []
	for path, base in runs:
		results, checked, items = checkView(path, base)
		if os.path.relpath(os.path.dirname(path), VIEWS) in swapped:
			results["1"] = results["1"] + ["el piloto está intercambiado en esta ruta"]
		bad = [s for s, p in results.items() if p]
		failed = failed or bool(bad)
		summary["pasa" if not bad else "falla"] += 1
		name = os.path.relpath(os.path.dirname(path), VIEWS) if path.startswith(VIEWS) else path
		detail.append("### `{}` · {} · {} ítems, {} respuestas comparadas".format(name, "PASA" if not bad else "FALLA", items, checked))
		for stage, problems in results.items():
			mark = "✅" if not problems else "❌"
			detail.append("- {} {} {}".format(mark, stage, STAGES[stage]) + ("" if not problems else ": " + "; ".join(problems[:5]) + (" (+{})".format(len(problems) - 5) if len(problems) > 5 else "")))
		detail.append("")
	extra = []
	if args.graph:
		problems = stageGraph(args.baseline)
		failed = failed or bool(problems)
		extra.append("- {} 7 Grafo{}".format("✅" if not problems else "❌", "" if not problems else ": " + "; ".join(problems[:8])))
	if args.compare_db:
		problems = stageData(args.compare_db[0], args.compare_db[1], args.exact)
		failed = failed or bool(problems)
		extra.append("- {} 8 Datos (registros {} y {}){}".format("✅" if not problems else "❌", args.compare_db[0], args.compare_db[1], "" if not problems else ": " + "; ".join(problems[:8])))
	lines.append("Resultado: **{}** · {} vistas pasan, {} fallan".format("PASA" if not failed else "FALLA", summary["pasa"], summary["falla"]))
	lines.append("")
	if extra:
		lines += ["## Etapas globales", ""] + extra + [""]
	lines += ["## Por vista", ""] + detail + ["## 9 Visual (manual)", "", CHECKLIST, ""]
	report = "\n".join(lines)
	if args.report:
		os.makedirs(os.path.dirname(os.path.abspath(args.report)), exist_ok=True)
		open(args.report, "w", encoding="utf-8").write(report)
		print("Reporte: {} · {}".format(args.report, "PASA" if not failed else "FALLA"))
	else:
		print(report)
	return 1 if failed else 0


if __name__ == "__main__":
	sys.exit(main())
