



def getRangeColor(value, minValue, maxValue, colorType="border"):
	
	"""
	Return display color based on whether a value falls within a numeric range.
	
	Version: 1.0.0
	
	Args:
		value (float): Value to evaluate. None or empty string returns neutral color
		minValue (float): Lower bound of the acceptance range (inclusive)
		maxValue (float): Upper bound of the acceptance range (inclusive)
		colorType (str): Target property - "border" or "text"
	
	Returns:
		str: Hex color string. Neutral color when in range or empty,
		     error color when out of range or on error
	
	Changelog:
		2026-08-12 | Andres G. | v1.0.0 - Initial version
	"""
	
	
	logger = system.util.getLogger("vam-fc-mes.papo_core.validation.getRangeColor")
	
	COLOR_BORDER_OK = "#C0C0C0"
	COLOR_TEXT_OK = "#000000"
	COLOR_ERROR = "#F70808"
	
	try:
		# Select neutral color according to target property
		if colorType == "text":
			neutralColor = COLOR_TEXT_OK
		else:
			neutralColor = COLOR_BORDER_OK

		# Return neutral for empty or unset values
		if value is None or value == "":
			return neutralColor

		# Return neutral when range is not configured
		if minValue is None or maxValue is None:
			return neutralColor

		# Convert inputs for numeric comparison
		currentValue = float(value)
		minimum = float(minValue)
		maximum = float(maxValue)

		# print "Value: {}, Range: {} - {}".format(currentValue, minimum, maximum)

		# Compare value against range
		if minimum <= currentValue <= maximum:
			return neutralColor

		# logger.info("Value {} out of range {} - {}".format(currentValue, minimum, maximum))

		return COLOR_ERROR

	except Exception as e:
		logger.error("Error evaluating range for value {}: {}".format(value, str(e)))
		if colorType == "text":
			return COLOR_TEXT_OK
		return COLOR_BORDER_OK

def getQuestions(value):
	"""
	Load every question text of a PAPO form in a single query.

	Resolves the template through COALESCE(MasterPapoID, ID) so cloned PAPOs
	read the questions of their master. Meant for a view-level custom
	property (view.custom.questions) so each label reads from it instead of
	querying the database per question.

	Version: 1.0.0

	Changelog:
		2026-10-22 | William M. | v1.0.0 - Initial version (EC07-0101 barcada pilot)

	Args:
		value (dict): Expression structure with:
			papoID (int): Form PapoID (view.params.papoID)
			dbConnection (str): Database connection (view.custom.dbConnection)

	Returns:
		dict: {"<papoItemID>": "Description"}. Empty dict when inputs are
		      missing or on error
	"""
	logger = system.util.getLogger("papo_core.items.getQuestions")

	try:
		papoID = value.get("papoID")
		dbConnection = value.get("dbConnection")
		if papoID is None or not dbConnection:
			return {}

		query = """
			SELECT ID, Description
			FROM papoitem
			WHERE PapoID = (SELECT COALESCE(MasterPapoID, ID) FROM papo WHERE ID = ?)
		"""
		ds = system.db.runPrepQuery(query, [papoID], dbConnection)

		questions = {}
		for row in range(ds.getRowCount()):
			description = ds.getValueAt(row, "Description")
			questions[str(ds.getValueAt(row, "ID"))] = description if description is not None else ""
		return questions

	except Exception as e:
		logger.error("Error loading questions for papoID {}: {}".format(value.get("papoID"), str(e)))
		return {}


def getQuestionText(value):
	"""
	Return the question text of one papoItem from the view question map.

	Falls back to a single-item query only when the item is not in the map
	(for example, a question that belongs to another PAPO).

	Version: 1.0.0

	Changelog:
		2026-10-22 | William M. | v1.0.0 - Initial version (EC07-0101 barcada pilot)

	Args:
		value (dict): Expression structure with:
			papoItemID (int): Item ID of the label (this.custom.papoItemID)
			questions (dict): Question map from getQuestions (view.custom.questions)
			dbConnection (str): Database connection for the fallback query

	Returns:
		str: Question description, or "" when not found or on error
	"""
	logger = system.util.getLogger("papo_core.items.getQuestionText")

	try:
		papoItemID = value.get("papoItemID")
		if papoItemID is None or papoItemID == "":
			return ""

		questions = value.get("questions") or {}
		key = str(int(papoItemID))
		if key in questions:
			return questions[key]

		dbConnection = value.get("dbConnection")
		if not dbConnection:
			return ""

		ds = system.db.runPrepQuery("SELECT Description FROM papoitem WHERE ID = ?", [int(papoItemID)], dbConnection)
		if ds.getRowCount() > 0 and ds.getValueAt(0, "Description") is not None:
			return ds.getValueAt(0, "Description")
		return ""

	except Exception as e:
		logger.error("Error reading question text for papoItemID {}: {}".format(value.get("papoItemID"), str(e)))
		return ""


def _toNumber(value):
	"""Number typed in a text field (comma or dot as decimal separator); None when it is not a number."""
	if value is None:
		return None
	try:
		return float(unicode(value).strip().replace(",", "."))
	except ValueError:
		return None


