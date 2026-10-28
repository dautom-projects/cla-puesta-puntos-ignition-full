"""
papo_core.report

Report data extraction for PAPO PDF reports.
build() is the one call of a report script: the report lists its
sections and the engine reads the cycle, fills the keys of the
template, the comment, the signatures and the history list. The
older entry points stay: config-driven (extractReportData) and
auto-configured (extractReportDataAuto), which discovers
RegisterTypeIDs from papoitem_registertype, derives section names
from registertype.Description, and handles multi-shift forms with
turno prefix grouping.

Every query reads only the cycle of the report station when the viewer
passes workstationNodeID (Gestion): two stations of the same node number
their cycles apart, so a cycle is (PapoID, NodeID, WorkstationNodeID,
RegisterCode). Without it the cycle is read by node, as before.

Version: 2.8.5

Changelog:
	2026-10-28 | William M. | v2.8.5 - _detectShiftFromTimestamp uses papo_core.ui.getShift (no getHour24 left)
	2026-10-28 | William M. | v2.8.4 - _normalizeDict keeps unicode values (the quality marks of CU11-0101
		printed as UTF-8 bytes)
	2026-10-28 | William M. | v2.8.3 - Reprocessed marks read Sí (with accent) as si (MZ07-0101)
	2026-10-28 | William M. | v2.8.2 - normalize okText (PT11-0104) and values marks with their own
		text (AC10-1801 bueno = Si / malo = No)
	2026-10-27 | William M. | v2.8.1 - Slot shiftNumber (TR11-0102 Fin by its shift); monthGrid takes the
		month of the last Fin, as the report script did
	2026-10-27 | William M. | v2.8.0 - Reprocessed mode values (one key per answer text:
		Exportación / Nacional in AC10-1003, Antes / Durante in PO11-0101)
	2026-10-27 | William M. | v2.7.0 - build(): nestedMarks and reprocessed mode x (PT11-0104),
		start and itemType / first (MZ11-0101)
	2026-10-27 | William M. | v2.6.0 - build(): copies (the same slot with another normalize),
		normalize ar / mark, typeName also gives _typeID, header (date and shift of the
		first record of a type)
	2026-10-27 | William M. | v2.5.0 - build() slots by time (shift, weekday, weekSlot) and
		monthGrid() for TR11-0102
	2026-10-27 | William M. | v2.4.0 - build(): several reprocessed groups per section,
		marks yn / ok / number, register type name per slot and the last-signature
		mode (roleLast), so every report script fits in a build() call
	2026-10-27 | William M. | v2.3.1 - Record shift from papo_core.ui.getShift
		(America/Bogota, not the gateway timezone) and hora_registro (HH:mm:ss of
		the record) in every section; OREC reports used their own shift numbering
	2026-10-27 | William M. | v2.3.0 - build(): sections with one slot
		per record (or one merged key), reprocessed classification with its
		mark, comment, signatures and the history list, so a report script
		is only its list of sections. Station filter (workstationNodeID) in
		every query
	2026-10-22 | William M. | v2.2.0 - extractShiftChecklist: per-shift
		OK / X / N/A columns for checklists filled once per shift (FU10-0202)
	2026-08-12 | William M. | v2.1.1 - Fix _extractSignatures classifying
		operator as admin: use Status column (Finalizado=operator,
		Revisado=supervisor) instead of unreliable role field from JSON
	2026-08-11 | William M. | v2.1.0 - Auto-configured engine
		(extractReportDataAuto): discovers sections from DB, derives
		names from registertype.Description (spaces/commas stripped),
		multi-shift turno grouping via Timestamp column
	2026-08-05 | William M. | v2.0.0 - Config-driven rewrite (sections:
		types/name/max/normalize, optional reprocessedIds/reprocessedMode)
		since v1.0.0 was never actually adopted by any report - it could
		not express grouped RegisterTypeID IN(...) sections, numbered
		multi-slots, alternate normalization (yn/ok), or the "reprocesado"
		sub-classification used by about half of the 53 existing report
		scripts surveyed. Signatures now numbered by default
		(firmaAdministrator{N}/firmaOperator{N}) plus a convenience alias
		(firmaAdministrator/firmaOperator = last one seen) for simple forms.
		Form-specific correlations (e.g. a signature tied to the same slot
		number as a specific finding) stay out of this engine - those are
		a few extra lines on top of it, not a generic engine concern.
	2026-07-06 | William | v1.0.0 - Initial Project Library version
"""

SUPERVISOR_ROLES = {"Supervisor_PAPO", "Administrator", "INTEGRADOR"}

# Cumple/No Cumple -> symbol/text per normalize mode
NORMALIZE_MODES = {
	"check": {"cumple": u"✔", "no cumple": u"✘"},
	"yn": {"cumple": "Si", "no cumple": "No"},
	"ok": {"cumple": "OK", "no cumple": "N OK"},
	"ar": {"cumple": "A", "no cumple": "R"},
	"mark": {"cumple": u"✘", "no cumple": ""},
	"okText": {"cumple": u"Ok", "no cumple": u"No Ok"},
}

# Bueno/Malo/Regular -> symbol/text for reprocessedMode="quality"
QUALITY_MODES = {
	"bueno": u"✔",
	"malo": u"✘",
	"regular": "Regular",
}


# ==================== INTERNAL HELPERS ====================

def _cycleFilter(papoID, nodeID, registerCode, station=None, alias=""):
	"""SQL condition and parameters of one cycle; the station only applies when it is given."""
	sql = "{0}PapoID = ? AND {0}NodeID = ? AND {0}RegisterCode = ? AND (? IS NULL OR {0}WorkstationNodeID = ?)".format(alias)
	return sql, [papoID, nodeID, registerCode, station, station]


def _normalizeDict(sourceDict, mode):
	"""Normalize answer values to symbols/text per mode, or leave as-is for 'raw'."""
	import java.util.Date

	valueMap = NORMALIZE_MODES.get(mode, {})
	result = {}
	for k, v in sourceDict.items():
		if isinstance(v, (list, tuple)):
			val = v[0] if v else None
		else:
			val = v

		if val is None:
			result[k] = ""
			continue

		if isinstance(val, java.util.Date):
			result[k] = val
			continue

		if isinstance(val, (int, long, float)):
			result[k] = val
			continue

		# unicode, not str: a mark like the quality cross would turn into UTF-8 bytes
		valStr = unicode(val).strip()
		valLower = valStr.lower()

		if mode != "raw" and valLower in valueMap:
			result[k] = valueMap[valLower]
		else:
			result[k] = valStr

	return result


