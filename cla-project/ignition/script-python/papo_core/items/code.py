



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
