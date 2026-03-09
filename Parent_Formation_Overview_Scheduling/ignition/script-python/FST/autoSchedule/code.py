import operator
from operator import itemgetter

import java
from java.util import Date

currentScheduleExcelPath = "[default]Formation/Tables/Schedule/currentScheduleFromExcel"
currentTempPath = "[default]Formation/Tables/Schedule/currentScheduleFromExcelTemp"
lastSchedulePath = "[default]Formation/Tables/Schedule/lastSchedule"
tagMaxPaths = []
tagMaxPaths.append("[default]Formation/Tables/Schedule/AutoSched/max/tablesPerHour1")
tagMaxPaths.append("[default]Formation/Tables/Schedule/AutoSched/max/tablesPerHour2")
tagMaxPaths.append("[default]Formation/Tables/Schedule/AutoSched/max/tableCountForXXHoursFromNow1")
tagMaxPaths.append("[default]Formation/Tables/Schedule/AutoSched/max/tableCountForXXHoursFromNow2")
tagMaxPaths.append("[default]Formation/Tables/Schedule/AutoSched/max/acidChanges1")
tagMaxPaths.append("[default]Formation/Tables/Schedule/AutoSched/max/acidChanges2")
tagMaxPaths.append("[default]Formation/Tables/Schedule/AutoSched/max/groupChanges1")
tagMaxPaths.append("[default]Formation/Tables/Schedule/AutoSched/max/groupChanges2")
testPaths = []
testPaths.append("[default]Formation/Tables/Schedule/AutoSched/test/tablesPerHour1")
testPaths.append("[default]Formation/Tables/Schedule/AutoSched/test/tablesPerHour2")
testPaths.append("[default]Formation/Tables/Schedule/AutoSched/test/tableCountForXXHoursFromNow1")
testPaths.append("[default]Formation/Tables/Schedule/AutoSched/test/tableCountForXXHoursFromNow2")
testPaths.append("[default]Formation/Tables/Schedule/AutoSched/test/acidChanges1")
testPaths.append("[default]Formation/Tables/Schedule/AutoSched/test/acidChanges2")
testPaths.append("[default]Formation/Tables/Schedule/AutoSched/test/groupChanges1")
testPaths.append("[default]Formation/Tables/Schedule/AutoSched/test/groupChanges2")
groupPaths = []
groupPaths.append("[default]Formation/Tables/Schedule/AutoSched/tablesPerHour1")
groupPaths.append("[default]Formation/Tables/Schedule/AutoSched/tablesPerHour2")
groupPaths.append("[default]Formation/Tables/Schedule/AutoSched/tableCountForXXHoursFromNow1")
groupPaths.append("[default]Formation/Tables/Schedule/AutoSched/tableCountForXXHoursFromNow2")
groupPaths.append("[default]Formation/Tables/Schedule/AutoSched/acidChanges1")
groupPaths.append("[default]Formation/Tables/Schedule/AutoSched/acidChanges2")
groupPaths.append("[default]Formation/Tables/Schedule/AutoSched/groupChanges1")
groupPaths.append("[default]Formation/Tables/Schedule/AutoSched/groupChanges2")



from FST import namedQueries
lineMin1, lineMax1, lineMin2, lineMax2 = namedQueries.getLineLimits()

def updateStatusBar(stringVal, intStyle,complete=False):
	paths = ["[default]Formation/Tables/Schedule/AutoSched/AutoScheduleDescription", "[default]Formation/Tables/Schedule/AutoSched/AutoScheduleStyle","[default]Formation/Tables/Schedule/inProgress"]
	system.tag.writeBlocking(paths, [stringVal,intStyle,complete])

def getCurrentSchedule():
	globTags = system.tag.readBlocking(["[default]Formation/Config/sequentialSchedule"]) #check if this site is setup for sequential, 1==Sequential
	sequentialSchedule = globTags[0].value
	tablesSorted = []
	for x in range(lineMin1,lineMax1+1) + range(lineMin2,lineMax2+1):
		table = x
		params1 = {"table": table}
		data = system.db.runNamedQuery("FormationScheduling/currentScheduleTableSort", params1)
	
		try:
			enabled = data.getValueAt(data.getRowCount() - 1,7)
			tablePath = "[default]Formation/Tables/"+str(x)
			enabledTagRead = system.tag.readBlocking([tablePath+"/enabledScheduling", tablePath+"/timeLeft"])
			enabledTable  = enabledTagRead[0].value and str(enabledTagRead[1].quality) == 'Good'
			if data.getRowCount() > 0 and enabled != 0: 
				dataPy = system.dataset.toPyDataSet( data )
				endDate = system.date.format(dataPy[0][2], "yyyy-MM-dd HH:mm") 	#round endDate to prevent bad sorting due to different table udpates
				endDate = system.date.parse(endDate,"yyyy-MM-dd HH:mm")
				endDateHour = system.date.hoursBetween(system.date.now(),endDate )
				alarm = dataPy[data.getRowCount() - 1][6]
				if sequentialSchedule:
					statusSort = 1
				else:
					statusSort = dataPy[data.getRowCount() - 1][8]
				exclusion = 1 		#1=no exclusion, 0=exclude table
				testFormHour = 0 	#for use in testing the formHour later in the script
				count = 0 			#for use in testing the count later in the script
				countLine1 = 0
				countLine2 = 0
				startTimeTrack = system.date.now()
				tableInfo = [ table, endDate, endDateHour, alarm, exclusion, testFormHour, count , countLine1, countLine2, startTimeTrack, statusSort] 
				tablesSorted.append(tableInfo)
			headers = [table, endDate, endDateHour, alarm, exclusion, testFormHour, count , countLine1, countLine2, startTimeTrack, statusSort]
			tableDS = system.dataset.toDataSet(headers,tablesSorted)
		except:
			pass
			print "tablesSorted append failed"
	dataCurrent = system.db.runNamedQuery("FormationScheduling/currentScheduleWithDetails", {})
	try:
		system.tag.writeBlocking(["[default]Formation/Tables/Schedule/currentTablesSorted"],[tableDS])
	except:
		pass
	return tablesSorted, dataCurrent

def getCurrentLists(path):
	exclu = system.tag.readBlocking([path])
	excluPy = system.dataset.toPyDataSet(exclu[0].value)
	excluGroup = []
	excluIn = []
	excluNotIn = []
	for x in excluPy:
		excluGroup.append(x[0])
		try: excluIn.append(    map(int,x[1].split(",") ) )
		except: excluIn.append( [0] )
		try: excluNotIn.append( map(int,x[2].split(",") ) )
		except: excluNotIn.append( [0] )
	return excluGroup, excluIn, excluNotIn

def autoSchedStep1():
	startTime = system.date.now()
	FST.autoSchedule.updateStatusBar("Initializing", 1, 1)
	FST.autoSchedule.initializeTest()
	
	#first pass with smart shuffle
	globTags = system.tag.readBlocking(["[default]Formation/Config/sequentialSchedule"]) #check if this site is setup for sequential, 1==Sequential
	sequentialSchedule = globTags[0].value	
	FST.autoSchedule.updateStatusBar("Smart Shuffling...", 1, 1)
	FST.autoSchedule.sort_smartShuffle()
	writeVals = []
	for row in range(len(groupPaths)):
		writeVals.append(-1)
	system.tag.writeBlocking(groupPaths, writeVals)
	system.tag.writeBlocking(tagMaxPaths, writeVals)
	FST.autoSchedule.updateStatusBar("Initial table set...", 1, 1)
	useManOrder = True
	tablesSorted, dataQuery1 = FST.autoSchedule.getCurrentSchedule()
	FST.autoSchedule.mySlowFunction(useManOrder,dataQuery1)
	initialRun = False
	if sequentialSchedule:
		pass #do nothing right now
	else:
		FST.autoSchedule.sort_smartShuffle(initialRun)
		FST.autoSchedule.updateStatusBar("Evaluating options...", 1, 1)
		FST.autoSchedule.setTableData(useManOrder)
		FST.autoSchedule.updateStatusBar("Sorting by line...", 1, 1)
		
	FST.autoSchedule.sort_SeparateLines() #separate lines
	finishTime = system.date.now()
	secElapsed = system.date.secondsBetween(startTime, finishTime)
	FST.autoSchedule.updateStatusBar("Completed Step 1 in " +str(secElapsed) + " sec", 0, 0)
	return True
	
