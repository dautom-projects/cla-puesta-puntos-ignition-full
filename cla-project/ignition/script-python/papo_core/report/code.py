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

Version: 2.3.0

Changelog:
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

		valStr = str(val).strip()
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

			shiftVal = None
			try:
				if ctxDt is not None:
					hour = system.date.getHour24(ctxDt)
					if hour >= 22 or hour < 6:
						shiftVal = "1"
					elif hour >= 6 and hour < 14:
						shiftVal = "2"
					else:
						shiftVal = "3"
			except:
				shiftVal = None
			agg["shift"].append(shiftVal)

		result = dict(agg)
		if includeInsights:
			result[u'insights'] = sep.join(dict.fromkeys(insightsAll)) if insightsAll else u''
		data[keyName] = result

	except:
		try:
			data[keyName] = {u'user': [], u'date': [], u'shift': [], u'insights': u''}
		except:
			pass


def _classifyReprocessed(ds, allowedIds, mode):
	"""Classify specific papoItemIDs into cumple/no-cumple (or quality) buckets."""
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
			valLower = str(val).strip().lower() if val is not None else ""

			if mode == "quality":
				if valLower in QUALITY_MODES:
					result["{0}papoItemID{1}".format(valLower, papoItemID)] = QUALITY_MODES[valLower]
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
		SELECT DataAnswer
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


def _detectShiftFromTimestamp(dt):
	"""Determine shift number from a java.util.Date timestamp."""
	if dt is None:
		return "0"
	try:
		hour = system.date.getHour24(dt)
		if hour >= 22 or hour < 6:
			return "1"
		elif hour >= 6 and hour < 14:
			return "2"
		else:
			return "3"
	except:
		return "0"


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


def _buildSection(ds, data, section):
	"""One build() section: a key per record (name1, name2...) or one merged key, plus its reprocessed marks."""
	name = section["name"]
	slot = section.get("slot", "record")
	mode = section.get("normalize", "check")
	reprocessedIds = section.get("reprocessedIds")
	reprocessedMode = section.get("reprocessedMode", "check")
	reprocessedName = section.get("reprocessedName", "reprocesed" + name)

	if slot == "single":
		_fillDataFromDataset(ds, data, name)
		data[name] = _normalizeDict(data[name], mode)
		if reprocessedIds:
			data[reprocessedName] = _normalizeDict(_classifyReprocessed(ds, reprocessedIds, reprocessedMode), mode)
		return

	rowCount = ds.getRowCount()
	colCount = ds.getColumnCount()
	headers = [ds.getColumnName(i) for i in range(colCount)]

	# Only the slots of the saved records exist, as in the report scripts it replaces
	for k in range(rowCount):
		values = [ds.getValueAt(k, i) for i in range(colCount)]
		oneByN = system.dataset.toDataSet(headers, [values])
		slotName = '{0}{1}'.format(name, k + 1)
		_fillDataFromDataset(oneByN, data, slotName)
		data[slotName] = _normalizeDict(data[slotName], mode)
		if reprocessedIds:
			marks = _classifyReprocessed(oneByN, reprocessedIds, reprocessedMode)
			data['{0}{1}'.format(reprocessedName, k + 1)] = _normalizeDict(marks, mode)


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

def build(data, sections, history="RegisterHistoryStation", signatures="role", signaturePrefix=('firmaAdministrator', 'firmaOperator')):
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
				"single" = all the records merged in data[name]
			normalize (str): "check" (default, Cumple/No Cumple -> check/x
				symbols), "yn" (-> Si/No), "ok" (-> OK/N OK), "raw" (no mapping)
			reprocessedIds (list[int], optional): papoItemIDs also marked in
				cumplepapoItemID{ID} / nocumplepapoItemID{ID} (or bueno/malo/regular)
			reprocessedMode (str, optional): "check" (default) or "quality"
			reprocessedName (str, optional): base key of the marks, numbered like
				the section (defaults to "reprocesed" + name)
		history (str): key of the history list the template table reads, or None
		signatures (str): "role" (default, as the report scripts: Supervisor_PAPO ->
			adminKey1, 2..., Operator -> operatorKey) or "status" (Revisado -> adminKey1...,
			Finalizado -> operatorKey1..., plus a last-seen alias without the number)
		signaturePrefix (tuple): (adminKey, operatorKey) base names for signatures

	Returns:
		None: Populates data in place

	Changelog:
		2026-10-27 | William M. | v1.0.0 - Initial version (pilot AC10-0202, AC10-0301,
			AC10-1101, CA02-2102)
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
			_buildSection(ds, data, section)

		data["comment"] = _extractComments(papoID, nodeID, registerCode, db, station)
		if signatures == "status":
			_extractSignatures(data, papoID, nodeID, registerCode, db, signaturePrefix[0], signaturePrefix[1], station)
		else:
			_extractSignaturesByRole(data, papoID, nodeID, registerCode, db, signaturePrefix[0], signaturePrefix[1], station)
		if history:
			data[history] = _historyList(papoID, nodeID, registerCode, db, station)

	except Exception as e:
		logger.error("Error building report data: " + str(e))


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