def _fillDataFromDataset(ds, data, keyName, includeInsights=True, sep=u' *---* '):
	"""Parse DataAnswer JSON rows and aggregate into a single dict."""
	from collections import defaultdict
	try:
		agg = defaultdict(list)
		insightsAll = []

		import java.text, java.util
		DATE_FORMATS = [
			"EEE MMM dd HH:mm:ss Z yyyy",
			"yyyy-MM-dd HH:mm:ss",
			"yyyy/MM/dd HH:mm:ss",
			"dd-MM-yyyy HH:mm:ss",
			"dd/MM/yyyy HH:mm:ss",
			"yyyy-MM-dd'T'HH:mm:ss",
			"yyyy-MM-dd'T'HH:mm:ss.SSSZ",
			"MMM d, yyyy, hh:mm:ss a"
		]

		def parseDateString(s):
			for fmt in DATE_FORMATS:
				try:
					sdf = java.text.SimpleDateFormat(fmt, java.util.Locale.US)
					return sdf.parse(s)
				except:
					continue
			return None

		rowCount = 0 if ds is None else ds.getRowCount()

		for i in range(rowCount):
			raw = ds.getValueAt(i, 'DataAnswer')
			if not raw:
				continue

			try:
				obj = system.util.jsonDecode(raw)
			except:
				continue

			if not (isinstance(obj, dict) and "items" in obj):
				continue

			items = obj["items"]
			ctxUser = u''
			ctxDt = None

			for it in items:
				if "insights" in it:
					if isinstance(it.get("user"), basestring):
						u = it["user"].strip()
						if u:
							ctxUser = u

					t = it.get("timestamp")
					if t is not None and ctxDt is None:
						try:
							if isinstance(t, (int, long, float)):
								ctxDt = system.date.fromMillis(long(t))
							elif isinstance(t, basestring):
								s = t.strip()
								s = s.replace(" COT ", " -0500 ").replace(" COT", " -0500").replace("COT ", "-0500 ")
								ctxDt = parseDateString(s)
						except:
							ctxDt = None

					iv = it.get("insights")
					if isinstance(iv, basestring):
						s = iv.strip()
						if s:
							insightsAll.append(s)

			for it in items:
				if "papoItemID" in it:
					key = "papoItemID{0}".format(it["papoItemID"])
					val = it.get("answer")
					if isinstance(val, (int, long, float)):
						val = str(round(float(val), 1))
					agg[key].append(val)

			agg["user"].append(ctxUser)
			agg["date"].append(ctxDt)

			# Plant shift (T1 22-06, T2 06-14, T3 14-22) and time of the record, in plant local time
			shiftVal = None
			timeVal = u''
			if ctxDt is not None:
				try:
					shift = papo_core.ui.getShift(ctxDt)
					shiftVal = str(shift) if shift is not None else None
					timeFormat = java.text.SimpleDateFormat("HH:mm:ss")
					timeFormat.setTimeZone(java.util.TimeZone.getTimeZone("America/Bogota"))
					timeVal = timeFormat.format(ctxDt)
				except:
					shiftVal = None
			agg["shift"].append(shiftVal)
			agg["hora_registro"].append(timeVal)

		result = dict(agg)
		if includeInsights:
			result[u'insights'] = sep.join(dict.fromkeys(insightsAll)) if insightsAll else u''
		data[keyName] = result

	except:
		try:
			data[keyName] = {u'user': [], u'date': [], u'shift': [], u'insights': u''}
		except:
			pass


def _classifyReprocessed(ds, allowedIds, mode, keys=None):
	"""Classify specific papoItemIDs into marks: check (cumple/nocumple), quality (bueno/malo/regular), yn, ok or number."""
	result = {}
	if ds is None:
		return result

	allowedSet = set(allowedIds)
	for i in range(ds.getRowCount()):
		raw = ds.getValueAt(i, 'DataAnswer')
		if not raw:
			continue
		try:
			obj = system.util.jsonDecode(raw)
		except:
			continue

		if not (isinstance(obj, dict) and "items" in obj):
			continue

		for item in obj["items"]:
			if "papoItemID" not in item or item["papoItemID"] not in allowedSet:
				continue
			val = item.get("answer")
			papoItemID = item["papoItemID"]
			valLower = unicode(val).strip().lower() if val is not None else u""
			if valLower == u"s\xed":
				valLower = u"si"

			if mode == "quality":
				if valLower in QUALITY_MODES:
					result["{0}papoItemID{1}".format(valLower, papoItemID)] = QUALITY_MODES[valLower]
			elif mode == "yn":
				# siItemID{ID} / noItemID{ID} (AC10-1003)
				if valLower == "cumple" or valLower == "si":
					result["siItemID{0}".format(papoItemID)] = 'Cumple'
				elif valLower == "no cumple" or valLower == "no":
					result["noItemID{0}".format(papoItemID)] = 'No Cumple'
			elif mode == "ok":
				# The item key itself with OK / NO OK (EC07-0101)
				if valLower == "cumple":
					result["papoItemID{0}".format(papoItemID)] = 'OK'
				elif valLower == "no cumple":
					result["papoItemID{0}".format(papoItemID)] = 'NO OK'
			elif mode == "values":
				# One key per answer text: keys = {"Exportación": "expoItemID", ...} -> expoItemID{ID} (AC10-1003, PO11-0101)
				# keys: {answer text: key prefix} (mark No Cumple) or {answer text: [key prefix, text]}
				for answer, target in (keys or {}).items():
					if unicode(val).strip() == answer:
						prefix, text = (target[0], target[1]) if isinstance(target, (list, tuple)) else (target, 'No Cumple')
						result["{0}{1}".format(prefix, papoItemID)] = text
			elif mode == "x":
				# Both keys always, X or blank, for every item of the list (PT11-0104)
				result["cumplepapoItemID{0}".format(papoItemID)] = 'X' if valLower == "cumple" else u''
				result["nocumplepapoItemID{0}".format(papoItemID)] = 'X' if valLower == "no cumple" else u''
			elif mode == "number":
				# One mark per numeric answer: number{value}papoItemID, without the ID as the template uses it (TE11-0401)
				if val is not None:
					result["number{0}papoItemID".format(val)] = 'No Cumple'
			else:
				if valLower == "cumple" or valLower == "si":
					result["cumplepapoItemID{0}".format(papoItemID)] = 'Cumple'
				elif valLower == "no cumple" or valLower == "no":
					result["nocumplepapoItemID{0}".format(papoItemID)] = 'No Cumple'

	return result