def autoSchedStep2():
	globTags = system.tag.readBlocking(["[default]Formation/Config/sequentialSchedule"]) #check if this site is setup for sequential, 1==Sequential
	sequentialSchedule = globTags[0].value
	startTime = system.date.now()
	FST.autoSchedule.updateStatusBar("Initializing", 1, 1)
	FST.autoSchedule.initializeTest()
	writeVals = []
	for row in range(len(groupPaths)):
		writeVals.append(-1)
	system.tag.writeBlocking(groupPaths, writeVals)
	system.tag.writeBlocking(tagMaxPaths, writeVals)
	useManOrder = True
	FST.autoSchedule.updateStatusBar("Evaluating options...", 1, 1)
	tablesSorted, dataQuery1 = FST.autoSchedule.getCurrentSchedule()
	FST.autoSchedule.mySlowFunction(useManOrder,dataQuery1)
	FST.autoSchedule.updateStatusBar("Sorting by line...", 1, 1)
	FST.autoSchedule.sort_SeparateLines() #separate lines
	finishTime = system.date.now()
	secElapsed = system.date.secondsBetween(startTime, finishTime)
	FST.autoSchedule.updateStatusBar("Completed Step 2 in " +str(secElapsed) + " sec", 0, 0)
	return True

def autoBackgroundOptimize():
	globTags = system.tag.readBlocking(["[default]Formation/Config/sequentialSchedule"]) #check if this site is setup for sequential, 1==Sequential
	sequentialSchedule = globTags[0].value
	startTime = system.date.now()
	FST.autoSchedule.updateStatusBar("Clearing schedules...", 1, 1)
	FST.autoSchedule.clearSchedules()
	dsTag = system.tag.readBlocking([currentScheduleExcelPath])
	dataset = dsTag[0].value
	FST.autoSchedule.initializeSched(dataset)
	timeOffsetSetting = 30
	FST.autoSchedule.updateStatusBar("Clearing tables...", 1, 1)
	FST.autoSchedule.clearTables()
	writeVals = []
	for row in range(len(groupPaths)):
		writeVals.append(-1)
	system.tag.writeBlocking(groupPaths, writeVals)
	system.tag.writeBlocking(tagMaxPaths, writeVals)
	FST.autoSchedule.updateStatusBar("Running Background optimization...", 1, 1)
	tagForceOrder = system.tag.readBlocking(["[default]Formation/Tables/Schedule/manualIStartTimeFreeze"])
	if tagForceOrder[0].value == 0:
		FST.autoSchedule.updateStatusBar("Smart Shuffling...", 1, 1)
		FST.autoSchedule.sort_smartShuffle()
	useManOrder = True
	FST.autoSchedule.updateStatusBar("Evaluating options, initial...", 1,1)
	tablesSorted, dataQuery1 = FST.autoSchedule.getCurrentSchedule()
	FST.autoSchedule.mySlowFunction(useManOrder,dataQuery1)
	FST.autoSchedule.updateStatusBar("Evaluating options...", 1,1)
	if sequentialSchedule:
			#do nothing right now
			pass
	else:
		if tagForceOrder[0].value == 0:
			FST.autoSchedule.sort_smartShuffle(initialRun = False)
		FST.autoSchedule.setTableData(useManOrder)
		FST.autoSchedule.updateStatusBar("Sorting by line...", 1,1)
	FST.autoSchedule.sort_SeparateLines() #separate lines
	FST.autoSchedule.sendToSchedule()
	finishTime = system.date.now()
	secElapsed = system.date.secondsBetween(startTime, finishTime)
	FST.autoSchedule.updateStatusBar("Completed Optimization in "+str(secElapsed) + " sec", 0, 0)
		#FST.autoSchedule.updateStatusBar("Background failed", 2, 0)

def testConfig():
	try:
		initializedTrue
	except:
		FST.autoSchedule.initializeTest()
	FST.autoSchedule.updateStatusBar("Testing schedule...", 1, 1)
	writeVals = []
	for row in range(len(testPaths)):
		writeVals.append(-1)
	system.tag.writeBlocking(testPaths, writeVals)
	useManOrder = True
	tablesSorted, dataQuery1 = FST.autoSchedule.getCurrentSchedule()
	FST.autoSchedule.mySlowFunction(useManOrder,dataQuery1)
	FST.autoSchedule.mySlowFunction(useManOrder, testConfig=1)
	FST.autoSchedule.updateStatusBar("Metrics updated", 0, 0)

def clearTables():
	tag = system.tag.readBlocking([currentScheduleExcelPath])
	data = tag[0].value
	table = -1
	rowCount = data.getRowCount()
	for row in range(rowCount):
		data = system.dataset.setValue(data, row,colTable, table)
	system.tag.writeBlocking([currentScheduleExcelPath],[data])

def sendToSchedule():
	FST.autoSchedule.updateStatusBar("Sending to schedule..", 1, 1)
	FST.autoSchedule.initializeTest()
	tag = system.tag.readBlocking([currentScheduleExcelPath])
	data = tag[0].value
	dataset = data
	data = system.dataset.sort(data,"StartTime")
	rowsToDelete = []
	startOrder = 0
	startOrderEast = 0
	startOrderWest = 0
	dataTag = system.tag.readBlocking(["[default]Formation/Config/loadTime"])
	dataLoad = dataTag[0].value
	loadTimesDS = dataLoad
	if data.getRowCount() > 0: 
		dataPy = system.dataset.toPyDataSet( data )
		for row in range(data.getRowCount()):
			try: table = int(dataPy[row][colTable])
			except: table = -999
			if table >= lineMin1 and table <= lineMax2: #check for valid table number
				sku =  dataPy[row][colDUF]
				group = str(dataPy[row][colGroup]).upper()
				qty = dataPy[row][colQty]
				priority = dataPy[row][colHot]
				batch = dataPy[row][colBatch]
				formProg = 0 #dataPy[row][13] #not currently found in FDC, only SADC
				timeLeft = float(dataPy[row][colFormHour])*60 #in minutes
				formHours = dataPy[row][colFormHour]
				refillAcid = dataPy[row][colAcid]
				try: bathLevel = 0.0 #float(dataPy[row][16]) #not currently found in FDC, only SADC
				except: bathLevel = 0.0
				if priority == 1 or priority == "1":
					label = "(HOT)" + group + "-" + str (sku)
				else:
					label = group + "-" + str (sku)
				eastWest =  dataPy[row][colLine]
				date = system.date.now() #dataPy[row][1] #not currently found in FDC, only SADC
				shift = 0 #dataPy[row][2] #not currently found in FDC, only SADC
				inRoom = 0 #dataPy[row][3] #not currently found in FDC, only SADC
				prodOrder = 0 #dataPy[row][4] #not currently found in FDC, only SADC
				legacy = 0 #dataPy[row][5] #not currently found in FDC, only SADC
				pos = 0 #dataPy[row][10] #not currently found in FDC, only SADC
				gpoDoof = 0 #dataPy[row][11]  #not currently found in FDC, only SADC

				addTime = FST.commonScripts.findMatch(loadTimesDS, group, 'group', 'value', 'default')
				
				try: startTime = dataPy[row][colStartT]
				except: startTime = "0"
	#					print "Timeleft = " + str(timeLeft)
	#					print "Formhours = " + str(formHours)
				print "Group = " + str(group) + " added at Table = " + str(table) + " startOrder = " + str(startOrder) + " at " + str(startTime)
				
				setAuto = dataPy[row][colSetAuto]
				#set startOrder by side
				if table >= lineMin2:
					print "South representin'"
					startOrderWest = startOrderWest + 1
					startOrder = startOrderWest
				else: 
					startOrderEast = startOrderEast + 1
					startOrder = startOrderEast
				#startOrder = startOrder + 1 #dataPy[row][20]
				truckOrder = dataPy[row][colTruckOrder]
				truckOrderIndex = dataPy[row][colTruckOrderIndex]
				truckNotes = dataPy[row][colTruckNotes]
				
				params = {"table": table,"label": label, "timeLeft": timeLeft, "sku": sku ,"group": group, "formProg": formProg, "formHours": formHours,"refillAcid": refillAcid, "bathLevel":bathLevel, "priority":priority,"qty":qty,"eastWest":eastWest,"date":date,"shift":shift,"inRoom":inRoom,"prodOrder":prodOrder,"legacy":legacy,"pos":pos,"gpoDoof":gpoDoof,"batch":batch,"addTime":addTime, "startTime":startTime,"setAuto":setAuto,"startOrder":startOrder, "truckNotes": truckNotes, "truckOrder":truckOrder, "truckOrderIndex":truckOrderIndex }
				# Run the Named Query
				system.db.runNamedQuery("FormationScheduling/insertEventAuto", params)
				rowsToDelete.append(row)
	dataWrite = system.dataset.deleteRows(data,rowsToDelete)
	system.tag.writeBlocking([currentScheduleExcelPath],[dataWrite])
	FST.autoSchedule.updateStatusBar("Events scheduled..", 0, 0)

