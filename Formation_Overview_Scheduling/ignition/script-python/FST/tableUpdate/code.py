def tableUpdate(table):
	try:	
		params1 = {"table": table}
		projectName = shared.constants.PROJECT_NAME
		data = system.db.runNamedQuery(projectName,"FormationScheduling/currentScheduleTable", params1)
		if data.getRowCount() > 1: 
			for row in range(data.getRowCount()):
				if row == 0:
					currentEndDate = data.getValueAt(0,"EndDate")
					priorEndTime = currentEndDate #used for next row
				else:	
					group = str(data.getValueAt(row,"Group"))
					loadTimesTag = system.tag.readBlocking(["[default]Formation/Config/loadTime"])
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
					system.db.runNamedQuery(projectName,"FormationScheduling/updateScheduleTime",params)
					priorEndTime = data.getValueAt(row,"EndDate") #used for next row
					currentEndDate = newEndDate
			#UpdateSQL
		tagPath = shared.constants.DATA_PATH + "/" + str(table)	
		battery = system.tag.read(tagPath + "/batt_rev")
		timeLeftRaw = system.tag.read(tagPath + "/timeLeft")
		if str(timeLeftRaw.quality) == 'Good' and str(statusTag.quality) == "Good":
			timeLeft = timeLeftRaw.value
			enabledRaw = system.tag.read(tagPath = "/enabledScheduling")
			enabled = enabledRaw.value
		else:
			timeLeft = -999
			enabled = 0
		group = system.tag.read(tagPath+"/group")
		alarm = system.tag.read(tagPath+"/alarm")
		currentTime = system.date.now()
		params = {"battery": battery.value, "table": table.value, "timeLeft":timeLeft, "groupType":group.value, "alarm":alarm.value, "enabled":enabled,"statusColor":statusColor,"statusAuto":statusAuto, "currentTime":currentTime }
		# Run the Named Query
		system.db.runNamedQuery("Formation_Overview_Scheduling","FormationScheduling/updateScheduleCurrentBatts", params)
		return True
	except:
		return False
		pass