def _queryByTypes(typeIDs, papoID, nodeID, registerCode, db, station=None):
	"""Query registerhistory filtered by one or more RegisterTypeID (IN clause)."""
	placeholders = ",".join(["?"] * len(typeIDs))
	cycleSql, params = _cycleFilter(papoID, nodeID, registerCode, station)
	sql = '''
		SELECT DataAnswer, RegisterTypeID, Timestamp
		FROM registerhistory
		WHERE {0} AND RegisterTypeID IN ({1})
		ORDER BY ID ASC
	'''.format(cycleSql, placeholders)
	return system.db.runPrepQuery(sql, params + list(typeIDs), db)


def _processSection(ds, data, section):
	"""Build one section: single merged dict (max=1) or numbered slots (max>1)."""
	name = section["name"]
	maxRepeat = section.get("max", 1)
	mode = section.get("normalize", "check")
	reprocessedIds = section.get("reprocessedIds")
	reprocessedMode = section.get("reprocessedMode", "check")
	reprocessedName = section.get("reprocessedName", "reprocesed" + name)

	if maxRepeat <= 1:
		_fillDataFromDataset(ds, data, name)
		data[name] = _normalizeDict(data[name], mode)
		if reprocessedIds:
			data[reprocessedName] = _classifyReprocessed(ds, reprocessedIds, reprocessedMode)
		return

	rowCount = ds.getRowCount()
	colCount = ds.getColumnCount()
	headers = [ds.getColumnName(i) for i in range(colCount)]

	for i in range(1, maxRepeat + 1):
		data['{0}{1}'.format(name, i)] = {}
		if reprocessedIds:
			data['{0}{1}'.format(reprocessedName, i)] = {}

	for k in range(min(rowCount, maxRepeat)):
		values = [ds.getValueAt(k, i) for i in range(colCount)]
		oneByN = system.dataset.toDataSet(headers, [values])
		slotName = '{0}{1}'.format(name, k + 1)
		_fillDataFromDataset(oneByN, data, slotName)
		data[slotName] = _normalizeDict(data[slotName], mode)
		if reprocessedIds:
			data['{0}{1}'.format(reprocessedName, k + 1)] = _classifyReprocessed(oneByN, reprocessedIds, reprocessedMode)


def _extractComments(papoID, nodeID, registerCode, db, station=None):
	"""Collect unique insights text from every row in this cycle."""
	cycleSql, params = _cycleFilter(papoID, nodeID, registerCode, station)
	sql = '''
		SELECT DataAnswer
		FROM registerhistory
		WHERE {0}
		ORDER BY ID ASC
	'''.format(cycleSql)
	ds = system.db.runPrepQuery(sql, params, db)

	insightsList = []
	for row in range(ds.getRowCount()):
		jsonStr = ds.getValueAt(row, "DataAnswer")
		if jsonStr is None or not isinstance(jsonStr, basestring):
			continue
		jsonStr = jsonStr.strip()
		if not jsonStr:
			continue
		parsed = system.util.jsonDecode(jsonStr)
		if isinstance(parsed, dict) and "items" in parsed:
			for item in parsed["items"]:
				txt = item.get("insights")
				if txt:
					insightsList.append(unicode(txt).strip())

	seen = set()
	uniqueInsights = []
	for txt in insightsList:
		if txt not in seen:
			seen.add(txt)
			uniqueInsights.append(txt)
	return ". ".join(uniqueInsights)


def _extractSignatures(data, papoID, nodeID, registerCode, db, prefixAdmin, prefixOperator, station=None):
	"""Numbered signatures (prefix1, prefix2, ...) plus a last-seen convenience alias."""
	# Query includes Status to distinguish operator (Finalizado) from supervisor (Revisado)
	cycleSql, params = _cycleFilter(papoID, nodeID, registerCode, station)
	sql = '''
		SELECT DataAnswer, Status
		FROM registerhistory
		WHERE {0} AND RegisterTypeID = 10
		ORDER BY ID ASC
	'''.format(cycleSql)
	ds = system.db.runPrepQuery(sql, params, db)

	adminIdx = 0
	operatorIdx = 0
	for k in range(ds.getRowCount()):
		raw = ds.getValueAt(k, "DataAnswer")
		if not raw:
			continue
		try:
			obj = system.util.jsonDecode(raw)
		except:
			continue

		status = ds.getValueAt(k, "Status")
		fullName = (obj.get("name", "") + " " + obj.get("lastname", "")).strip()

		if status == "Finalizado":
			operatorIdx += 1
			data["{0}{1}".format(prefixOperator, operatorIdx)] = fullName
			data[prefixOperator] = fullName
		elif status == "Revisado":
			adminIdx += 1
			data["{0}{1}".format(prefixAdmin, adminIdx)] = fullName
			data[prefixAdmin] = fullName


def _extractSignaturesByRole(data, papoID, nodeID, registerCode, db, prefixAdmin, prefixOperator, station=None):
	"""Signatures by the signer's roles, as the report scripts do: Supervisor_PAPO -> prefixAdmin1, 2... and
	Operator -> prefixOperator (a user with both roles fills both)."""
	cycleSql, params = _cycleFilter(papoID, nodeID, registerCode, station)
	sql = '''
		SELECT DataAnswer
		FROM registerhistory
		WHERE {0} AND RegisterTypeID = 10
		ORDER BY ID ASC
	'''.format(cycleSql)
	ds = system.db.runPrepQuery(sql, params, db)

	adminIdx = 0
	for k in range(ds.getRowCount()):
		raw = ds.getValueAt(k, "DataAnswer")
		if not raw:
			continue
		try:
			obj = system.util.jsonDecode(raw)
		except:
			continue

		roles = obj.get("role")
		if roles is None:
			continue
		if "Supervisor_PAPO" in roles:
			adminIdx += 1
			data["{0}{1}".format(prefixAdmin, adminIdx)] = (obj.get("name", "") + " " + obj.get("lastname", "")).strip()
		if "Operator" in roles:
			data[prefixOperator] = obj.get("name", "") + " " + obj.get("lastname", "")


def _extractSignaturesLast(data, papoID, nodeID, registerCode, db, prefixAdmin, prefixOperator, roles, station=None):
	"""One signature per kind, the last one seen: any of roles -> prefixAdmin, Operator -> prefixOperator."""
	cycleSql, params = _cycleFilter(papoID, nodeID, registerCode, station)
	sql = '''
		SELECT DataAnswer
		FROM registerhistory
		WHERE {0} AND RegisterTypeID = 10
		ORDER BY ID ASC
	'''.format(cycleSql)
	ds = system.db.runPrepQuery(sql, params, db)

	for k in range(ds.getRowCount()):
		raw = ds.getValueAt(k, "DataAnswer")
		if not raw:
			continue
		try:
			obj = system.util.jsonDecode(raw)
		except:
			continue

		signerRoles = obj.get("role")
		if signerRoles is None:
			continue
		fullName = (obj.get("name", "") + " " + obj.get("lastname", "")).strip()
		if [r for r in roles if r in signerRoles]:
			data[prefixAdmin] = fullName
		if "Operator" in signerRoles:
			data[prefixOperator] = fullName