def clearSchedules():
	FST.autoSchedule.updateStatusBar("Clearing schedule..", 1, 1)
	try:
		initializedTrue
	except:
		FST.autoSchedule.initializeTest()
	clearFromTag = system.tag.readBlocking(["[default]Formation/Config/dateClearFrom"]) #get clear from date
	clearFrom = clearFromTag[0].value
	#read items to local table
	newRows = []
	params = {"statusID":3, "lineMin1":lineMin1,"lineMax2":lineMax2}
	data = system.db.runNamedQuery("FormationScheduling/currentScheduleFuture", params)
	print data
	if data.getRowCount() > 0:
		for row in range(data.getRowCount()):
			startTime = data.getValueAt(row,"StartDate")
			if startTime >= clearFrom:
				eastWest = data.getValueAt(row,"TableAlias1")
				date = data.getValueAt(row,"DateSched")
				shift = data.getValueAt(row,"Shift")
				inRoom = data.getValueAt(row,"InRoom")
				prodOrder = data.getValueAt(row,"ProdOrder")
				legacy = data.getValueAt(row,"LegacyNumber")
				sku = data.getValueAt(row,"DUFWRev")
				group = data.getValueAt(row,"Group")
				qty = data.getValueAt(row,"Qty")
				priority = data.getValueAt(row,"Priority")
				pos = data.getValueAt(row,"Pos")
				gpoDoof = data.getValueAt(row,"GpoDoof")
				formProg = data.getValueAt(row,"FormProg")
				formHrs = data.getValueAt(row,"FormHrs")
				refillAcid = data.getValueAt(row,"RefillAcid")
				bathLevel = data.getValueAt(row,"BathLevel")
				table = data.getValueAt(row,"Table")
				batch = data.getValueAt(row,"Batch")
				startOrder = data.getValueAt(row,"StartOrder")
				truckNotes = data.getValueAt(row,"TruckNotes")
				truckOrder = data.getValueAt(row,"TruckOrder")
				truckOrderIndex = data.getValueAt(row,"TruckOrderIndex")
				marked = "" #FDC only
				notes = "" #FDC only
				setAuto = 1
				
				newRows.append( [ priority, notes,sku,group,formHrs,refillAcid,bathLevel,qty,qty,batch,eastWest,table,startTime,setAuto,startOrder, truckNotes, truckOrder, truckOrderIndex ] ) 
				# for reference headers = [namePartNumber,nameGroup,nameLine,nameHot,nameFormHrs,nameAcid,nameQty,nameBatch,nameTable,nameStartTime,nameSetAuto,nameStartOrder]
	#print newRows
	dataPrepTag = system.tag.readBlocking([currentScheduleExcelPath])
	dataPrep = dataPrepTag[0].value
	#print dataPrep
	dataNew = system.dataset.addRows(dataPrep,newRows)
	system.tag.writeBlocking([currentScheduleExcelPath],[dataNew])
	
	#clear items from schedule
	params = {"clearFrom": clearFrom}
	# Run the Named Query
	system.db.runNamedQuery("FormationScheduling/updateScheduleStatusAll", params)
	headers = []
	for x in range(dataPrep.getColumnCount()):
		nameCol = dataPrep.getColumnName(x)
		headers.append(nameCol)
	vals = []
	oldSched = system.dataset.toDataSet(headers,vals)
	oldItems = system.dataset.addRows(oldSched,newRows)
	system.tag.writeBlocking([lastSchedulePath],[oldItems])
	
	FST.autoSchedule.updateStatusBar("Schedule Cleared..", 0, 0)
	
def initializeTest():
	dsTag = system.tag.readBlocking([currentScheduleExcelPath])
	dataset = dsTag[0].value
	FST.autoSchedule.initializeSched(dataset)

def initializeSched(dataset):
	global sourceData
	global iterationCount
	global initializedTrue
	global currTempData
	global timeOffsetSetting
	timeOffsetSetting = 60
	iterationCount = 0
	sourceData = dataset
	currTempData = dataset
	system.tag.writeBlocking([currentTempPath],[dataset])
	#column header names
	try:
		colHrId = dataset.getColumnIndex(" HRS ")
		nameFormHrs = " HRS "
	except:
		nameFormHrs = "HRS"
	try:
		colHrIdx = dataset.getColumnIndex(" ACID ")
		nameAcid = " ACID "
	except:
		nameAcid = "ACID"
	try:
		colHrIdx = dataset.getColumnIndex(" WATER ")
		nameBathLevel = " WATER "
	except:
		nameBathLevel = "WATER"
	
	namePartNumber = "Part Number"
	nameGroup = "Group Size"
	nameBatch = "Batch"
	nameQty = "Scheduled"
	nameTable = "Table"
	nameStartTime = "StartTime"
	nameSetAuto = "SetAuto"
	nameStartOrder = "StartOrder"
	nameHot = "Priority"
	nameLine = "Line"
	nameTruckNotes = "TruckNotes"
	nameTruckOrder = "TruckOrder"
	nameTruckIndex = "OrderIndex"
	#dynamic column indexes
	global colDUF
	global colGroup
	global colBatch
	global colFormHour
	global colAcid
	global colQty
	global colTable
	global colStartT
	global colSetAuto
	global colStartOrder
	global colHot
	global colLine
	global colTruckNotes
	global colTruckOrder
	global colTruckOrderIndex
	
	colDUF = dataset.getColumnIndex(namePartNumber)
	colGroup = dataset.getColumnIndex(nameGroup)
	colBatch = dataset.getColumnIndex(nameBatch)
	colFormHour = dataset.getColumnIndex(nameFormHrs)
	colAcid = dataset.getColumnIndex(nameAcid)
	colQty = dataset.getColumnIndex(nameQty)
	colTable = dataset.getColumnIndex(nameTable)
	colStartT = dataset.getColumnIndex(nameStartTime)
	colSetAuto = dataset.getColumnIndex(nameSetAuto)
	colStartOrder =  dataset.getColumnIndex(nameStartOrder) 
	colHot = dataset.getColumnIndex(nameHot)
	colLine = dataset.getColumnIndex(nameLine)
	try:
		colTruckOrder = dataset.getColumnIndex(nameTruckOrder)
	except:
		pass
	try:
		colTruckOrderIndex = dataset.getColumnIndex(nameTruckIndex)
	except:
		pass
	try:
		colTruckNotes = dataset.getColumnIndex(nameTruckNotes)
	except:
		pass
	initializedTrue = True

def getLocation(tableSet):
	try:
		tableSet = int(tableSet)
		if  tableSet >= lineMin1 and tableSet <= lineMax1:
			lineTable = 1
		elif tableSet >= lineMin2 and tableSet <= lineMax2:
			lineTable = 2
		else:
			lineTable = 0
		return lineTable
	except:
		return 0

