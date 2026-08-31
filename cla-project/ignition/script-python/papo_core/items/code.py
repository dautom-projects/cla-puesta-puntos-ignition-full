



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