def _registerTypeNames(db):
	"""RegisterTypeID -> registertype.Description."""
	names = {}
	ds = system.db.runPrepQuery("SELECT ID, Description FROM registertype", [], db)
	for i in range(ds.getRowCount()):
		names[ds.getValueAt(i, 0)] = ds.getValueAt(i, 1)
	return names


def _detectShiftFromTimestamp(dt):
	"""Determine shift number from a java.util.Date timestamp."""
	if dt is None:
		return "0"
	shift = papo_core.ui.getShift(dt)
	return str(shift) if shift is not None else "0"


def _queryForAuto(typeIDs, papoID, nodeID, registerCode, db, station=None):
	"""Query registerhistory including Timestamp for shift detection."""
	placeholders = ",".join(["?"] * len(typeIDs))
	cycleSql, params = _cycleFilter(papoID, nodeID, registerCode, station)
	sql = '''
		SELECT DataAnswer, Timestamp
		FROM registerhistory
		WHERE {0} AND RegisterTypeID IN ({1})
		ORDER BY ID ASC
	'''.format(cycleSql, placeholders)
	return system.db.runPrepQuery(sql, params + list(typeIDs), db)


def _processAutoSections(ds, data, typeName, normalizeMode):
	"""Process rows for one RegisterTypeID into numbered sections."""
	rowCount = ds.getRowCount()
	colCount = ds.getColumnCount()
	headers = [ds.getColumnName(i) for i in range(colCount)]

	for k in range(rowCount):
		values = [ds.getValueAt(k, i) for i in range(colCount)]
		oneRow = system.dataset.toDataSet(headers, [values])
		slotName = '{0}{1}'.format(typeName, k + 1)
		_fillDataFromDataset(oneRow, data, slotName)
		data[slotName] = _normalizeDict(data[slotName], normalizeMode)


def _processAutoSectionsMultiShift(ds, data, typeName, normalizeMode):
	"""Process rows with turno grouping for multi-shift forms."""
	rowCount = ds.getRowCount()
	colCount = ds.getColumnCount()
	headers = [ds.getColumnName(i) for i in range(colCount)]

	# Group rows by shift using Timestamp column
	turnoGroups = {}
	for k in range(rowCount):
		dt = ds.getValueAt(k, 'Timestamp')
		shift = _detectShiftFromTimestamp(dt)
		if shift not in turnoGroups:
			turnoGroups[shift] = []
		turnoGroups[shift].append(k)

	# Process each turno group
	for turno in sorted(turnoGroups.keys()):
		indices = turnoGroups[turno]
		for idx, k in enumerate(indices):
			values = [ds.getValueAt(k, i) for i in range(colCount)]
			oneRow = system.dataset.toDataSet(headers, [values])
			slotName = 'turno{0}_{1}{2}'.format(turno, typeName, idx + 1)
			_fillDataFromDataset(oneRow, data, slotName)
			data[slotName] = _normalizeDict(data[slotName], normalizeMode)


EMPTY_SLOT = {u'user': [], u'date': [], u'shift': [], u'insights': u''}


def _oneRow(ds, k):
	"""Row k of a dataset as a one-row dataset."""
	headers = [ds.getColumnName(i) for i in range(ds.getColumnCount())]
	return system.dataset.toDataSet(headers, [[ds.getValueAt(k, i) for i in range(ds.getColumnCount())]])


def _recordDate(raw):
	"""Date of a record from its DataAnswer JSON (the timestamp of the insights item), or None."""
	holder = {}
	_fillDataFromDataset(system.dataset.toDataSet(["DataAnswer"], [[raw]]), holder, "x", False)
	dates = (holder.get("x") or {}).get("date") or [None]
	return dates[0]


def _calendar(date):
	"""java.util.Calendar on a date in plant local time, weeks from Monday (ISO)."""
	from java.util import Calendar, TimeZone
	cal = Calendar.getInstance(TimeZone.getTimeZone("America/Bogota"))
	cal.setFirstDayOfWeek(Calendar.MONDAY)
	cal.setMinimalDaysInFirstWeek(4)
	cal.setTime(date)
	return cal


def _isoWeek(date):
	"""(year, ISO week) of a date in plant local time."""
	from java.util import Calendar
	cal = _calendar(date)
	return (cal.get(Calendar.YEAR), cal.get(Calendar.WEEK_OF_YEAR))


def _weekday(date):
	"""1 = Monday ... 7 = Sunday, in plant local time."""
	from java.util import Calendar
	return ((_calendar(date).get(Calendar.DAY_OF_WEEK) + 5) % 7) + 1


def _weekSlot(date):
	"""Slot 1..21 of the weekly grid (Monday T1, T2, T3 ... Sunday T3); T1 from 22:00 belongs to the next day."""
	from java.util import Calendar
	cal = _calendar(date)
	hour = cal.get(Calendar.HOUR_OF_DAY)
	if hour >= 22 or hour < 6:
		turnoIndex = 0
		if hour >= 22:
			cal.add(Calendar.DATE, 1)
	elif hour < 14:
		turnoIndex = 1
	else:
		turnoIndex = 2
	dayIndex = (cal.get(Calendar.DAY_OF_WEEK) + 5) % 7
	return dayIndex * 3 + turnoIndex + 1


def _nestedMarks(ds, mark, quality=False):
	"""{"cumple": {papoItemID: mark or ''}, "nocumple": {...}} for every item of the rows (PT11-0104), plus bueno /
	malo / regular when quality."""
	names = ("cumple", "nocumple", "bueno", "malo", "regular") if quality else ("cumple", "nocumple")
	answers = {"cumple": "cumple", "nocumple": "no cumple", "bueno": "bueno", "malo": "malo", "regular": "regular"}
	out = dict((n, {}) for n in names)
	for i in range(0 if ds is None else ds.getRowCount()):
		raw = ds.getValueAt(i, "DataAnswer")
		try:
			obj = system.util.jsonDecode(raw) if raw else None
		except:
			obj = None
		if not (isinstance(obj, dict) and "items" in obj):
			continue
		for item in obj["items"]:
			if item.get("papoItemID") is None:
				continue
			value = unicode(item.get("answer") or u"").strip().lower()
			for n in names:
				out[n]["papoItemID{0}".format(item["papoItemID"])] = mark if value == answers[n] else u''
	return out