def setTableData(useManOrder):
	global iterationCount
	try:
		initializedTrue
	except:
		FST.autoSchedule.initializeTest()
	#find single groups and reorder and retest	
	tag = system.tag.readBlocking([currentScheduleExcelPath,"[default]Formation/Tables/Schedule/config/lockPriorities"])
	data = tag[0].value
	lockPrio = tag[1].value
	#currTempData = data
 	system.tag.writeBlocking([currentTempPath],[data]) #copy main to temp
	tablesSorted, dataQuery = FST.autoSchedule.getCurrentSchedule()
	singles = 0
	rowCount = data.getRowCount()
	for row in range(rowCount): #test each row for single - group focused
		tag = system.tag.readBlocking([currentTempPath]) #clear tags
		data = tag[0].value #clear tags
		#data = currTempData
		setAuto = data.getValueAt(row,colSetAuto)
		prio = int(data.getValueAt(row,colHot))
		tableSet = data.getValueAt(row,colTable)
		lineTable = FST.autoSchedule.getLocation(tableSet)
		if setAuto == 1:
			if row+1 < rowCount and data.getValueAt(row,colGroup) != data.getValueAt(row+1,colGroup) and (row == 0 or data.getValueAt(row,colGroup) != data.getValueAt(row-1,colGroup)): #found single
				matchRow = 0 
				singles = singles + 1
				#look for matches starting at last row
				for j in range(row+1,rowCount):
					setAuto = data.getValueAt(j,colSetAuto)
					tableJ = data.getValueAt(j,colTable)
					lineJ = FST.autoSchedule.getLocation(tableJ)
					if lineJ == lineTable: #Check that line is not switching; changing lines should skip first line2/3/etc event and check next
						if setAuto == 1 and data.getValueAt(row,colGroup) == data.getValueAt(j,colGroup): #if next row matches, and that one is not single
							#check to make sure this match is single
							if j+1 < rowCount and j-1 >= 0 and data.getValueAt(j,colGroup) != data.getValueAt(j+1,colGroup) and data.getValueAt(j,colGroup) != data.getValueAt(j-1,colGroup): #found single
								#found match that is single and can be moved for testg
								valHot = int(data.getValueAt(j,colHot))
								if ((prio == valHot) or lockPrio == 0 or ((prio != 1 and lockPrio == 1) or (prio >= 4 and valHot >= 4 and lockPrio == 3 ))):  	  #check to see if priorities match, currently only check for priorit
									print "FoundMatchGroup= "+ str(row) +" MatchRow= " + str(j) + " found match at data.getValueAt(row,colGroup) = " + str(data.getValueAt(row,colGroup)) + " data.getValueAt(j,colGroup) = " + str(data.getValueAt(j,colGroup))
									dataPy = system.dataset.toPyDataSet(data)
									data = system.dataset.addRow(data, row+1, dataPy[j])#newRow)
									data = system.dataset.deleteRow(data, j+1)
									#currTempData = data
									system.tag.writeBlocking([currentTempPath],[data]) #clear tags
									dataQuery1 = dataQuery
									FST.autoSchedule.mySlowFunction(useManOrder, dataQuery1) #rerun autosched main script for comparison
									print "--> Go to next match find for testing"
									iterationCount += 1
							
	for row in range(rowCount): #test each row for single - acid focused
		tag = system.tag.readBlocking([currentTempPath])  #clear tags
		data = tag[0].value #clear tags
		#data = currTempData
		setAuto = data.getValueAt(row,colSetAuto)
		prio = int(data.getValueAt(row,colHot))
		tableSet = data.getValueAt(row,colTable)
		lineTable = FST.autoSchedule.getLocation(tableSet)		
		if setAuto == 1:
			if row+1 < rowCount and data.getValueAt(row,colAcid) != data.getValueAt(row+1,colAcid) and (row == 0 or data.getValueAt(row,colAcid) != data.getValueAt(row-1,colAcid)): #found single
				matchRow = 0 
				singles = singles + 1
				#look for matches starting at last row
				for j in range(row+1,rowCount):
					setAuto = data.getValueAt(j,colSetAuto)
					tableJ = data.getValueAt(j,colTable)
					lineJ = FST.autoSchedule.getLocation(tableJ)
					if lineJ == lineTable: #Check that line is not switching; changing lines should skip first line2/3/etc event and check next
						if setAuto == 1 and data.getValueAt(row,colAcid) == data.getValueAt(j,colAcid): #if next row matches, and that one is not single
							#check to make sure this match is single
							if j+1 < rowCount and j-1 >= 0 and data.getValueAt(j,colAcid) != data.getValueAt(j+1,colAcid) and data.getValueAt(j,colAcid) != data.getValueAt(j-1,colAcid): #found single
								#found match that is single and can be moved for testing
								valHot = int(data.getValueAt(j,colHot))
								if ((prio == valHot) or lockPrio == 0 or ((prio != 1 and lockPrio == 1) or (prio >= 4 and valHot >= 4 and lockPrio == 3 ))) : 						
									print "FoundMatchAcid= "+ str(row) +" MatchRow= " + str(j) + " found match at data.getValueAt(row,colAcid) = " + str(data.getValueAt(row,colAcid)) + " data.getValueAt(j,colAcid) = " + str(data.getValueAt(j,colAcid))
									dataPy = system.dataset.toPyDataSet(data)
									data = system.dataset.addRow(data, row+1, dataPy[j])#newRow
									data = system.dataset.deleteRow(data, j+1)
									#currTempData = data
									system.tag.writeBlocking([currentTempPath],[data])  #clear tags
									dataQuery2 = dataQuery
									FST.autoSchedule.mySlowFunction(useManOrder,dataQuery2) #rerun autosched main script for comparison
									iterationCount += 1

	FST.autoSchedule.mySlowFunction(useManOrder,dataQuery)
def shuffleLine(lineData):
	try:
		initializedTrue
	except:
		FST.autoSchedule.initializeTest()
	#shuffle schedule testing
	shuffle = lineData #for testing shuffle logic in/out
	smartSel = True
	if smartSel:
		#break out line
		#break out priority 1s and do a shuffle on only those
		prio1 = []
		others = []
		for x in shuffle:
			if x[colHot] == 1 or x[colHot] == "1":
				prio1.append(x)
			else:
				others.append(x)
		
		listLen = len(lineData)
		prio1Len = len(prio1)
		othersLen = len(others)
		shuffle = []
		
		#execute for priority 1 items:
		middlePointer = int(((prio1Len-1)/3) + 1)
		slice2IndexEnd = middlePointer + middlePointer
		slice1 = prio1[:middlePointer]
		slice2 = prio1[middlePointer:slice2IndexEnd]
		slice2 = sorted(slice2,reverse=True, key=operator.itemgetter(colAcid,colFormHour,colGroup)) #focus on Acid changeover minimization
		slice3 = prio1[slice2IndexEnd:]
		slice3 = sorted(slice3,reverse=True, key=operator.itemgetter(colAcid,colFormHour,colGroup)) #focus on Acid changeover minimization
		start1 = 1.0 #formation side 1 (i.e. north/east)
		for x in slice3:
			x[colStartOrder] = start1
			start1 = start1 + 1.0
		start1 = 1.0
		for x in slice2:
			x[colStartOrder] = start1
			start1 = start1 + 1.0
		start1 = 1.0
		for x in slice1:
			x[colStartOrder] = start1
			start1 = start1 + 1.0
		prio1 = slice3 + slice2 + slice1
		
		#execute for others
		middlePointer = int(((othersLen-1)/3) + 1)
		slice2IndexEnd = middlePointer + middlePointer
		slice1 = others[:middlePointer]
		slice2 = others[middlePointer:slice2IndexEnd]
		slice2 = sorted(slice2,reverse=True, key=operator.itemgetter(colAcid,colFormHour,colGroup)) #focus on Acid changeover minimization
		slice3 = others[slice2IndexEnd:]
		slice3 = sorted(slice3,reverse=True, key=operator.itemgetter(colAcid,colFormHour,colGroup)) #focus on Acid changeover minimization
		start = 1.0
		start1 = 1.0 #formation side 1 (i.e. north/east)
		for x in slice3:
			x[colStartOrder] = start1
			start1 = start1 + 1.0
		start1 = 1.0
		for x in slice2:
			x[colStartOrder] = start1
			start1 = start1 + 1.0
		start1 = 1.0
		for x in slice1:
			x[colStartOrder] = start1
			start1 = start1 + 1.0
		others = slice3 + slice2 + slice1
		
		shuffle = prio1 + others
		shuffle = sorted(shuffle,reverse=False, key=operator.itemgetter(colFormHour,colGroup,colAcid))
		shuffle = sorted(shuffle,reverse=False, key=operator.itemgetter(colHot,colStartOrder))#sort by priority
		#shuffle = sorted(shuffle,reverse=False, key=operator.itemgetter(colLine))#sort by priority
	return shuffle
	
