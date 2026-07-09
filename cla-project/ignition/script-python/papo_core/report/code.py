"""
papo_core.report

Report data extraction for PAPO PDF reports.
Universal script for all forms - queries registerhistory by each
RegisterTypeID, parses DataAnswer JSON, and populates the report
data dict. Register types not used by a form are left empty.

Version: 1.0.0

Changelog:
	2026-07-06 | William | v1.0.0 - Initial Project Library version
"""

# Single record types: (RegisterTypeID, keyName)
SINGLE_TYPES = [
	(7, 'startShift'),
	(8, 'endShift'),
]

# Multiple record types: (RegisterTypeID, prefix)
MULTI_TYPES = [
	(1, 'hour'),
	(2, 'twohour'),
	(3, 'halfhour'),
	(4, 'fourhour'),
	(5, 'referenceChange'),
	(6, 'maintenance'),
	(9, 'midShift'),
	(11, 'daily'),
	(13, 'initialCheck'),
	(14, 'rejection'),
	(15, 'finding'),
	(16, 'batteryIn'),
	(17, 'batteryOut'),
	(18, 'defect'),
	(19, 'stop'),
	(20, 'barcada'),
]

# Roles that count as supervisor signature
SUPERVISOR_ROLES = {"Supervisor_PAPO", "Administrator", "INTEGRADOR"}


# ==================== INTERNAL HELPERS ====================

def _normalizeDict(sourceDict):
	"""Normalize answer values to symbols or clean strings."""
	import java.util.Date

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

		if valLower == "cumple":
			result[k] = u"\u2714"
		elif valLower == "no cumple":
			result[k] = u"\u2718"
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


def _processMultipleRows(ds, data, prefix):
	"""Process a multi-row dataset, one key per row: prefix1, prefix2, etc."""
	rowCount = ds.getRowCount()
	colCount = ds.getColumnCount()
	headers = [ds.getColumnName(i) for i in range(colCount)]

	for k in range(rowCount):
		values = [ds.getValueAt(k, i) for i in range(colCount)]
		oneByN = system.dataset.toDataSet(headers, [values])
		name = '{}{}'.format(prefix, k + 1)
		_fillDataFromDataset(oneByN, data, name)
		data[name] = _normalizeDict(data[name])


def _processSingleRecord(ds, data, keyName):
	"""Process a single-record dataset (all rows as one block)."""
	_fillDataFromDataset(ds, data, keyName)
	data[keyName] = _normalizeDict(data[keyName])


def _queryByType(registerTypeID, papoID, nodeID, registerCode, db):
	"""Query registerhistory filtered by RegisterTypeID."""
	sql = '''
		SELECT DataAnswer 
		FROM registerhistory 
		WHERE PapoID = ? AND NodeID = ? AND RegisterCode = ? AND RegisterTypeID = ? 
		ORDER BY ID ASC
	'''
	return system.db.runPrepQuery(sql, [papoID, nodeID, registerCode, registerTypeID], db)


# ==================== PUBLIC FUNCTIONS ====================

def extractReportData(data):
	"""
	Extract and flatten all registerhistory data into the report data dict.

	Args:
		data (dict): Report data dict with papoID, nodeID, registerCode, db

	Returns:
		None: Populates data dict in place
	"""
	papoID = data.get('papoID', 1)
	nodeID = data.get('nodeID', 5)
	registerCode = data.get('registerCode', 18)
	db = data.get('db', 'papo_db') or 'papo_db'

	# Resolve reference for logger name
	try:
		refResult = system.db.runPrepQuery("SELECT Reference FROM papo WHERE ID = ?", [papoID], db)
		ref = refResult.getValueAt(0, 0) if refResult.getRowCount() > 0 else "papo_core.report"
	except:
		ref = "papo_core.report"
	logger = system.util.getLogger(ref)

	try:
		# Single record types
		for typeID, keyName in SINGLE_TYPES:
			ds = _queryByType(typeID, papoID, nodeID, registerCode, db)
			_processSingleRecord(ds, data, keyName)

		# Multiple record types
		for typeID, prefix in MULTI_TYPES:
			ds = _queryByType(typeID, papoID, nodeID, registerCode, db)
			_processMultipleRows(ds, data, prefix)

		# Comments (insights from all records)
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

		data["comment"] = ". ".join(uniqueInsights)

		# Signatures (RegisterTypeID 10)
		ds = _queryByType(10, papoID, nodeID, registerCode, db)

		for k in range(ds.getRowCount()):
			raw = ds.getValueAt(k, "DataAnswer")
			if not raw:
				continue

			try:
				obj = system.util.jsonDecode(raw)
			except:
				continue

			role = obj.get("role", "")
			if isinstance(role, basestring):
				roleSet = set([role])
			elif isinstance(role, list):
				roleSet = set(role)
			else:
				roleSet = set()

			# Operator takes priority (may also hold admin roles)
			if "Operator" in roleSet:
				data["firmaOperator"] = (obj.get("name", "") + " " + obj.get("lastname", "")).strip()
			elif roleSet & SUPERVISOR_ROLES:
				data["firmaAdministrator"] = (obj.get("name", "") + " " + obj.get("lastname", "")).strip()

	except Exception as e:
		logger.error("Error extracting report data: " + str(e))