def _itemsOfType(ds, itemType):
	"""Rows whose JSON keeps only the items of registerTypeID itemType (plus the insights item); rows without any
	are left out (MZ11-0101 saves its first 4-hour check inside the Inicio record)."""
	rows = []
	for i in range(ds.getRowCount()):
		raw = ds.getValueAt(i, "DataAnswer")
		try:
			obj = system.util.jsonDecode(raw) if raw else None
		except:
			obj = None
		if not (isinstance(obj, dict) and "items" in obj):
			continue
		kept = [it for it in obj["items"] if "papoItemID" in it and it.get("registerTypeID") == itemType]
		if not kept:
			continue
		kept += [it for it in obj["items"] if "insights" in it]
		rows.append([system.util.jsonEncode({"items": kept})])
	return system.dataset.toDataSet(["DataAnswer"], rows)


def _reprocessedGroups(section, mode):
	"""Reprocessed groups of a section: the list "reprocessed" plus the one-group shorthand reprocessedIds."""
	groups = list(section.get("reprocessed") or [])
	if section.get("reprocessedIds"):
		groups.insert(0, {"ids": section["reprocessedIds"], "name": section.get("reprocessedName", "reprocesed" + section["name"]),
			"mode": section.get("reprocessedMode", "check"), "normalize": section.get("reprocessedNormalize", mode)})
	return [dict(g, mode=g.get("mode", "check"), normalize=g.get("normalize", mode)) for g in groups]


def _buildSection(ds, data, section, typeNames=None):
	"""One build() section: a key per record (name1, name2...) or one merged key, plus its reprocessed marks."""
	name = section["name"]
	slot = section.get("slot", "record")
	mode = section.get("normalize", "check")
	groups = _reprocessedGroups(section, mode)
	if section.get("itemType") is not None:
		ds = _itemsOfType(ds, section["itemType"])
		if section.get("first") and ds.getRowCount() > 1:
			ds = _oneRow(ds, 0)

	if slot == "single":
		_fillDataFromDataset(ds, data, name)
		raw = data[name]
		data[name] = _normalizeDict(raw, mode)
		for copy in section.get("copies") or []:
			data[copy["name"]] = _normalizeDict(raw, copy.get("normalize", mode))
		for g in groups:
			data[g["name"]] = _normalizeDict(_classifyReprocessed(ds, g["ids"], g["mode"], g.get("keys")), g["normalize"])
		return

	if slot in ("shift", "shiftNumber", "weekday", "weekSlot"):
		_buildTimeSlots(ds, data, section, slot, mode, groups)
		return

	rowCount = ds.getRowCount()
	colCount = ds.getColumnCount()
	headers = [ds.getColumnName(i) for i in range(colCount)]

	# Only the slots of the saved records exist, as in the report scripts it replaces
	for k in range(rowCount):
		values = [ds.getValueAt(k, i) for i in range(colCount)]
		oneByN = system.dataset.toDataSet(headers, [values])
		slotName = '{0}{1}'.format(name, k + section.get("start", 1))
		_fillDataFromDataset(oneByN, data, slotName)
		data[slotName] = _normalizeDict(data[slotName], mode)
		if section.get("nestedMarks"):
			data[slotName].update(_nestedMarks(oneByN, section["nestedMarks"], section.get("nestedQuality", False)))
		for g in groups:
			marks = _classifyReprocessed(oneByN, g["ids"], g["mode"], g.get("keys"))
			data['{0}{1}'.format(g["name"], k + section.get("start", 1))] = _normalizeDict(marks, g["normalize"])
		if section.get("typeName") and typeNames is not None:
			typeID = ds.getValueAt(k, "RegisterTypeID")
			data[slotName + "_type"] = typeNames.get(typeID, u"Desconocido")
			data[slotName + "_typeID"] = typeID
		for copy in section.get("copies") or []:
			raw = {}
			_fillDataFromDataset(oneByN, raw, "x")
			data["{0}{1}".format(copy["name"], k + section.get("start", 1))] = _normalizeDict(raw["x"], copy.get("normalize", mode))


def _buildTimeSlots(ds, data, section, slot, mode, groups):
	"""Slots by time: "shift" (one column per plant shift in order of appearance, records of the same shift merged
	unless merge is False, the first columns empty), "weekday" (name1 Monday .. name7 Sunday, first record of each day
	in the week of the first dated record) and "weekSlot" (name1 .. name21, Monday T1 .. Sunday T3, from the record
	Timestamp)."""
	name = section["name"]
	slots = []
	if slot == "shift":
		for i in range(1, section.get("columns", 3) + 1):
			data["{0}{1}".format(name, i)] = ""
			for g in groups:
				data["{0}{1}".format(g["name"], i)] = ""
		columns, count = {}, 0
		for k in range(ds.getRowCount()):
			row = _oneRow(ds, k)
			holder = {}
			_fillDataFromDataset(row, holder, "x")
			shift = ((holder.get("x") or {}).get("shift") or [None])[0]
			if shift in columns:
				number = columns[shift]
			else:
				count += 1
				number = count
				if shift:
					columns[shift] = number
			slots.append((number, row))
	elif slot == "shiftNumber":
		# name1..name3 = the record of plant shift 1..3, empty when there is none (TR11-0102)
		for i in (1, 2, 3):
			data["{0}{1}".format(name, i)] = dict(EMPTY_SLOT)
			for g in groups:
				data["{0}{1}".format(g["name"], i)] = {}
		for k in range(ds.getRowCount()):
			row = _oneRow(ds, k)
			holder = {}
			_fillDataFromDataset(row, holder, "x")
			shift = ((holder.get("x") or {}).get("shift") or [None])[0]
			slots.append((int(shift) if shift else k + 1, row))
	elif slot == "weekday":
		target, byDay = None, {}
		for k in range(ds.getRowCount()):
			date = _recordDate(ds.getValueAt(k, "DataAnswer"))
			if date is None:
				continue
			if target is None:
				target = _isoWeek(date)
			if _isoWeek(date) == target and _weekday(date) not in byDay:
				byDay[_weekday(date)] = _oneRow(ds, k)
		for day in range(1, 8):
			if day in byDay:
				slots.append((day, byDay[day]))
			else:
				data["{0}{1}".format(name, day)] = dict(EMPTY_SLOT)
	else:
		for k in range(ds.getRowCount()):
			stamp = ds.getValueAt(k, "Timestamp")
			slots.append((_weekSlot(stamp) if stamp is not None else k + 1, _oneRow(ds, k)))

	merge = slot == "shift" and section.get("merge", True)
	for number, row in slots:
		slotName = "{0}{1}".format(name, number)
		holder = {}
		_fillDataFromDataset(row, holder, "x")
		values = _normalizeDict(holder["x"], mode)
		if merge and isinstance(data.get(slotName), dict):
			data[slotName].update(values)
		else:
			data[slotName] = values
		for g in groups:
			marks = _normalizeDict(_classifyReprocessed(row, g["ids"], g["mode"], g.get("keys")), g["normalize"])
			markName = "{0}{1}".format(g["name"], number)
			if merge and isinstance(data.get(markName), dict):
				data[markName].update(marks)
			else:
				data[markName] = marks