def sort_smartShuffle(initialRun = True):
	globTags = system.tag.readBlocking(["[default]Formation/Config/sequentialSchedule"]) #check if this site is setup for sequential, 1==Sequential
	sequentialSchedule = globTags[0].value
	FST.autoSchedule.initializeTest()
	dsTag = system.tag.readBlocking([currentScheduleExcelPath])
	dataset = dsTag[0].value
	dataPy = system.dataset.toPyDataSet(dataset)
	dataTemp = []
	for j in dataPy:
		rowList = list(j)
		rowList[colFormHour] = float(rowList[colFormHour])
		dataTemp.append(rowList)
	dataPy = dataTemp
	dataPy = sorted(dataPy,reverse=True, key=operator.itemgetter(colFormHour,colGroup,colAcid))
	dataPy = sorted(dataPy,reverse=False, key=operator.itemgetter(colHot))#sort by priority
	headers = system.dataset.getColumnHeaders(dataset)
	
	valPaths = []
	valPaths.append("[default]Formation/Tables/Schedule/config/EnabledLine1OnlyGoesLine1")
	valPaths.append("[default]Formation/Tables/Schedule/config/EnabledLine2OnlyGoesLine2")
	valReads = system.tag.readBlocking(valPaths)
	onlyL1 = valReads[0].value
	onlyL2 = valReads[1].value
	#convert to list
	dataList1 = []
	dataList2 = []
	dataElse = []
	for x in range(len(dataPy)):
		tableSet = dataPy[x][colTable]
		if initialRun:
			if dataPy[x][colLine] == "1":
				if onlyL1:
					dataList1.append(list(dataPy[x]))
				else:
					dataElse.append(list(dataPy[x]))
			elif dataPy[x][colLine] == "2":
				if onlyL2:
					dataList2.append(list(dataPy[x]))
				else:
					dataElse.append(list(dataPy[x]))
			else:
				dataElse.append(list(dataPy[x]))
		else:
			lineTable = FST.autoSchedule.getLocation(tableSet)
			if lineTable == 1:
				dataList1.append(list(dataPy[x]))
			elif lineTable == 2:
				dataList2.append(list(dataPy[x]))
			else:
				dataElse.append(list(dataPy[x]))
	newDataPy1 = dataList1
	newDataPy1 = sorted(newDataPy1,reverse=True, key=operator.itemgetter(colFormHour,colGroup,colAcid))
	newDataPy2 = dataList2
	newDataPy2 = sorted(newDataPy2,reverse=True, key=operator.itemgetter(colFormHour,colGroup,colAcid))
	newDataPyO = dataElse
	newDataPyO = sorted(newDataPyO,reverse=True, key=operator.itemgetter(colFormHour,colGroup,colAcid))
	if sequentialSchedule:
		shuffle1 = sorted(newDataPy1,reverse=False, key=operator.itemgetter(colHot))
		shuffle2 = sorted(newDataPy2,reverse=False, key=operator.itemgetter(colHot)) 
		shuffleO = sorted(newDataPyO,reverse=False, key=operator.itemgetter(colHot))
	else:
		shuffle1 = FST.autoSchedule.shuffleLine(newDataPy1)
		shuffle2 = FST.autoSchedule.shuffleLine(newDataPy2)
		shuffleO = FST.autoSchedule.shuffleLine(newDataPyO)
	shuffleNew = shuffle1 + shuffle2 + shuffleO
	for j in shuffleNew:
		j[colStartT] = system.date.parse(j[colStartT])  #not sure why this translation was needed, the date kept faulting during the manual background optimization.  
	
	dataNew = system.dataset.toDataSet(headers,shuffleNew)
	if dataNew.getRowCount() > 0:
		print "SmartShuffle wrote new data"
		system.tag.writeBlocking([currentScheduleExcelPath],[dataNew])
		system.tag.writeBlocking([currentTempPath],[dataNew])
	
def sort_SeparateLines():
	try:
		initializedTrue
	except:
		FST.autoSchedule.initializeTest()
	dsTag = system.tag.readBlocking([currentScheduleExcelPath])
	dataset = dsTag[0].value
	dataPy = system.dataset.toPyDataSet(dataset)
	dataTemp = []
	dataTemp1 = []
	dataTemp2 = []
	for j in dataPy:
		rowList = list(j)
		rowList[colFormHour] = float(rowList[colFormHour])
		tableNum = rowList[colTable]
		if tableNum >= lineMin2:
			dataTemp2.append(rowList)
		else:
			dataTemp1.append(rowList)
	dataTemp = dataTemp1 + dataTemp2
	dataPy = dataTemp
	#dataPy = sorted(dataPy,reverse=False, key=operator.itemgetter(colLine))#sort by priority
	headers = system.dataset.getColumnHeaders(dataset)
	
	#convert to list
	dataList = []
	for x in range(dataset.getRowCount()):
		dataList.append(list(dataPy[x]))
	
	#shuffle schedule testing
	shuffle = dataList #for testing shuffle logic in/out
	
	#pass new dataset
	dataNew = system.dataset.toDataSet(headers,shuffle)

	system.tag.writeBlocking([currentScheduleExcelPath],[dataNew])
	return True
	
def mySlowFunction(useManOrder, dataQueryNew, testConfig=0):
	global iterationCount
	tagMaxPaths = []
	tagMaxPaths.append("[default]Formation/Tables/Schedule/AutoSched/max/tablesPerHour1")
	tagMaxPaths.append("[default]Formation/Tables/Schedule/AutoSched/max/tablesPerHour2")
	tagMaxPaths.append("[default]Formation/Tables/Schedule/AutoSched/max/tableCountForXXHoursFromNow1")
	tagMaxPaths.append("[default]Formation/Tables/Schedule/AutoSched/max/tableCountForXXHoursFromNow2")
	tagMaxPaths.append("[default]Formation/Tables/Schedule/AutoSched/max/acidChanges1")
	tagMaxPaths.append("[default]Formation/Tables/Schedule/AutoSched/max/acidChanges2")
	tagMaxPaths.append("[default]Formation/Tables/Schedule/AutoSched/max/groupChanges1")
	tagMaxPaths.append("[default]Formation/Tables/Schedule/AutoSched/max/groupChanges2")
	testPaths = []
	testPaths.append("[default]Formation/Tables/Schedule/AutoSched/test/tablesPerHour1")
	testPaths.append("[default]Formation/Tables/Schedule/AutoSched/test/tablesPerHour2")
	testPaths.append("[default]Formation/Tables/Schedule/AutoSched/test/tableCountForXXHoursFromNow1")
	testPaths.append("[default]Formation/Tables/Schedule/AutoSched/test/tableCountForXXHoursFromNow2")
	testPaths.append("[default]Formation/Tables/Schedule/AutoSched/test/acidChanges1")
	testPaths.append("[default]Formation/Tables/Schedule/AutoSched/test/acidChanges2")
	testPaths.append("[default]Formation/Tables/Schedule/AutoSched/test/groupChanges1")
	testPaths.append("[default]Formation/Tables/Schedule/AutoSched/test/groupChanges2")
	groupPaths = []
	groupPaths.append("[default]Formation/Tables/Schedule/AutoSched/tablesPerHour1")
	groupPaths.append("[default]Formation/Tables/Schedule/AutoSched/tablesPerHour2")
	groupPaths.append("[default]Formation/Tables/Schedule/AutoSched/tableCountForXXHoursFromNow1")
	groupPaths.append("[default]Formation/Tables/Schedule/AutoSched/tableCountForXXHoursFromNow2")
	groupPaths.append("[default]Formation/Tables/Schedule/AutoSched/acidChanges1")
	groupPaths.append("[default]Formation/Tables/Schedule/AutoSched/acidChanges2")
	groupPaths.append("[default]Formation/Tables/Schedule/AutoSched/groupChanges1")
	groupPaths.append("[default]Formation/Tables/Schedule/AutoSched/groupChanges2")
	globTags = system.tag.readBlocking(["[default]Formation/Config/sequentialSchedule","[default]Formation/Config/dateStartFrom"]) #check if this site is setup for sequential, 1==Sequential
	sequentialSchedule = globTags[0].value
	startFrom = globTags[1].value #set startFromDate for auto scheduling
	isDateBefore = system.date.isBefore(startFrom, system.date.now())
	if isDateBefore:
		startFrom = system.date.now()
	try:
		initializedTrue
	except:
		FST.autoSchedule.initializeTest()
		print "initializedTrue not True"
	#sort Tables and pull current EndDates per table, ignore table if disabled
	#description = "Sort current tables status by EndDate"
	#steps.append(description)
	lastStartTime = system.date.now()
	lastStartTimeLine1 = system.date.now()
	lastStartTimeLine2 = system.date.now()
	tablesTag = system.tag.readBlocking(["[default]Formation/Tables/Schedule/currentTablesSorted"])

	tablesSortedTag = tablesTag[0].value
	pyDS = system.dataset.toPyDataSet(tablesSortedTag)
	tableSort = []
	for row in pyDS:
		newRow = []
		for i in range(len(row)):
			newRow.append(row[i])
		tableSort.append(newRow)
	tableSort = sorted(tableSort,reverse=False,key=operator.itemgetter(1,10,0)) #sort by endDate, status, table
	tableSortLen = len(tableSort)
	#assign Table numbers to priority Table on screen
	#description = "Assign tables to schedule and check for exclusions"
	#steps.append(description)
	if testConfig == 0:
		tagPathNew = currentTempPath
	else:
		tagPathNew = "[default]Formation/Tables/Schedule/currentScheduleToTest"
	dataTag = system.tag.readBlocking([tagPathNew,"[default]Formation/Config/loadTime"])
	#data = currTempData
	data = dataTag[0].value #clear tags