def _cycleRegisters(component):
	"""Registers of the form's type saved in the open cycle of this station, oldest first: (Timestamp, User, {papoItemID: answer}, insights)."""
	params = component.view.params
	query = """
		SELECT [Timestamp], [User], DataAnswer
		FROM registerhistory
		WHERE WorkstationNodeID = ? AND PapoID = ? AND RegisterTypeID = ?
			AND RegisterCode = (
				SELECT TOP 1 RegisterCode FROM registerhistory
				WHERE WorkstationNodeID = ? AND PapoID = ?
				ORDER BY RegisterCode DESC, ID DESC
			)
		ORDER BY ID ASC
	"""
	args = [params.workstationnodeID, params.papoID, component.view.custom.registerTypeID,
		params.workstationnodeID, params.papoID]
	ds = system.db.runPrepQuery(query, args, component.view.custom.dbConnection)
	registers = []
	for row in range(ds.getRowCount()):
		data = system.util.jsonDecode(ds.getValueAt(row, "DataAnswer") or "{}") or {}
		answers = {}
		insights = u""
		for item in data.get("items", []):
			if "papoItemID" in item and item.get("answer") not in (None, ""):
				answers.setdefault(item["papoItemID"], item["answer"])
			elif isinstance(item.get("insights"), basestring):
				insights = item["insights"].strip()
		registers.append((ds.getValueAt(row, "Timestamp"), ds.getValueAt(row, "User"), answers, insights))
	return registers


def getCycleSum(component, sumItemID, keyItemID, keyValue, current):
	"""
	Sum of one item over the registers of the open cycle of this station, plus the value being entered.

	Reads the registers of the same type already saved in the cycle (same WorkstationNodeID, PapoID and
	last RegisterCode, the one register.save uses) and adds the sumItemID answers that are numbers; with
	keyItemID, only the registers whose keyItemID answer equals keyValue. The form being filled is not
	saved yet, so current is added.

	Version: 1.1.0

	Changelog:
		2026-10-28 | William M. | v1.1.0 - keyItemID None adds every register of the cycle (FO10-0100: total
			batteries entered in the form)
		2026-10-28 | William M. | v1.0.0 - Initial version (FO10-0100: total batteries per table in the shift)

	Args:
		component (Component): Any component of the form (self in a binding transform)
		sumItemID (int): papoItemID to add up (e.g. battery quantity)
		keyItemID (int): papoItemID that groups the registers (e.g. table number); None for all of them
		keyValue (str): Answer of keyItemID in the form being filled
		current (str): Value of sumItemID in the form being filled

	Returns:
		str: The total as text (no decimals when whole); "" when there is nothing to add or on error
	"""
	ref = str(getattr(component.view.custom, "referencePapo", "") or "papo_core.items")
	logger = system.util.getLogger(ref)

	try:
		if keyItemID is not None and keyValue in (None, ""):
			return ""
		total = _toNumber(current)
		for stamp, user, answers, insights in _cycleRegisters(component):
			if keyItemID is not None and unicode(answers.get(keyItemID, "")) != unicode(keyValue):
				continue
			number = _toNumber(answers.get(sumItemID))
			if number is not None:
				total = (total or 0) + number

		if total is None:
			return ""
		return unicode(int(total)) if total == int(total) else unicode(total)

	except Exception as e:
		logger.error("getCycleSum {} by {}: {}".format(sumItemID, keyItemID, str(e)))
		return ""


def getCycleRegisters(component, columns, checks=()):
	"""
	Registers of the same type saved in the open cycle of this station, one row per register, for a table.

	Same registers getCycleSum adds up (same WorkstationNodeID, PapoID, RegisterTypeID and last RegisterCode),
	oldest first. Each row maps the table fields to the saved answers, as the report shows them: whole numbers
	without decimals and the Cumple / No Cumple of the checks fields as check / x marks.

	Version: 1.1.0

	Changelog:
		2026-10-28 | William M. | v1.1.0 - "insights" source (Observaciones) and checks marks: the columns of the
			FO10-0100 report
		2026-10-28 | William M. | v1.0.0 - Initial version (FO10-0100: battery entries of the form)

	Args:
		component (Component): Any component of the form (self in a binding transform)
		columns (dict): {field: papoItemID}; "time" gives the time of the register (HH:mm), "user" its operator
			and "insights" its observations
		checks (list): Fields whose answer Cumple / No Cumple shows as a check / x mark

	Returns:
		list[dict]: One {field: text} per register; [] when there are none or on error
	"""
	ref = str(getattr(component.view.custom, "referencePapo", "") or "papo_core.items")
	logger = system.util.getLogger(ref)

	try:
		marks = {u"cumple": u"\u2714", u"no cumple": u"\u2718"}
		rows = []
		for stamp, user, answers, insights in _cycleRegisters(component):
			row = {}
			for field, source in columns.items():
				if source == "time":
					row[field] = system.date.format(stamp, "HH:mm") if stamp is not None else ""
				elif source == "user":
					row[field] = user or ""
				elif source == "insights":
					row[field] = insights
				else:
					value = answers.get(source)
					if isinstance(value, float) and value == int(value):
						value = int(value)
					row[field] = "" if value is None else unicode(value)
					if field in checks:
						row[field] = marks.get(row[field].strip().lower(), row[field])
			rows.append(row)
		return rows

	except Exception as e:
		logger.error("getCycleRegisters: {}".format(str(e)))
		return []


def formatTagTime(value):
	"""
	Time read from the PLC as text: HH:mm:ss when the tag is a date, the text as it comes otherwise.

	Version: 1.0.0

	Changelog:
		2026-10-28 | William M. | v1.0.0 - Initial version (FO10-0100: Hora final real saved "None" without a value)

	Args:
		value: Tag value (date, text or None)

	Returns:
		str: The time as text; "" without a value
	"""
	if value is None:
		return ""
	if hasattr(value, "getTime"):
		return system.date.format(value, "HH:mm:ss")
	return value if isinstance(value, basestring) else unicode(value)