def _header(data, typeID, papoID, nodeID, registerCode, db, station=None):
	"""data["date"] and data["shift"] from the Timestamp of the cycle's first record of typeID."""
	cycleSql, params = _cycleFilter(papoID, nodeID, registerCode, station)
	ds = system.db.runPrepQuery("SELECT Timestamp FROM registerhistory WHERE {0} AND RegisterTypeID = ? ORDER BY ID ASC".format(cycleSql),
		params + [typeID], db)
	if ds.getRowCount() > 0:
		date = ds.getValueAt(0, 0)
		shift = papo_core.ui.getShift(date)
		data["date"] = date
		data["shift"] = str(shift) if shift is not None else None
	else:
		data["date"] = None
		data["shift"] = None


def _historyList(papoID, nodeID, registerCode, db, station=None):
	"""Records of the cycle for the history table (same columns as the report query RegisterHistory)."""
	cycleSql, params = _cycleFilter(papoID, nodeID, registerCode, station, "rh.")
	sql = '''
		SELECT
			rh.Timestamp AS Fecha,
			rh.[User] AS "Global ID",
			rh.Status AS "Estado",
			rt.Description AS "Tipo Registro",
			rh.RegisterTypeID
		FROM registerhistory rh
		INNER JOIN registertype rt ON rh.RegisterTypeID = rt.ID
		WHERE {0}
		ORDER BY rh.Timestamp ASC
	'''.format(cycleSql)
	return system.dataset.toDataSet(system.db.runPrepQuery(sql, params, db))


# ==================== PUBLIC FUNCTIONS ====================

def build(data, sections, history="RegisterHistoryStation", signatures="role", signaturePrefix=('firmaAdministrator', 'firmaOperator'),
		signatureRoles=("Supervisor_PAPO",), header=None):
	"""
	Fill the data of a report from its list of sections.

	The one call of a report script: each section names the register types
	it reads and the key the template uses; the engine adds the comment, the
	signatures and the history list. Logic that only one form has stays as a
	few lines after this call in its report.

	Version: 1.0.0

	Args:
		data (dict): Report data dict with papoID, nodeID, registerCode, db and,
			when the viewer passes it, workstationNodeID (only that station's cycle)
		sections (list): Each item is a dict:
			types (list[int]): RegisterTypeID(s) read together, ordered by ID
			name (str): base key in data
			slot (str): "record" (default) = one key per record, name1..nameN;
				"single" = all the records merged in data[name]; "shift" = one column
				per plant shift in order of appearance (records of the same shift merged
				unless merge is False; columns: empty columns first, default 3);
				"shiftNumber" = name1..name3 by the plant shift of the record;
				"weekday" = name1 Monday .. name7 Sunday; "weekSlot" = name1 .. name21
				(Monday T1 .. Sunday T3, from the record Timestamp)
			normalize (str): "check" (default, Cumple/No Cumple -> check/x
				symbols), "yn" (-> Si/No), "ok" (-> OK/N OK), "raw" (no mapping)
			reprocessedIds (list[int], optional): papoItemIDs also marked in
				cumplepapoItemID{ID} / nocumplepapoItemID{ID} (or bueno/malo/regular)
			reprocessedMode (str, optional): "check" (default) or "quality"
			reprocessedName (str, optional): base key of the marks, numbered like
				the section (defaults to "reprocesed" + name)
			reprocessedNormalize (str, optional): mapping of the marks (defaults to
				the section normalize; e.g. "ok" -> OK / N OK)
			reprocessed (list, optional): more groups of marks, each a dict with ids,
				name, mode ("check", "quality", "yn" -> siItemID/noItemID, "ok" -> the
				item key with OK / NO OK, "number" -> number{value}papoItemID, "x" -> both keys
				with X or blank, "values" -> keys {answer text: key prefix or [prefix, text]})
				and normalize ("okText" -> Ok / No Ok besides the section modes)
			typeName (bool, optional): also name{N}_type = registertype.Description of the record
				and name{N}_typeID = its RegisterTypeID
			start (int, optional): number of the first record slot (default 1)
			itemType (int, optional): keep only the items of that registerTypeID inside each
				record, and first (bool) keeps only the first record that has them
			nestedMarks (str, optional): each slot also gets cumple / nocumple dicts with this
				mark or blank for every item (nestedQuality adds bueno / malo / regular)
			copies (list, optional): the same slots again under another name with another
				normalize, each a dict with name and normalize (e.g. "ar" -> A / R, "mark" ->
				check-x on Cumple, blank on No Cumple)
		history (str): key of the history list the template table reads, or None
		signatures (str): "role" (default, as the report scripts: Supervisor_PAPO ->
			adminKey1, 2..., Operator -> operatorKey), "roleLast" (one adminKey and one
			operatorKey, the last of each) or "status" (Revisado -> adminKey1...,
			Finalizado -> operatorKey1..., plus a last-seen alias without the number)
		signaturePrefix (tuple): (adminKey, operatorKey) base names for signatures
		signatureRoles (tuple): roles of a supervisor signature for "roleLast"
		header (int, optional): RegisterTypeID whose first record gives data["date"] (its
			Timestamp) and data["shift"] (its plant shift)

	Returns:
		None: Populates data in place

	Changelog:
		2026-10-27 | William M. | v1.0.0 - Initial version (pilot AC10-0202, AC10-0301,
			AC10-1101, CA02-2102); reprocessedNormalize for FO10-0601 / FO10-1701;
			reprocessed groups and modes yn / ok / number, typeName and signatures
			"roleLast" for the rest of the reports
	"""
	papoID = data.get('papoID')
	nodeID = data.get('nodeID')
	registerCode = data.get('registerCode')
	db = data.get('db', 'papo_db') or 'papo_db'
	station = data.get('workstationNodeID')

	try:
		refResult = system.db.runPrepQuery("SELECT Reference FROM papo WHERE ID = ?", [papoID], db)
		ref = refResult.getValueAt(0, 0) if refResult.getRowCount() > 0 else "papo_core.report"
	except:
		ref = "papo_core.report"
	logger = system.util.getLogger(ref)

	try:
		typeNames = _registerTypeNames(db) if [s for s in sections if s.get("typeName")] else None
		for section in sections:
			ds = _queryByTypes(section["types"], papoID, nodeID, registerCode, db, station)
			_buildSection(ds, data, section, typeNames)

		data["comment"] = _extractComments(papoID, nodeID, registerCode, db, station)
		if signatures == "status":
			_extractSignatures(data, papoID, nodeID, registerCode, db, signaturePrefix[0], signaturePrefix[1], station)
		elif signatures == "roleLast":
			_extractSignaturesLast(data, papoID, nodeID, registerCode, db, signaturePrefix[0], signaturePrefix[1], signatureRoles, station)
		else:
			_extractSignaturesByRole(data, papoID, nodeID, registerCode, db, signaturePrefix[0], signaturePrefix[1], station)
		if history:
			data[history] = _historyList(papoID, nodeID, registerCode, db, station)
		if header is not None:
			_header(data, header, papoID, nodeID, registerCode, db, station)

	except Exception as e:
		logger.error("Error building report data: " + str(e))