#	for row in range(data.getRowCount()):
#		print data.getValueAt(row,colGroup)
	loadTimesDS = dataTag[1].value
	#create sequence from exclusion dataset
	excluGroup, excluIn, excluNotIn = FST.autoSchedule.getCurrentLists("[default]Formation/Tables/Schedule/exclusions")
	
	
	#assign tables and check for exclusions
	linesSet = system.tag.readBlocking(["[default]Formation/Tables/Schedule/config/EnabledLine1OnlyGoesLine1","[default]Formation/Tables/Schedule/config/EnabledLine2OnlyGoesLine2"])
	line1Set = linesSet[0].value
	line2Set = linesSet[1].value
	#set earliest time to lastStartTime IF the manual button is on
	tagForceOrder = system.tag.readBlocking(["[default]Formation/Tables/Schedule/manualIStartTimeFreeze"]) #read max values saved
	if useManOrder:
		forceOrder = tagForceOrder[0].value
	else:
		forceOrder = 0
	firstLine2Line = False
	firstLine1Line = False
	startComps = []
	for row in range(data.getRowCount()):
		#check for setAuto flag
		setAutoCheck = bool(data.getValueAt(row,colSetAuto))
		if setAutoCheck == 1:
			
			#Check for exclusions, is this group allowed to go on this table? Is the table enabled?
			x = 0
			table = tableSort[x][0]
			for j in tableSort:j[4] = 1 #reset exclusion column	
			currentGroup = data.getValueAt(row,colGroup)
			addTime = FST.commonScripts.findMatch(loadTimesDS, currentGroup, 'group', 'value', 'default')
			
			foundExclu = 0 #used to find first exclusion, in order to manage complex exclusion lists
			#excluGroup = sorted(excluGroup,reverse=True, key=operator.itemgetter(0)) #sort by length
			for i in range(len(excluGroup)): #check to see if excluGroup is in currentGroup
				if excluGroup[i] == currentGroup and excluGroup[i]:
					for j in tableSort:  #set exclusion bit to 0 if it finds an exclusion
						if ( j[0] not in excluIn[i] and 0 not in excluIn[i]) or (j[0] in excluNotIn[i] and 0 not in excluNotIn[i]):
							j[4] = 0
							foundExclu = 1
				if foundExclu == 1: #break for loop when the first exclusion on the list is found
					break

					
			#	make comparison array to test count per hour
			formHr = float(data.getValueAt(row,colFormHour))
			forHrAdjusted = formHr + (addTime/60)
			formHrInt = int(formHr)
			currTable = data.getValueAt(row,colTable)
			schedLocation = data.getValueAt(row,colLine)
#			if len(schedLocation) > 0:
#				pass
#			else:
#				if currTable >= lineMin2 and currTable <= lineMax2:
#					schedLocation = "2"
#				elif currTable >= lineMin1 and currTable <= lineMax1:
#					schedLocation = "1"
			for j in tableSort: 	#set testFormHour column
				j[5] = formHrInt + j[2]  
			for j in tableSort: 	#set count column
				count = 0
				countLine1 = 0 #East = North
				countLine2 = 0 #West = South
				testItem = j[5]
				if j[2] > 0:#ignore count if timeLeft = 0 or within next hour
					for i in tableSort:
						if i[2] == testItem: 
							count = count + 1	#set count column if testForm
							if schedLocation == "2":  #SADC = East/West, FDC = 1 (north), 2(south)
								countLine1 = countLine1 + 1
							elif schedLocation == "1":   #SADC = East/West, FDC = 1 (north), 2(south)
								countLine2 = countLine2 + 1
					j[6] = count
					j[7] = countLine1
					j[8] = countLine2
			#print "CURRENT GROUP = " + currentGroup + " with schedLocation " + schedLocation					

			
			#set table number
			table = -1
			checkForArea = False  
			line1GoLine1Only = False
			line2GoLine2Only = False
			if line2Set == True and schedLocation == "2":   #check for where west is set to go. #SADC = East/West, FDC = 1 (north), 2(south)
				line2GoLine2Only = True
				checkForArea = True
			elif line1Set == True and schedLocation == "1":  #check for where east is set to go. #SADC = East/West, FDC = 1 (north), 2(south)
				line1GoLine1Only = True
				checkForArea = True

			for j in tableSort:
				if schedLocation == "2":   #SADC = East/West, FDC = 1 (north), 2(south)
					count = j[8]
				elif schedLocation == "1":     #SADC = East/West, FDC = 1 (north), 2(south)
					count = j[7]
				else: count = j[6]
				include = j[4]
				if include == 1 and ( (checkForArea and ((line2GoLine2Only and j[0] >= lineMin2 ) or (line1GoLine1Only and j[0] <= lineMax1))) or not checkForArea) and count < 3:# remove as comment, if 3/hour/side is not desired
					table = j[0]
					data = system.dataset.setValue(data, row,colTable, table)				#set table at pos0				
					#set startDate (table has been picked, now set the startTime dynamically)
					if table >= lineMin2 and firstLine2Line == False:   #set first for each side
						#print "found first line2"
						firstLine2Line = True
						lastEndTimeLine2 = j[1]
						lastStartTimeLine2 = j[9]
					if table <=lineMax1 and firstLine1Line == False:
						#print "found first line1"
						firstLine1Line = True
						lastEndTimeLine1 = j[1]
						lastStartTimeLine1 = j[9]
#					if forceOrder == 1: 
#						if table >= lineMin2: 
#							startTimeBase = lastEndTimeLine2 #lastStartTimeLine2
#						else:
#							startTimeBase = lastEndTimeLine1 #lastStartTimeLine1
#						testStartTime = system.date.addMinutes(startTimeBase,int(addTime+5))	
#					else:
					testStartTime = system.date.addMinutes(j[1],int(addTime+5))	 #sets initial testing time
					if testStartTime < startFrom: #make sure to start after start from time set on the screen
						testStartTime = system.date.addMinutes(startFrom,int(addTime+5))
					if forceOrder == 1:
						if table >= lineMin2:  
							lastStartTimeLine2 = system.date.addMinutes(lastStartTimeLine2,int(addTime))
						else: 
							lastStartTimeLine1 = system.date.addMinutes(lastStartTimeLine1,int(addTime))
							#print "resetting time " + str(lastStartTimeLine1)
					else:
						if table >= lineMin2:			#set lastStartTime variable for the side for this row, use line 2 min
							#check to see if any other table on this side is set to a similar startTime, only 1 table can loaded at a time
							conflict = 1
							while conflict == 1:
								conflict = 0
#bug fix bypass 10-28-21, corner case that allows batts to be loaded at the same start time								
#								for i in tableSort:
#									if i[0] >=lineMin2 and i[0] <=lineMax2: #compare with line min/max
#										testMinBetween = abs(system.date.minutesBetween(i[9],testStartTime)) #check timeBetween
#										if testMinBetween < addTime:
#											#print "Found a conflicting west startTime, rechecking startTimes"
#											conflict = 1
#											break
#bug fix 10-28-21, corner case that allows batts to be loaded at the same start time								
								for i in startComps:  
									if i[0] >=lineMin2 and i[0] <=lineMax2: #compare with line min/max
										testMinBetween = abs(system.date.minutesBetween(i[1],testStartTime)) #check timeBetween
										if testMinBetween < addTime:
											conflict = 1
											break
								if conflict == 1:
									testStartTime = system.date.addMinutes(testStartTime,10) #add 10 minutes and redo search
								else:
									lastStartTime = testStartTime 
									break
						else:
							#check to see if any other table on this side is set to a similar startTime
							conflict = 1
							while conflict == 1:
								conflict = 0
