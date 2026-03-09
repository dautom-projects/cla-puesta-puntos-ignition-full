def findMatch(dataSet, matchVal, searchCol, resultCol, noMatchVal):
	pyDataSet = system.dataset.toPyDataSet(dataSet)
	foundMatch = False
	for row in pyDataSet:
		value = row[searchCol]
		if value == matchVal:
			foundMatch = True
			returnVal = row[resultCol]
			return returnVal
	if foundMatch == False:
		for row in pyDataSet:
			value = row[searchCol]
			if value == noMatchVal:
				foundMatch = True
				returnVal = row[resultCol]
				return returnVal
def dateParse(initialDate, formatString = "yyyy-MM-dd HH:mm"):
	try:
		returnDate = system.date.format(initialDate, formatString)
		returnDate = system.date.parse(returnDate, formatString)
		return returnDate
	except:
		pass
		
