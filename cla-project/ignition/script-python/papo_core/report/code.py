"""
papo_core.report

Report data extraction for PAPO PDF reports.
Two modes: config-driven (extractReportData) with explicit sections
list, and auto-configured (extractReportDataAuto) which discovers
RegisterTypeIDs from papoitem_registertype, derives section names
from registertype.Description, and handles multi-shift forms with
turno prefix grouping.

Version: 2.1.1

Changelog:
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


def _queryByTypes(typeIDs, papoID, nodeID, registerCode, db):
	"""Query registerhistory filtered by one or more RegisterTypeID (IN clause)."""
	placeholders = ",".join(["?"] * len(typeIDs))
	sql = '''
		SELECT DataAnswer
		FROM registerhistory
		WHERE PapoID = ? AND NodeID = ? AND RegisterCode = ? AND RegisterTypeID IN ({0})
		ORDER BY ID ASC
	'''.format(placeholders)
	params = [papoID, nodeID, registerCode] + list(typeIDs)
	return system.db.runPrepQuery(sql, params, db)


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


def _extractComments(papoID, nodeID, registerCode, db):
	"""Collect unique insights text from every row in this cycle."""
	sql = '''
		SELECT DataAnswer
		FROM registerhistory
		WHERE PapoID = ? AND NodeID = ? AND RegisterCode = ?
		ORDER BY ID ASC
	'''
	ds = system.db.runPrepQuery(sql, [papoID, nodeID, registerCode], db)

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


def _extractSignatures(data, papoID, nodeID, registerCode, db, prefixAdmin, prefixOperator):
	"""Numbered signatures (prefix1, prefix2, ...) plus a last-seen convenience alias."""
	# Query includes Status to distinguish operator (Finalizado) from supervisor (Revisado)
	sql = '''
		SELECT DataAnswer, Status
		FROM registerhistory
		WHERE PapoID = ? AND NodeID = ? AND RegisterCode = ? AND RegisterTypeID = 10
		ORDER BY ID ASC
	'''
	ds = system.db.runPrepQuery(sql, [papoID, nodeID, registerCode], db)

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


def _queryForAuto(typeIDs, papoID, nodeID, registerCode, db):
	"""Query registerhistory including Timestamp for shift detection."""
	placeholders = ",".join(["?"] * len(typeIDs))
	sql = '''
		SELECT DataAnswer, Timestamp
		FROM registerhistory
		WHERE PapoID = ? AND NodeID = ? AND RegisterCode = ? AND RegisterTypeID IN ({0})
		ORDER BY ID ASC
	'''.format(placeholders)
	params = [papoID, nodeID, registerCode] + list(typeIDs)
	return system.db.runPrepQuery(sql, params, db)


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


# ==================== PUBLIC FUNCTIONS ====================

def extractReportData(data, sections, signaturePrefix=('firmaAdministrator', 'firmaOperator')):
	"""
	Extract and flatten registerhistory data into the report data dict.

	Args:
		data (dict): Report data dict with papoID, nodeID, registerCode, db
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

	try:
		refResult = system.db.runPrepQuery("SELECT Reference FROM papo WHERE ID = ?", [papoID], db)
		ref = refResult.getValueAt(0, 0) if refResult.getRowCount() > 0 else "papo_core.report"
	except:
		ref = "papo_core.report"
	logger = system.util.getLogger(ref)

	try:
		for section in sections:
			ds = _queryByTypes(section["types"], papoID, nodeID, registerCode, db)
			_processSection(ds, data, section)

		data["comment"] = _extractComments(papoID, nodeID, registerCode, db)
		_extractSignatures(data, papoID, nodeID, registerCode, db, signaturePrefix[0], signaturePrefix[1])

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

			ds = _queryForAuto([typeID], papoID, nodeID, registerCode, db)
			if ds.getRowCount() == 0:
				continue

			if not multiShift:
				_processAutoSections(ds, data, typeName, normalizeMode)
			else:
				_processAutoSectionsMultiShift(ds, data, typeName, normalizeMode)

		# Extract comments
		data["comment"] = _extractComments(papoID, nodeID, registerCode, db)

		# Extract signatures
		_extractSignatures(
			data, papoID, nodeID, registerCode, db, sigPrefix[0], sigPrefix[1])

	except Exception as e:
		logger.error("Error in extractReportDataAuto: " + str(e))
