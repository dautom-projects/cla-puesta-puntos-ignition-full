loadTimesTag = system.tag.readBlocking(["[default]Formation/Config/loadTime"])
lineMin1, lineMax1, lineMin2, lineMax2 = FST.namedQueries.getLineLimits()

def tablesUpdate():
	#try:
	timerStart = system.date.now()
	tagProgress = system.tag.read("[default]Formation/Tables/Schedule/inProgress")
	#tagProgress = system.tag.read("[default]Formation/Tables/Schedule/sendingToSchedule")
	tablesPath = "[default]Formation/Config/Tables/tableRanges"
	if not tagProgress.value:
		tablesRangesTag = system.tag.readBlocking([tablesPath])
		tablesRanges = tablesRangesTag[0].value
		failures1 = []
		failures2 = []
		if tablesRanges.getRowCount()>0:
			for row in range(tablesRanges.getRowCount()):
				x = tablesRanges.getValueAt(row,0)
				table = x
				print table
				updateTry = 0
				success = FST.tableUpdate.singleUpdate(table)
				if not success:
					failures1.append(x)
				system.tag.write("[default]Formation/Tables/Schedule/currentTableToUpdate",x)
		if len(failures1)>0:
			print "failures"
			for row in range(tablesRanges.getRowCount()):
				x = tablesRanges.getValueAt(row,0)
				table = x
				updateTry = 0
				success = FST.tableUpdate.singleUpdate(table)
				if not success:
					failures2.append(x)
				system.tag.write("[default]Formation/Tables/Schedule/currentTableToUpdate",x)
	timerEnd = system.date.now()
	timerScript = system.date.millisBetween(timerStart,timerEnd)
	system.tag.write("[default]Formation/Tables/Schedule/udpateTimeExec",timerScript)
		#print "AutoUpdateSchedTime script run time = " + str(timerScript) + " ms. Line " + str(table) + " was updated"
		#return True
	#except:
		#return False