def monthGrid(data, typeIDs, prefix="turno", refTypeID=8):
	"""
	Monthly grid of marks: data["turno{shift}"]["dia{day}"]["papoItemID{ID}"] = check / x for every record of
	the given types in the month of the cycle (the month of its last record of refTypeID, or this month), read
	by node and, when the viewer passes it, by station. Used after build() by TR11-0102.

	Version: 1.0.0

	Args:
		data (dict): Report data dict with papoID, nodeID, registerCode, db, optional workstationNodeID
		typeIDs (list[int]): RegisterTypeID(s) of the grid records
		prefix (str): base key per shift (default "turno")
		refTypeID (int): register type whose last record gives the month (default 8, Fin)

	Returns:
		None: Populates data["turno1"]..["turno3"] with dia1..dia31 in place

	Changelog:
		2026-10-27 | William M. | v1.0.0 - Initial version (from the TR11-0102 report script)
	"""
	papoID = data.get('papoID')
	nodeID = data.get('nodeID')
	registerCode = data.get('registerCode')
	db = data.get('db', 'papo_db') or 'papo_db'
	station = data.get('workstationNodeID')
	logger = system.util.getLogger("papo_core.report.monthGrid")
	try:
		cycleSql, params = _cycleFilter(papoID, nodeID, registerCode, station)
		ref = system.db.runPrepQuery("SELECT TOP 1 Timestamp FROM registerhistory WHERE {0} AND RegisterTypeID = ? ORDER BY Timestamp DESC".format(cycleSql),
			params + [refTypeID], db)
		refDate = ref.getValueAt(0, "Timestamp") if ref.getRowCount() > 0 else system.date.now()
		monthStart = system.date.getDate(system.date.getYear(refDate), system.date.getMonth(refDate), 1)
		monthEnd = system.date.addMonths(monthStart, 1)
		placeholders = ",".join(["?"] * len(typeIDs))
		sql = '''
			SELECT DataAnswer, Timestamp
			FROM registerhistory
			WHERE PapoID = ? AND NodeID = ? AND (? IS NULL OR WorkstationNodeID = ?) AND Timestamp >= ? AND Timestamp < ?
				AND RegisterTypeID IN ({0})
			ORDER BY ID ASC
		'''.format(placeholders)
		ds = system.db.runPrepQuery(sql, [papoID, nodeID, station, station, monthStart, monthEnd] + list(typeIDs), db)

		for shift in (1, 2, 3):
			data["{0}{1}".format(prefix, shift)] = dict(("dia{0}".format(day), {}) for day in range(1, 32))
		for i in range(ds.getRowCount()):
			raw = ds.getValueAt(i, "DataAnswer")
			stamp = ds.getValueAt(i, "Timestamp")
			if not raw or stamp is None:
				continue
			try:
				obj = system.util.jsonDecode(raw)
			except:
				continue
			if not (isinstance(obj, dict) and "items" in obj):
				continue
			shift = papo_core.ui.getShift(stamp)
			day = "dia{0}".format(system.date.getDayOfMonth(stamp))
			for item in obj["items"]:
				if "papoItemID" not in item:
					continue
				answer = item.get("answer")
				if answer in ("Cumple", "Si"):
					mark = NORMALIZE_MODES["check"]["cumple"]
				elif answer in ("No Cumple", "No"):
					mark = NORMALIZE_MODES["check"]["no cumple"]
				else:
					continue
				data["{0}{1}".format(prefix, shift)][day]["papoItemID{0}".format(item["papoItemID"])] = mark
	except Exception as e:
		logger.error("Error building the month grid: " + str(e))


def extractReportData(data, sections, signaturePrefix=('firmaAdministrator', 'firmaOperator')):
	"""
	Extract and flatten registerhistory data into the report data dict.

	Args:
		data (dict): Report data dict with papoID, nodeID, registerCode, db and
			optional workstationNodeID (only that station's cycle)
		sections (list): Each item is a dict:
			types (list[int]): RegisterTypeID(s) grouped in one IN(...) query
			name (str): base key written into data (e.g. "inicio", "item")
			max (int): 1 (default) = data[name] is one merged dict;
				>1 = data[name1]..data[nameMax], unused slots left empty
			normalize (str): "check" (default, Cumple/No Cumple -> check/x
				symbols), "yn" (-> Si/No), "ok" (-> OK/N OK), "raw" (no mapping)
			reprocessedIds (list[int], optional): papoItemIDs to also
				classify separately (cumplepapoItemIDxxx/nocumplepapoItemIDxxx)
			reprocessedMode (str, optional): "check" (default) or "quality"
				(Bueno/Malo/Regular)
			reprocessedName (str, optional): base key for the reprocessed
				dict (defaults to "reprocesed" + name)
		signaturePrefix (tuple): (adminKey, operatorKey) base names for
			signatures, numbered signaturePrefix[0]{N}/[1]{N} plus a
			last-seen convenience alias without the number

	Returns:
		None: Populates data dict in place

	Changelog:
		2026-08-05 | William M. | v2.0.0 - Config-driven rewrite
	"""
	papoID = data.get('papoID')
	nodeID = data.get('nodeID')
	registerCode = data.get('registerCode')
	db = data.get('db', 'papo_db') or 'papo_db'
	station = data.get('workstationNodeID')

	try:
		refResult = system.db.runPrepQuery("SELECT Reference FROM papo WHERE ID = ?", [papoID], db)
		ref = refResult.getValueAt(0, 0) if refResult.getRowCount() > 0 else "papo_core.report"
	except:
		ref = "papo_core.report"
	logger = system.util.getLogger(ref)

	try:
		for section in sections:
			ds = _queryByTypes(section["types"], papoID, nodeID, registerCode, db, station)
			_processSection(ds, data, section)

		data["comment"] = _extractComments(papoID, nodeID, registerCode, db, station)
		_extractSignatures(data, papoID, nodeID, registerCode, db, signaturePrefix[0], signaturePrefix[1], station)

	except Exception as e:
		logger.error("Error extracting report data: " + str(e))


