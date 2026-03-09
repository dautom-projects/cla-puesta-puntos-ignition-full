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