def singleUpdate(table):	
	chargeFaults = [10,33,13]
	#UpdateSQL
	tagPath = "[default]Formation/Tables" + "/" + str(table)
	valPaths = []
	valPaths.append(tagPath + "/batt_rev") #0
	valPaths.append(tagPath + "/timeLeft") #1
	valPaths.append(tagPath + "/table/statusIDRaw") #2
	valPaths.append(tagPath + "/table/statusID") #3
	valPaths.append(tagPath + "/enabledScheduling") #4
	valPaths.append(tagPath + "/group") #5
	valPaths.append(tagPath + "/alarm") #6
	valReads = system.tag.readBlocking(valPaths)
	battery = valReads[0]
	timeLeftRaw = valReads[1]
	status = valReads[2]
	statusAuto = valReads[3].value
		#translate to status color
	if   status.value in chargeFaults and statusAuto == 13: statusColor = 0 #charge fault
	elif statusAuto == 13: statusColor = 7
	elif statusAuto == 4: statusColor = 3 #charging complete
	elif statusAuto == 5: statusColor = 5 #charging
	elif statusAuto == 14: statusColor = 6 #load mode
	elif statusAuto == 2: statusColor = 2 #unload mode
	elif statusAuto == 1: statusColor = 1 #empty
	elif statusAuto == 11: statusColor = 8 #waiting to put on charge
	elif statusAuto == 3: statusColor = 4 #ready to unload
	elif statusAuto == 6: statusColor = 4 #FIFO
	else: statusColor = 999
	if str(timeLeftRaw.quality) == 'Good' and str(status.quality) == "Good":
		timeLeft = timeLeftRaw.value
		enabled = valReads[4].value
	else:
		timeLeft = -999
		enabled = 0
	group = valReads[5]
	alarm = valReads[6]
	currentTime = system.date.now()
	params = {"battery": battery.value, "table": table, "timeLeft":timeLeft, "groupType":group.value, "alarm":alarm.value, "enabled":enabled,"statusColor":statusColor,"statusAuto":statusAuto, "currentTime":currentTime }
	# Run the Named Query
	system.db.runNamedQuery("FormationScheduling/updateScheduleCurrentBatts", params)
	
	##Auto complete logic
	valPaths = []
	valPaths.append(tagPath + "/_datasetRaw") #0
	valPaths.append(tagPath + "/table/autoCompleteScriptLastResults") #1
	valPaths.append(tagPath + "/table/autoCompleteBothSides") #2
	valPaths.append(tagPath + "/table/autoCompleteNext") #3
	scriptPath = tagPath + "/table/autoCompleteScriptRun"
	valPaths.append(scriptPath) #4	
	valReads = system.tag.readBlocking(valPaths)
	datasetRaw = valReads[0].value
	colBatt = datasetRaw.getColumnIndex("Batt_Rev")
	battsUnique = []
	for row in range(datasetRaw.getRowCount()):
		battRev = datasetRaw.getValueAt(row,colBatt)
		try:
			intLen = len(battRev)
			if intLen > 4:
				battRev = battRev[:-2]
		except:
			battRev = ""
		if battRev not in battsUnique:
			battsUnique.append(battRev)
	autoCompBothSides = valReads[2]

	if valReads[4].value == 1:#compare debounce to time when the battery type changed
		if autoCompBothSides.value == 1:
			upcomingData = system.db.runNamedQuery("FormationScheduling/eventOrderAll",{})
		if table < lineMin2:
			params1 = {"minTable": lineMin1,"maxTable": lineMax1}
			upcomingData = system.db.runNamedQuery("FormationScheduling/eventOrderLine1WithLocked", params1)
		else:
			params1 = {"minTable": lineMin2,"maxTable": lineMax2}
			upcomingData = system.db.runNamedQuery("FormationScheduling/eventOrderLine2WithLocked", params1)
				#check each rev in the upcoming list
		colDuf = upcomingData.getColumnIndex("DUFWrev")
		colRow = upcomingData.getColumnIndex("rowID")
		battsUniqueLen = len(battsUnique) #need to check lengths for mixed tables
		matchFound = 0
		matchingRow = 0
		if battsUniqueLen > 0: #Filter out blank batt_revs
			for row in range(upcomingData.getRowCount()):
				revMatch = 0 #default to check if revisions match
				battRev = upcomingData.getValueAt(row,colDuf)
				print "battRev: " + battRev
				for j in battsUnique:
					if j in battRev and len(j)>0:
						revMatch = revMatch + 1
				if revMatch == battsUniqueLen:
					matchFound = 1
					matchingRow = upcomingData.getValueAt(row,colRow) 
					break #matching rev found
			
			logger = system.util.getLogger("myLogger") #troubleshooting only	
			if matchFound == 1:
				#run update script
				autoComplete = valReads[3].value
				if autoComplete == True: #if in Load mode, autocomplete
					eventID = str(matchingRow)
					statusID = 4  #complete statusID
					params = {"eventID": eventID,"statusID": statusID}
					# Run the Named Query
					data = system.db.runNamedQuery("FormationScheduling/updateScheduleStatusSingle", params)
				
					system.tag.write(tagPath + "/table/autoCompleteScriptLastResults",1)
					logger.info("Table " + str(table) + " was AutoCompleted with EventID = " + str(eventID) + ". BattsUniqueDatasetFromDTI = " + str(battsUnique))
				else:
					pass
					logger.info("AutoCompleteScript Skipped Table " + str(table) + "due to table AutoComplete being off")
					
			else:
				system.tag.write(tagPath + "/table/autoCompleteScriptLastResults",0) #make alarm in this tag
				upcomingBattRevs = [] #make a list of upcoming for troubleshooting.
				for row in range(upcomingData.getRowCount()):
					battRev = upcomingData.getValueAt(row,colDuf)
					upcomingBattRevs.append(battRev)
				logger.info("AutoCompleteScript Skipped Table " + str(table) + " due to match not being found. BattsUniqueDatasetFromDTI = " + str(battsUnique) + ". UpcomingListRevs = " + str(upcomingBattRevs))
		system.tag.writeBlocking([scriptPath], [0])			
	system.tag.write(tagPath + "/table/autoCompleteScriptUniqueBattsResult", str(battsUnique))
	params1 = {"table": table}
	data = system.db.runNamedQuery("FormationScheduling/currentScheduleTable", params1)
	
	#schedule auto updating of static event times, when the current events overlap i.e. time updates)
	if data.getRowCount() > 1: 
		for row in range(data.getRowCount()):
			if row == 0:
				currentEndDate = data.getValueAt(0,"EndDate")
				priorEndTime = currentEndDate #used for next row
			else:	
				group = str(data.getValueAt(row,"Group"))
				addTime = FST.commonScripts.findMatch(loadTimesTag[0].value, group, 'group', 'value', 'default')
				startTime = data.getValueAt(row,"StartDate")
				priorTime = system.date.minutesBetween(priorEndTime,startTime) #calc prior time spacing between events
				if priorTime < addTime: 
					newStartDate = system.date.addMinutes(currentEndDate,addTime)
				elif currentEndDate > startTime:
					newStartDate = system.date.addMinutes(currentEndDate,addTime)
				else:
					newStartDate = startTime #system.date.addMinutes(startTime,timeOffset)
				
				timeLength = abs( system.date.minutesBetween ( data.getValueAt(row,"EndDate"),startTime) )
				newEndDate = system.date.addMinutes(newStartDate,timeLength)
				rowID = data.getValueAt(row,"rowID")
				params = {"rowID": rowID,"startDate": newStartDate, "endDate": newEndDate}
				system.db.runNamedQuery("FormationScheduling/updateScheduleTime",params)
				priorEndTime = data.getValueAt(row,"EndDate") #used for next row
				currentEndDate = newEndDate		
	return True
	#except:
		#return False