#bug fix bypass 10-28-21, corner case that allows batts to be loaded at the same start time								
#								for i in tableSort:  
#									if i[0] >=lineMin1 and i[0] <=lineMax1: #compare with line min/max
#										testMinBetween = abs(system.date.minutesBetween(i[9],testStartTime)) #check timeBetween
#										if testMinBetween < addTime:
#											#print "Found a conflicting east startTime, rechecking startTimes"
#											conflict = 1
#											#if j[0] == 6: print "Found conflict @ Table = " + str(i[0]) + " with i[9] = " + str(i[9]) + " and testStartTime = " + str(testStartTime) + "with testMinBetween = " + str(testMinBetween)
#											break
#bug fix 10-28-21, corner case that allows batts to be loaded at the same start time								
								for i in startComps:  
									if i[0] >=lineMin1 and i[0] <=lineMax1: #compare with line min/max
										testMinBetween = abs(system.date.minutesBetween(i[1],testStartTime)) #check timeBetween
										if testMinBetween < addTime:
											conflict = 1
											break
								if conflict == 1:
									testStartTime = system.date.addMinutes(testStartTime,10) #add 10 minutes and redo search
								else:
									lastStartTime = testStartTime 
									break
					if table >= lineMin2 and forceOrder == False:			#move back temp variable for side
						lastStartTimeLine2 = lastStartTime
					elif forceOrder == 0: 
						lastStartTimeLine1 = lastStartTime
					if forceOrder == 0: 
						j[9] = lastStartTime
						startComps.append([table, j[9] ])
					else: 
						if table >= lineMin2: 
							j[9] = system.date.addMinutes(lastStartTimeLine2,int(addTime))	
							if j[9] < j[1]: j[9] = system.date.addMinutes(j[1],int(addTime))
							lastStartTimeLine2 = j[9]
						else:		   
							j[9] = system.date.addMinutes(lastStartTimeLine1,int(addTime))	
							if j[9] < j[1]: j[9] = system.date.addMinutes(j[1],int(addTime))
							lastStartTimeLine1 = j[9]		
					data = system.dataset.setValue(data, row,colStartT, j[9])				#set startTime
					timeOffset = int(formHr*60)
					j[1] = system.date.addMinutes(j[9], timeOffset)				#offset current EndDate and change formHr to minutes
					if table >= lineMin2: 
						lastEndTimeLine2 = j[1]
					else:
						lastEndTimeLine1 = j[1]
					j[2] = system.date.hoursBetween(system.date.now(),j[1] )				#update EndDateHour
					tableSort = sorted(tableSort,reverse=False,key=operator.itemgetter(1,10,0))		#re-sort tableSorted Dataset
					break
			if table == -1: #if table is still zero, then go and sort tables by count,enddate,table
				#print "cmon now"
				tableSort = sorted(tableSort,reverse=False,key=operator.itemgetter(5,6,1,10,0))	
				for j in tableSort:
					include = j[4]
					if include == 1 and ( (checkForArea and ((line2GoLine2Only and j[0] >= lineMin2) or (line1GoLine1Only and j[0] <= lineMax1))) or not checkForArea):
						table = j[0]
						data = system.dataset.setValue(data, row,colTable, table)				#set table at pos0
						
						#set startDate (table has been picked, now set the startTime dynamically)
						#find the initial startTime for comparison, this is the earliest it can be, add 5 for offset based on update delay
						#set earliest time to lastStartTime IF the manual button is on
						if table >= lineMin2 and firstLine2Line == 0:   #set first for each side
							firstLine2Line == True
							lastEndTimeLine2 = j[1]
						if table <=lineMax1 and firstLine1Line == 0:
							firstLine1Line == True
							lastEndTimeLine1 = j[1]
						testStartTime = system.date.addMinutes(j[1],int(addTime+5))	

						if forceOrder == 1: 
							if table >= lineMin2:  
								lastStartTimeLine2 = system.date.addMinutes(lastStartTimeLine2,int(addTime))
								lastStartTime = lastStartTimeLine2 #system.date.addMinutes(lastStartTimeLine2,int(addTime))
	
							else: 
								lastStartTimeLine1 = system.date.addMinutes(lastStartTimeLine1,int(addTime))
								lastStartTime = lastStartTimeLine1 #system.date.addMinutes(lastStartTimeLine1,int(addTime))
						else:						
							if table >= lineMin2: 			#set lastStartTime variable for the side for this row
								#check to see if any other table on this side is set to a similar startTime
								conflict = 1
								while conflict == 1:
									conflict = 0
#bug fix bypass 10-28-21, corner case that allows batts to be loaded at the same start time								
#								for i in tableSort:
#									if i[0] >=lineMin2 and i[0] <=lineMax2: #compare with line min/max
#										testMinBetween = abs(system.date.minutesBetween(i[9],testStartTime)) #check timeBetween
#										if testMinBetween < addTime:
#											#print "Found a conflicting west startTime, rechecking startTimes"
#											conflict = 1
#											break
#bug fix 10-28-21, corner case that allows batts to be loaded at the same start time								
								for i in startComps:  
									if i[0] >=lineMin2 and i[0] <=lineMax2: #compare with line min/max
										testMinBetween = abs(system.date.minutesBetween(i[1],testStartTime)) #check timeBetween
										#print "Cmon noowww For table = " + str(table) +" compare against table = " + str(i[0]) +  "  testMinBetween = " + str(testMinBetween) + "; addTime =" + str(addTime) +" testStartTime = " + str(testStartTime) + " i[1] = " + str(i[1])
										if testMinBetween < addTime:
											#print "Found a conflicting east startTime, rechecking startTimes"
											conflict = 1
											#if j[0] == 6: print "Found conflict @ Table = " + str(i[0]) + " with i[9] = " + str(i[9]) + " and testStartTime = " + str(testStartTime) + "with testMinBetween = " + str(testMinBetween)
											break
									if conflict == 1:
										testStartTime = system.date.addMinutes(testStartTime,10) #add 10 minutes and redo search
									else:
										lastStartTime = testStartTime 
										break
							else:
								#check to see if any other table on this side is set to a similar startTime
								conflict = 1
								while conflict == 1:
									conflict = 0
