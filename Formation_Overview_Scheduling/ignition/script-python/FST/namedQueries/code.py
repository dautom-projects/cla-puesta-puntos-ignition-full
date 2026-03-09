def getLineLimits():
	lineRangePaths = []
	lineRangePaths.append("[default]Formation/Config/Tables/lineTableMin1")
	lineRangePaths.append("[default]Formation/Config/Tables/lineTableMax1")
	lineRangePaths.append("[default]Formation/Config/Tables/lineTableMin2")
	lineRangePaths.append("[default]Formation/Config/Tables/lineTableMax2")
	lineRanges = system.tag.readBlocking(lineRangePaths)
	lineMin1 = lineRanges[0].value
	lineMax1 = lineRanges[1].value
	lineMin2 = lineRanges[2].value
	lineMax2 = lineRanges[3].value
	return lineMin1, lineMax1, lineMin2, lineMax2
	
def callCurrentSchedule():
	lineMin1, lineMax1, lineMin2, lineMax2 = FST.namedQueries.lineLimits()
	params1 = {"line1Min": lineMin1, "line2Max": lineMax2}
	data = system.db.runNamedQuery("FormationScheduling/currentSchedule", params1)
	return data

def getTableLineQuery1(lineNum, sortReverse = False):
	if lineNum == 1 or lineNum == 2:
		tagPath = "[default]Formation/Config/Tables/lineRange"+str(lineNum)
	else:
		tagPath = "[default]Formation/Config/Tables/tableRanges"
	dsTag = system.tag.readBlocking([tagPath])
	origDataset = dsTag[0].value
	if  sortReverse:
		dataset = system.dataset.sort(origDataset, 0, False)
	else:
		dataset = origDataset
	strList = ""
	listStr = []
	for row in range(dataset.getRowCount()):
		x = dataset.getValueAt(row,0)
		strL = "statusID"+str(x)+" as ["+str(x)+"]"
		listStr.append(strL)
	strList = ",".join(listStr)
	return strList

def getTableLineQuery2(lineNum, sortReverse = False):
		if lineNum == 1 or lineNum == 2:
			tagPath = "[default]Formation/Config/Tables/lineRange"+str(lineNum)
		else:
			tagPath = "[default]Formation/Config/Tables/tableRanges"
		dsTag = system.tag.readBlocking([tagPath])
		dsTag = system.tag.readBlocking([tagPath])
		origDataset = dsTag[0].value
		if  sortReverse:
			dataset = system.dataset.sort(origDataset, 0, False)
		else:
			dataset = origDataset
		strList = ""
		listStr = []
		for row in range(dataset.getRowCount()):
			x = dataset.getValueAt(row,0)
			strL = "["+str(x)+"]"
			listStr.append(strL)
		strList = ",".join(listStr)
		return strList