def extractReportDataAuto(data):
	"""
	Auto-configured report data extraction.

	Discovers RegisterTypeIDs from papoitem_registertype, derives
	section names from registertype.Description (spaces/commas stripped),
	and processes each type as numbered sections.

	Version: 2.1.0

	Args:
		data (dict): Report data dict with:
			papoID (int): Papo ID
			nodeID (int): Node ID
			registerCode (int): Register code for this form session
			db (str): Database connection name
			workstationNodeID (int, optional): Only that station's cycle
			multiShift (bool): Enable turno grouping (default False)
			normalizeMode (str): "check" (default), "yn", "ok", "raw"

	Returns:
		None: Populates data dict in place

	Changelog:
		2026-08-11 | William M. | v2.1.0 - Auto-configured engine
	"""
	papoID = data.get('papoID')
	nodeID = data.get('nodeID')
	registerCode = data.get('registerCode')
	db = data.get('db', 'papo_db') or 'papo_db'
	multiShift = data.get('multiShift', False)
	normalizeMode = data.get('normalizeMode', 'check')
	sigPrefix = data.get('signaturePrefix', ('firmaAdministrator', 'firmaOperator'))
	station = data.get('workstationNodeID')

	# Resolve MasterPapoID
	try:
		masterResult = system.db.runPrepQuery(
			"SELECT COALESCE(MasterPapoID, ID) FROM papo WHERE ID = ?",
			[papoID], db)
		masterID = masterResult.getValueAt(0, 0) if masterResult.getRowCount() > 0 else papoID
	except:
		masterID = papoID

	# Get logger from papo Reference
	try:
		refResult = system.db.runPrepQuery(
			"SELECT Reference FROM papo WHERE ID = ?", [papoID], db)
		ref = refResult.getValueAt(0, 0) if refResult.getRowCount() > 0 else "papo_core.report"
	except:
		ref = "papo_core.report"
	logger = system.util.getLogger(ref)

	try:
		# Discover RegisterTypeIDs for this papo from DB
		typesDs = system.db.runPrepQuery("""
			SELECT DISTINCT pir.RegisterTypeID, rt.Description
			FROM papoitem pi
			JOIN papoitem_registertype pir ON pir.PapoItemID = pi.ID
			JOIN registertype rt ON rt.ID = pir.RegisterTypeID
			WHERE pi.PapoID = ?
			ORDER BY pir.RegisterTypeID
		""", [masterID], db)

		# Process each discovered type
		for i in range(typesDs.getRowCount()):
			typeID = typesDs.getValueAt(i, "RegisterTypeID")
			rawName = typesDs.getValueAt(i, "Description")
			typeName = rawName.replace(" ", "").replace(",", "")

			ds = _queryForAuto([typeID], papoID, nodeID, registerCode, db, station)
			if ds.getRowCount() == 0:
				continue

			if not multiShift:
				_processAutoSections(ds, data, typeName, normalizeMode)
			else:
				_processAutoSectionsMultiShift(ds, data, typeName, normalizeMode)

		# Extract comments
		data["comment"] = _extractComments(papoID, nodeID, registerCode, db, station)

		# Extract signatures
		_extractSignatures(
			data, papoID, nodeID, registerCode, db, sigPrefix[0], sigPrefix[1], station)

	except Exception as e:
		logger.error("Error in extractReportDataAuto: " + str(e))


def extractShiftChecklist(data, typeIDs, prefix="t", marks=None):
	"""
	Build per-shift OK / X / N/A columns for checklists filled once per shift.

	Groups the cycle's records of the given RegisterTypeIDs by the shift of
	their Timestamp and keeps the latest record of each shift. Each answer
	goes into the column key of its value, so the template places one mark
	per column (e.g. @t2.ok11260@, @t2.x11260@, @t2.na11260@).

	Version: 1.0.0

	Args:
		data (dict): Report data dict with papoID, nodeID, registerCode, db and
			optional workstationNodeID (only that station's cycle)
		typeIDs (list[int]): RegisterTypeID(s) of the checklist records
		prefix (str): Base key per shift, data["{prefix}{shift}"] (default "t")
		marks (dict, optional): Lowercase answer -> (column, mark). Default:
			cumple -> ("ok", check), no cumple -> ("x", cross), n/a -> ("na", check)

	Returns:
		None: Populates data["{prefix}1"], data["{prefix}2"] and data["{prefix}3"]
			in place, each with ok{ID} / x{ID} / na{ID} marks plus "user" (who
			filled that shift) and "date" (row Timestamp)

	Changelog:
		2026-10-22 | William M. | v1.0.0 - Initial version (FU10-0202)
	"""
	papoID = data.get('papoID')
	nodeID = data.get('nodeID')
	registerCode = data.get('registerCode')
	db = data.get('db', 'papo_db') or 'papo_db'

	if marks is None:
		marks = {
			"cumple": ("ok", NORMALIZE_MODES["check"]["cumple"]),
			"no cumple": ("x", NORMALIZE_MODES["check"]["no cumple"]),
			"n/a": ("na", NORMALIZE_MODES["check"]["cumple"]),
		}

	logger = system.util.getLogger("papo_core.report.extractShiftChecklist")

	try:
		# Empty columns so every shift key exists in the template
		for shift in (1, 2, 3):
			data["{0}{1}".format(prefix, shift)] = {"user": "", "date": None}

		ds = _queryForAuto(typeIDs, papoID, nodeID, registerCode, db, data.get('workstationNodeID'))
		for i in range(ds.getRowCount()):
			raw = ds.getValueAt(i, "DataAnswer")
			if not raw:
				continue
			try:
				obj = system.util.jsonDecode(raw)
			except:
				continue
			if not (isinstance(obj, dict) and "items" in obj):
				continue

			rowDate = ds.getValueAt(i, "Timestamp")
			shift = papo_core.ui.getShift(rowDate)
			if shift is None:
				continue

			column = {"user": "", "date": rowDate}
			for item in obj["items"]:
				if "papoItemID" in item:
					answer = item.get("answer")
					answerKey = unicode(answer).strip().lower() if answer is not None else u""
					if answerKey in marks:
						columnName, mark = marks[answerKey]
						column["{0}{1}".format(columnName, item["papoItemID"])] = mark
				elif "insights" in item and isinstance(item.get("user"), basestring):
					column["user"] = item["user"].strip()

			# Rows come ordered by ID, so the latest record of each shift wins
			data["{0}{1}".format(prefix, shift)] = column

	except Exception as e:
		logger.error("Error building shift checklist: " + str(e))