#bug fix bypass 10-28-21, corner case that allows batts to be loaded at the same start time								
#								for i in tableSort:  
#									if i[0] >=lineMin1 and i[0] <=lineMax1: #compare with line min/max
#										testMinBetween = abs(system.date.minutesBetween(i[9],testStartTime)) #check timeBetween
#										if testMinBetween < addTime:
#											#print "Found a conflicting east startTime, rechecking startTimes"
#											conflict = 1
#											#if j[0] == 6: print "Found conflict @ Table = " + str(i[0]) + " with i[9] = " + str(i[9]) + " and testStartTime = " + str(testStartTime) + "with testMinBetween = " + str(testMinBetween)
#											break
#bug fix 10-28-21, corner case that allows batts to be loaded at the same start time								
								for i in startComps:  
									if i[0] >=lineMin1 and i[0] <=lineMax1: #compare with line min/max
										testMinBetween = abs(system.date.minutesBetween(i[1],testStartTime)) #check timeBetween
										#print "Cmon noowww For table = " + str(table) +" compare against table = " + str(i[0]) +  "  testMinBetween = " + str(testMinBetween) + "; addTime =" + str(addTime) +" testStartTime = " + str(testStartTime) + " i[1] = " + str(i[1])
										if testMinBetween < addTime:
											#print "Found a conflicting east startTime, rechecking startTimes"
											conflict = 1
											#if j[0] == 6: print "Found conflict @ Table = " + str(i[0]) + " with i[9] = " + str(i[9]) + " and testStartTime = " + str(testStartTime) + "with testMinBetween = " + str(testMinBetween)
											break
									if conflict == 1:
										testStartTime = system.date.addMinutes(testStartTime,10) #add 10 minutes and redo search
									else:
										lastStartTime = testStartTime 
										break
								
						if table >= lineMin2 and forceOrder == False:			#move back temp variable for side
							lastStartTimeLine2 = lastStartTime
						elif forceOrder == 0: 
							lastStartTimeLine1 = lastStartTime
						if forceOrder == 0: 
							j[9] = lastStartTime
							startComps.append([table, j[9] ])
						else: 
							if table >= lineMin2: 
								j[9] = system.date.addMinutes(lastStartTimeLine2,int(addTime))	
								if j[9] < j[1]: j[9] = system.date.addMinutes(j[1],int(addTime))
								lastStartTimeLine2 = j[9]
							else:		   
								j[9] = system.date.addMinutes(lastStartTimeLine1,int(addTime))	
								if j[9] < j[1]: j[9] = system.date.addMinutes(j[1],int(addTime))
								lastStartTimeLine1 = j[9]
						data = system.dataset.setValue(data, row,colStartT, j[9])				#set startTime
						timeOffset = int(formHr*60)
						j[1] = system.date.addMinutes(j[9], timeOffset)				#offset current EndDate and change formHr to minutes
						if table >= lineMin2: 
							lastEndTimeLine2 = j[1]
						else:
							lastEndTimeLine1 = j[1]
						j[2] = system.date.hoursBetween(system.date.now(),j[1] )				#update EndDateHour
						tableSort = sorted(tableSort,reverse=False,key=operator.itemgetter(1,10,0))		#re-sort tableSorted Dataset
						break
			if table <0:
				table = -999
				setFalse = 0
				data = system.dataset.setValue(data, row,colTable, table)
				data = system.dataset.setValue(data, row, colSetAuto, setFalse)
		else:
			table = -1
			data = system.dataset.setValue(data, row,colTable, table)
		#print "Table chosen is = " + str(table)
	#calculate goals and metrics for this auto sched table
	#variables
	tablecount1 = 0.0
	tablecount2 = 0.0
	tablesperhour1 = 0.0
	tablesperhour2 = 0.0
	acidChanges1 = 0.0
	acidChanges2 = 0.0
	groupChanges1 = 0.0
	groupChanges2 = 0.0
	lastGroup1 = ""
	lastGroup2 = ""
	lastAcid1 = ""
	lastAcid2 = ""
	tagHoursFromNow = system.tag.readBlocking(["[default]Formation/Tables/Schedule/AutoSched/hourFromNowToInclude"])
	hoursFromNow = int(tagHoursFromNow[0].value) #use this to compare to if < this time
	if startFrom > system.date.now():
		timeFromNowEnd = system.date.addHours(startFrom,hoursFromNow)     #use this to compare to if < this time
		timeFromNowStartOffset = system.date.addMinutes(startFrom,30) #this is used to ignore the first XXXX minutes from the current time
	else:
		timeFromNowEnd = system.date.addHours(system.date.now(),hoursFromNow)     #use this to compare to if < this time
		timeFromNowStartOffset = system.date.addMinutes(system.date.now(),30) #this is used to ignore the first XXXX minutes from the current time
	#run scores for new additions		
	dataOriginal = data
	dataSort = data #copy data
	#add endTime column
	colCount = dataSort.getColumnCount()
	columnName = "endTime"
	colEndTime = columnName
	columnData = []
	for i in range(dataSort.getRowCount()):
		formHr = float(dataSort.getValueAt(row,colFormHour))
		minOffset = int(formHr*60)
		startTime = dataSort.getValueAt(row,colStartT)
		startDate = system.date.parse(startTime)
		endTime = system.date.addMinutes(startDate, minOffset)	#add form and starttime to get endtimes
		columnData.append(endTime)
	dataSort = system.dataset.addColumn(dataSort, colCount, columnData, colEndTime, java.util.Date)
	dataSort = system.dataset.sort(dataSort, colEndTime)		#re-sort tableSorted Dataset
	data = dataSort

	changeTimes = system.tag.readBlocking(["[default]Formation/Config/acidChanges","[default]Formation/Config/groupChanges"])
	groupTime = 0
	acidTime = 0
	for row in range(data.getRowCount()):  
		formHr = float(data.getValueAt(row,colFormHour))
		minOffset = int(formHr*60)
		startTime = data.getValueAt(row,colStartT)
		startDate = system.date.parse(startTime)
		endTime = system.date.addMinutes(startDate, minOffset)
		setAuto = data.getValueAt(row, colSetAuto)
		if data.getValueAt(row, colTable) >= lineMin2: 	#side mapping
			line = 2
		else:	
			line = 1

		startTimeComparison = timeFromNowStartOffset #start time comparison
		endTimeComparison = timeFromNowEnd #end time comparison
		#print "startTimeComparison = " + str(startTimeComparison) + " endTime = " + str(endTime)+ " endTimeComparison =" + str(endTimeComparison)
		if endTime > startTimeComparison and endTime < endTimeComparison and setAuto == 1: 		#only consider if endtime is in between start and end times
			if line == 1: tablecount1 = tablecount1 + 1  #calc tablecounts by side
			if line == 2: tablecount2 = tablecount2 + 1
			
			group = data.getValueAt(row,colGroup)  #calc group changes
			if line == 1 and lastGroup1 != group:
				groupChanges1 = groupChanges1 + 1
				lastGroup1 = group
				groupTime = groupTime + FST.commonScripts.findMatch(changeTimes[1].value, group, 'group', 'value', 'default')	
			if line == 2 and lastGroup2 != group:					
				groupChanges2 = groupChanges2 + 1
				lastGroup2 = group
				groupTime = groupTime + FST.commonScripts.findMatch(changeTimes[1].value, group, 'group', 'value', 'default')	
			
			acid = data.getValueAt(row,colAcid)  #calc acid changes
			if line == 1 and lastAcid1 != acid:
				acidChanges1 = acidChanges1 + 1
				lastAcid1 = acid
				acidTime = acidTime + FST.commonScripts.findMatch(changeTimes[0].value, acid, 'group', 'value', 'default')
			if line == 2 and lastAcid2 != acid:					
				acidChanges2 = acidChanges2 + 1
				lastAcid2 = acid	
				acidTime = acidTime + FST.commonScripts.findMatch(changeTimes[0].value, acid, 'group', 'value', 'default')			

	if acidTime > groupTime:
		changeTime = float(acidTime)
	else:
		changeTime = float(groupTime)
	changeTime = changeTime/60
	hoursFromNowDiv = float(hoursFromNow) + changeTime
#	print acidTime
#	print changeTime
#	print groupTime
#	print hoursFromNowDiv
	data = dataOriginal #rewrite the original set to the data dataset		
	print str(tablecount1) + " Line 1 events count new"
	print str(tablecount2) + " Line 2 events count new"
	tablesperhour1 = tablecount1 / hoursFromNow
	tablesperhour2 = tablecount2 / hoursFromNow
	#print str(tablesperhour1) + " Line 1 Tables per hour new"
	#print str(tablesperhour2) + " Line 2 Tables per hour new" 
	#print str(groupChanges1) + " Line 1 GroupChanges new"
#	print str(groupChanges2) + " Line 2 GroupChanges new"  
	
	#run scores for current data already on the schedule
	tablecount1c = 0.0 	#c suffix is for 'current'
	tablecount2c = 0.0
	tablesperhour1c = 0.0
	tablesperhour2c = 0.0
	acidChanges1c = 0.0
	acidChanges2c = 0.0
	groupChanges1c = 0.0
	groupChanges2c = 0.0
	lastGroup1c = ""
	lastGroup2c = ""
	lastAcid1c = ""
	lastAcid2c = ""
	#dataCurrent = system.db.runNamedQuery("FormationScheduling/currentScheduleWithDetails", {})
	dataCurrent = dataQueryNew
	nameEndTime2 = "EndDate"
	nameLine2 = "ItemID"	
	nameGroup2 ="Group"	
	nameAcid2 = "RefillAcid"
	tableSeparation = lineMax1 # when it goes from Line 1 to Line 2
	for row in range(dataCurrent.getRowCount()):  
		if dataCurrent.getValueAt(row,nameLine2) > tableSeparation: 	#side mapping
			line = 2	
		else:	
			line = 1
		
		endTime = dataCurrent.getValueAt(row,nameEndTime2)	
		startTimeComparison = timeFromNowStartOffset #start time comparison
		endTimeComparison = timeFromNowEnd #end time comparison
		#print "startTimeComparison = " + str(startTimeComparison) + " endTime = " + str(endTime)+ " endTimeComparison =" + str(endTimeComparison)
		if endTime > startTimeComparison and endTime < endTimeComparison: 		#only consider if endtime is in between start and end times
			if line == 1: tablecount1c += 1  #calc tablecounts by side
			if line == 2: tablecount2c += 1
				
	print str(tablecount1c) + " Line 1 events count current"
	print str(tablecount2c) + " Line 2 events count current"
	tablesperhour1c = tablecount1c / hoursFromNowDiv
	tablesperhour2c = tablecount2c / hoursFromNowDiv
#	print str(tablesperhour1c) + " Line 1 Tables per hour current"
#	print str(tablesperhour2c) + " Line 2 Tables per hour current" 

	
	tagTables = system.tag.readBlocking(["[default]Formation/Tables/Schedule/AutoSched/max/tablesPerHour1","[default]Formation/Tables/Schedule/AutoSched/max/tablesPerHour2"]) #read max values saved
	tablesPerHourSumSaved = round(tagTables[0].value + tagTables[1].value,1)
	writeVals = []
	writeVals.append(tablesperhour1+tablesperhour1c)
	writeVals.append(tablesperhour2+tablesperhour2c)
	writeVals.append(tablecount1+tablecount1c)
	writeVals.append(tablecount2+tablecount2c)
	writeVals.append(acidChanges1)
	writeVals.append(acidChanges2)
	writeVals.append(groupChanges1)
	writeVals.append(groupChanges2)


	if testConfig == 0:
		system.tag.writeBlocking(groupPaths, writeVals)
	else:
		system.tag.writeBlocking(testPaths, writeVals)
	#write top performing order
	#print str(changeTime)
	tablesPerHourSum = round(tablesperhour1+tablesperhour1c + tablesperhour2+tablesperhour2c,1)
	print "tablesPerHourSumSaved" + str(tablesPerHourSumSaved) +" tablesPerHourSum = " + str(tablesPerHourSum) 
	print "Saved - New = " + str(tablesPerHourSumSaved - tablesPerHourSum)
	if tablesPerHourSumSaved - tablesPerHourSum <= 0.1:   #tablesPerHourSum >= tablesPerHourSumSaved:
		#print tablesPerHourSum
		#print data.getRowCount()
		if data.getRowCount()>0:
			if testConfig == 0:
				system.tag.writeBlocking([currentScheduleExcelPath],[data])
				#system.tag.writeBlocking([currentTempPath],[data])
				system.tag.writeBlocking(tagMaxPaths, writeVals)
				print "***Saved this config"
