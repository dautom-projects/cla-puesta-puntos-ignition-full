def checkParam(paramValue, paramType, default):
	"""
	Checks to see if a param contains an invalid value, and
		if so logs a warning and returns the default value
		for the param. Returns the value if it is valid.
		
	Args:
		paramValue: Value of the param.
		paramType: Type of the param.
		default: Default of the param.
	
	Returns:
		The value of the param if it is not null or empty,
			otherwise the default value for the param.
	"""	
	if paramType == 'string':
		return checkStringParam(paramValue, default)
	elif paramType == 'boolean':
		return checkBoolParam(paramValue, default)
	elif paramType == 'object':
		return checkObjParam(paramValue, default)
		
def checkStringParam(paramValue, default):
	"""
	Checks to see if paramValue is a string. If it is a
		string then returns the same value, otherwise
		returns the default.
		
	Args:
		paramValue: String param value to check.
		default: Default value for the param.
	
	Returns:
		Value of paramValue if it is a string, or default
			if it is not a string.
	"""	
	if isString(paramValue):
		# Param value is a string. Call strip() in case there are leading or trailing whitespaces.
		return paramValue.strip()
	else:
		# Param is not a string.
		return default
	
def checkBoolParam(paramValue, default):
	"""
	Checks to see if paramValue is a boolean. If it is a
		boolean then returns the same value, otherwise
		returns the default.
		
	Args:
		paramValue: Boolean param value to check.
		default: Default value for the param.
	
	Returns:
		Value of paramValue if it is a boolean, or default
			if it is not a boolean.
	"""	
	if isBoolean(paramValue):
		# Param value is a bool.
		return paramValue
	else:
		# Param is not a bool.	
		return default
		
def checkObjParam(paramValue, expected):
	"""
	Performs a series of checks on the object parameter
		paramValue to make sure that it has the expected
		keys and that the values are of the expected type.
		
	Args:
		paramValue: Object param value to check.
		expected: Object containing the expected keys and
			value types along with the default values for
			this param.
	
	Returns:
		Object containing the keys, values in paramValue that
			passed the type check, and the default keys, values
			for any members that did not pass the type check.
	"""	
	# See if it is an object.
	if not isObject(paramValue):
		# Param is not an object. Create the default from the expected object.
		default = {key: value['default'] for key, value in expected.iteritems()}
		
		# Return the default value for this param.
		return default
		
	# Create the param to return.
	param = {}
	
	for objectMemberName, objectMemberVal in expected.iteritems():
		# Check to see if the object member is in the param.
		if objectMemberName in paramValue:
			# Get the value of this object member in the param.
			paramObjectMemberVal = paramValue[objectMemberName]
			
			# Get the expected type.
			expectedType = objectMemberVal['type']
			
			# See if the value is the expected type.
			if expectedType == 'string':
				isCorrectType = isString(paramObjectMemberVal)
			elif expectedType == 'boolean':
				isCorrectType = isBoolean(paramObjectMemberVal)
			elif expectedType == 'object':
				isCorrectType = isObject(paramObjectMemberVal)
			elif expectedType == 'date':
				isCorrectType = isUnixtimeOrDate(paramObjectMemberVal)
				
				# Convert to unixtime ms if needed.
				paramObjectMemberVal = ensureUnixtime(paramObjectMemberVal) \
				if isCorrectType else paramObjectMemberVal
			
			if isCorrectType:
				# Value can be added to param to return.
				param[objectMemberName] = paramObjectMemberVal
			else:
				# Get the type of the param object member value.
				paramObjectMemberValType = type(paramObjectMemberVal)
			
				# Get the default value for this object member.
				defaultVal = objectMemberVal['default']
				
				# Utilize the default value.
				param[objectMemberName] = defaultVal
		else:
			# Get the default value for this object member.
			defaultVal = objectMemberVal['default']
			
			# Utilize the default value.
			param[objectMemberName] = defaultVal
	
	return param
	
def isObject(value):
	"""
	Checks to see if value is an object.
		
	Args:
		value: Value to check.
	
	Returns:
		Boolean indicating whether value is an object or not.
	"""	
	# Import JythonMap to check to see if value is an object.
	from com.inductiveautomation.ignition.common.script.abc import JythonMap
	
	# Check to see if value is an object and return the result.
	return JythonMap.isInstance(value)
	
def isList(value):
	"""
	Checks to see if value is a list.
		
	Args:
		value: Value to check.
	
	Returns:
		Boolean indicating whether value is a list or not.
	"""	
	# Import ArrayList to check to see if value is a list.
	from java.util import ArrayList
	
	# Check to see if the value is an ArrayList and return the result.
	return isinstance(value, (list, ArrayList))
	
def isBoolean(value):
	"""
	Checks to see if value is a boolean.
		
	Args:
		value: Value to check.
	
	Returns:
		Boolean indicating whether value is a boolean or not.
	"""	
	# Check to see if the value is a boolean and return the result.
	return isinstance(value, bool)
	
def isString(value):
	"""
	Checks to see if value is a string.
		
	Args:
		value: Value to check.
	
	Returns:
		Boolean indicating whether value is a string or not.
	"""	
	# Check to see if the value is a string and return the result.
	return isinstance(value, (str, unicode))
	
def ensureUnixtime(date):
	"""
	Converts the date to millis if it is a java.util.Date.
		
	Args:
		date: Date that may be a java.util.Date.
	
	Returns:
		The date in unixtime (millis).
	"""
	# Import java.util.Date to check the date.
	from java.util import Date
	
	if Date.isInstance(date):
		return system.date.toMillis(date)
	else:
		return date
		
def isUnixtimeOrDate(value):
	"""
	Checks to see if the value is unixtime ms or 
		java.util.Date.
		
	Args:
		value: Value to be checked.
	
	Returns:
		True if the value is unixtime ms or a
			java.util.Date.
	"""
	# See if the value is unixtime ms.
	if isinstance(value, (int, long, float)):
		if value >= 0:
			return True
		else:
			return False
	else:
		# Import java.util.Date to check the date.
		from java.util import Date
		
		if Date.isInstance(value):
			return True
		else:
			return False