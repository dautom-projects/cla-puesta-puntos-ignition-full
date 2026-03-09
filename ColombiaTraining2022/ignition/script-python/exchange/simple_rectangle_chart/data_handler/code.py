def handleData(inputData):
	"""
	Ensures that the data is in a supported format by
		performing a series of checks on the data and
		converting the data if needed.
		
	Args:
		inputData: List or Dataset of time series data.
	
	Returns:
		An object containing the results of the checks and 
			the data, which may have been converted (dataset
			to list and/or java.util.Date to unixtime ms).
	"""	
	# If data is a Dataset, convert it to a list.
	if isDataset(inputData):
		data = convertToList(inputData)
	else:
		data = inputData
		
	# Check the structure of the data.
	structureResults = validateStructure(data)
	
	if structureResults['canRenderChart'] == True:
		# Data passed the structure checks.
		# Check the dates in the data.
		datesResults = validateDates(data)
		
		return datesResults
	else:
		# Data did not pass the structure checks.
		return structureResults
	
def validateStructure(data):
	"""
	Performs a series of checks on the structure of the data.
		
	Args:
		data: List or Dataset of time series data.
	
	Returns:
		An object containing the results of the checks.
	"""	
	# Check to see if the data is null.
	if data == None:
		return {'canRenderChart': False, 'reason': 'Data is null. It must be a list or Dataset.'}
	
	# Make sure data is a list.
	if not exchange.simple_rectangle_chart.helper.isList(data):
		return {'canRenderChart': False, 'reason': 'Data is not a list or Dataset. It is a {dataType}.'.format(dataType = type(data))}
	
	# Make sure data is not empty. If so, set reason to empty.
	if len(data) == 0:
		return {'canRenderChart': False, 'reason': ''}
		
	# Make sure that the keys of every data row are 'value' and 't_stamp'.
	correctRow = set(['value', 't_stamp'])
	incorrectRows = [index for index, row in enumerate(data) if set(row.keys()) != correctRow]
		
	if len(incorrectRows) > 0:
		return {'canRenderChart': False, 'reason': 'The following data rows do not contain the expected [t_stamp, value] format: {incorrectRows}'.format(incorrectRows = incorrectRows)}
	
	# Data structure passed the checks.	
	return {'canRenderChart': True}
	
def validateDates(data):
	"""
	Performs a series of checks on the dates in the data,
		and ensures that all all of the timestamps are unixtime.
		
	Args:
		data: List or Dataset of time series data.
	
	Returns:
		An object containing the results of the checks and 
			the data, which may have been converted (from
			java.util.Date to unixtime ms).
	"""	
	# Make sure that there are no null dates.
	nullDateRows = [index for index, row in enumerate(data) if row['t_stamp'] == None]
		
	if len(nullDateRows) > 0:
		return {'canRenderChart': False, 'reason': 'The timestamp of the following rows are null: {nullDateRows}'.format(nullDateRows = nullDateRows)}
	
	# Make sure that the timestamps of every row are unixtime or java.util.Date.
	unsupportedDateTypeRows = [index for index, row in enumerate(data) if not exchange.simple_rectangle_chart.helper.isUnixtimeOrDate(row['t_stamp'])]
	
	if len(unsupportedDateTypeRows) > 0:
		return {'canRenderChart': False, 'reason': 'The timestamp of the following rows are not unixtime (ms) or java.util.Date: {unsupportedDateTypeRows}'.format(unsupportedDateTypeRows = unsupportedDateTypeRows)}
		
	# If any of the timestamps are java.util.Date, then convert them to unixtime.
	data = [{'value': row['value'], 't_stamp': exchange.simple_rectangle_chart.helper.ensureUnixtime(row['t_stamp'])} for row in data]	
	
	# Make sure that timestamp of every row is greater than or equal to the timestamp of the previous row.
	endGreaterRows = [index for index in range(1,len(data)) if data[index - 1]['t_stamp'] > data[index]['t_stamp']]
				
	if len(endGreaterRows) > 0:
		return {'canRenderChart': False, 'reason': 'The timestamp is less than the end date of the previous entry in the following rows: {endGreaterRows}'.format(endGreaterRows = endGreaterRows)}
	
	# Dates in data passed the checks.
	return {'canRenderChart': True, 'data': data}

def convertToList(dataset):
	"""
	Converts a Dataset to a list.
		
	Args:
		dataset: Dataset to be converted.
	
	Returns:
		A list containing the data in the dataset.
	"""	
	# Create the list to hold the data.
	dataList = []
	
	# Get the names of the columns.
	columnNames = dataset.getColumnNames()
	
	# Get the info from each row of the dataset and add to the list.
	for x in range(dataset.getRowCount()):
		row = {}
		for column in columnNames:
			datasetValue = dataset.getValueAt(x, column)
			row[column] = datasetValue
		dataList.append(row)
	
	return dataList	
	
def isDataset(value):
	"""
	Checks to see if value is a dataset.
		
	Args:
		value: Value to check.
	
	Returns:
		Boolean indicating whether value is a dataset or not.
	"""	
	# Import Dataset to check to see if data is a Dataset.
	from com.inductiveautomation.ignition.common import Dataset
	
	# See if it is a dataset and return the result.
	return Dataset.isInstance(value)