#* DAUTOM SAS CONFIDENTIAL
#*_________________________
#*
#* [2013] - [2025] DAUTOM SAS
#* All Rights Reserved.
#*
#* NOTICE: All information contained herein is, and remains the property
#* of DAUTOM SAS and its suppliers, if any. The intellectual and 
#* technical concepts contained here in are proprietary to DAUTOM SAS
#* and its suppliers and may be covered by U.S and Foreign Patents, 
#* patents in process, and are protected by trade secret or copyright law. 
#* Dissemination of this information or reproduction of this material
#* is strictly forbidden unless prior written permission is obtained
#* from DAUTOM SAS.

'''


'''
import inspect 

#db variable

db = 'mes_core'

#call our log for calc

mes_core.logging.log('Dautom','MES Core:Calculating OEE','info')


def formatDateTime(dateTime):
	Year = system.date.getYear(dateTime)
	Month = system.date.getMonth(dateTime)
	Day = system.date.getDayOfMonth(dateTime)
	Hour = system.date.getHour24(dateTime)
	Min = system.date.getMinute(dateTime)
	Sec = system.date.getSecond(dateTime)
	
	dateTimeFormated = "{}-{}-{} {}:{}:{}".format(Year, Month + 1, Day, Hour, Min, Sec)
	return dateTimeFormated
	
def calcQuality(totalCountPath,goodCountPath,oeeQualityPath):
	print 'for calcQuality()'
	print locals().keys()
	print 'totalCountPath: ' + totalCountPath
	print 'goodCountPath: ' + goodCountPath
	print 'oeeQualityPath: ' + oeeQualityPath
	
	totalCount = system.tag.readBlocking(totalCountPath)[0].value
	goodCount = system.tag.readBlocking(goodCountPath)[0].value
	
	try:
		quality = float(goodCount)/float(totalCount)
		
	except:
		quality = 1
		
	system.tag.writeBlocking([oeeQualityPath], [quality])
	
	print 'Quality: ' + str(quality)
	print ''
	return quality
	
def calcAvailability(runTimePath,schTimePath,oeeAvailabilityPath):
	print 'for calcAvailability()'
	print locals().keys()
	print 'runTimePath: ' + runTimePath
	print 'totalTimePath: ' + schTimePath
	print 'oeeAvailabilityPath: ' + oeeAvailabilityPath
	
	runTime =  system.tag.readBlocking(runTimePath)[0].value
	schTime = system.tag.readBlocking(schTimePath)[0].value
	
	
	print runTime , schTime
	try:
		availability = float(runTime)/float(schTime)
	except:
		availability = 1
	
	system.tag.writeBlocking([oeeAvailabilityPath], [availability])
	print 'Availability: ' + str(availability)
	print ''
	return availability
	
def calcPerformance(totalCountPath,targetCountPath,oeePerformancePath):
	print 'for calcPerformance()'
	print locals().keys()
	print 'totalCountPath: ' + totalCountPath
	print 'targetCountPath: ' + targetCountPath
	print 'oeePerformancePath: ' + oeePerformancePath
	
	totalCount = system.tag.readBlocking(totalCountPath)[0].value
	targetCount = system.tag.readBlocking(targetCountPath)[0].value
	print totalCount, targetCount
	
	try:
		performance = float(totalCount)/float(targetCount)
	except:
		performance = 1
	
	system.tag.writeBlocking([oeePerformancePath], [performance])
	print 'Performance: ' + str(performance)
	print ''
	return performance
	
def getTagIDs(db,nodeID):
	print 'for getTagIDs()'
	print locals().keys()
	print 'NodeID: ' + str(nodeID)
	print 'db: ' + db
	
	listOfTags = []
	id = system.tag.readBlocking(nodeID)[0].value
	
	query = 'select ID from counttag where NodeID = ?'
	data = system.db.runPrepQuery(query, [id], db)
	mes_core.misc.printDatasetresultado(data)
	
	for row in data:
		tagID = row[0]
		listOfTags.append(tagID)
	
	print 'List of Tags: ' + str(listOfTags)
	print ''
	return listOfTags

def getGoodCount(goodCountPath, startTimePath, endTimePath, tagID, countTypeID, badCount,db=db):
	print 'for getGoodCount()'
	print locals().keys()
	print 'goodCountPath: ' + goodCountPath
	print 'startTimePath: ' + startTimePath
	print 'endTimePath: ' + endTimePath
	print 'tagID: ' + str(tagID)
	print 'countTypeID: ' + str(countTypeID)
	print 'db: ' + db
	
	#original query
	#query = '''
	#	select sum(Count) from counthistory
	#	where TagID = ? and
	#	CountTypeID = ? and 
	#	`TimeStamp` between ? and ?
	#'''
	
	# SQL Server compatible query
	query = '''
		SELECT SUM(ch.Count)
		FROM counthistory ch
		JOIN counttag ct ON ch.TagID = ct.ID
		WHERE ch.TagID = ?
		AND ct.CountTypeID = ?
		AND ch.TimeStamp BETWEEN ? AND ?
	'''
	
	startTime = system.tag.readBlocking(startTimePath)[0].value
	startTimeFormated = formatDateTime(startTime)	
	endTime = system.tag.readBlocking(endTimePath)[0].value
	endTimeFormated = formatDateTime(endTime)
	
	#original
	data = system.db.runPrepQuery(query,[tagID,countTypeID,startTimeFormated,endTimeFormated], db)
	mes_core.misc.printDatasetresultado(data)

		
	goodCount = 'None'
	
	for row in data:
		goodCount = row[0]
	if goodCount == None:
		goodCount = 0
		
	else:
		pass
	#system.tag.writeBlocking([goodCountPath], [goodCount])
	system.tag.writeBlocking([goodCountPath], [goodCount - badCount])
	print 'GoodCount: ' + str(goodCount)
	print ''
	return goodCount
	
	
def getBadCount(badCountPath,startTimePath,endTimePath,tagID,countTypeID,db=db):
	print 'for getBadCount()'
	print locals().keys()
	print 'badCountPath: ' + badCountPath
	print 'startTimePath: ' + startTimePath
	print 'endTimePath: ' + endTimePath
	print 'tagID: ' + str(tagID)
	print 'countTypeID: ' + str(countTypeID)
	print 'db: ' + db
	
	#original query
	"""
	query = '''
		Select sum(Count) from counthistory
		where TagID = ? and
		CountTypeID = ? and
		`TimeStamp` between ? and ?
	'''
	"""
	# SQL Server compatible query
	query = '''
		SELECT SUM(ch.Count)
		FROM counthistory ch
		JOIN counttag ct ON ch.TagID = ct.ID
		WHERE ch.TagID = ?
		AND ct.CountTypeID = ?
		AND ch.TimeStamp BETWEEN ? AND ?
	'''
	
	startTime = system.tag.readBlocking(startTimePath)[0].value
	startTimeFormated = formatDateTime(startTime)
	endTime = system.tag.readBlocking(endTimePath)[0].value
	endTimeFormated = formatDateTime(endTime)
	
	#original
	data = system.db.runPrepQuery(query,[tagID,countTypeID,startTimeFormated,endTimeFormated],db)
	mes_core.misc.printDatasetresultado(data)
	#test
#	data = system.db.runPrepQuery(query,[tagID,countTypeID],db)
	
	badCount = 'None'
	for row in data:
		badCount = row[0]
	if badCount == None:
		badCount = 0
	else:
		pass

	system.tag.writeBlocking([badCountPath], [badCount])
	
	print 'Bad Count: ' + str(badCount)	
	print ''
	return badCount	
	

def getTotalCount(db,nodeID,totalCountPath,startTimePath,endTimePath):
	print 'For getTotalCount()'
	print locals().keys()
	print 'db: ' + db
	print 'nodeID: ' + nodeID
	print 'totalCountPath: ' + totalCountPath
	print 'startTimePath: ' + startTimePath
	print 'endTimePath: ' + endTimePath

	tagIDs = getTagIDs(db,nodeID)
	tagIDs = str(tagIDs).replace('[','(')
	tagIDs = str(tagIDs).replace(']',')')
	tagIDs = tagIDs.replace(' ','')
	
	#original query
	#query = '''SELECT sum(Count) FROM counthistory
	#		where countTypeID != 2 and
	#		`TimeStamp` between ? and ? and (TagID in %s)'''% tagIDs
		
	# SQL Server compatible query
	query = '''
		SELECT SUM(h.Count)
		FROM counthistory h
		JOIN counttag t ON h.TagID = t.ID
		--WHERE t.CountTypeID != 1
		WHERE t.CountTypeID NOT IN (2,3)
		AND h.TimeStamp BETWEEN ? AND ?
		AND h.TagID IN %s
	''' % tagIDs
			
	startTime = system.tag.readBlocking(startTimePath)[0].value
	startTimeFormated = formatDateTime(startTime)
	endTime = system.tag.readBlocking(endTimePath)[0].value
	endTimeFormated = formatDateTime(endTime)
	
	#original
	data = system.db.runPrepQuery(query,[startTimeFormated,endTimeFormated],db)
	mes_core.misc.printDatasetresultado(data)
	
	totalCount = 'None'
	for row in data:
		totalCount = row[0]
	if totalCount == None:
		totalCount = 0
	else:
		pass
	
	system.tag.writeBlocking([totalCountPath],[totalCount])
	print 'Total Count: ' + str(totalCount)
	print ''
	return totalCount

def getUnplannedDowntimeSeconds(db,startTimePath,unplannedDowntimePath,nodeID):
	print 'for getUnplannedDowntimeSeconds()'
	print locals().keys()
	print 'db: ' + db
	print 'startTimePath: ' + startTimePath
	print 'unPlannedDowntimePath: ' + unplannedDowntimePath
	print 'NodeID: ' + nodeID
	
	startTime = system.tag.readBlocking(startTimePath)[0].value
	startTimeFormated = formatDateTime(startTime)
	print startTimeFormated
	
	id = system.tag.readBlocking(nodeID)[0].value
	
	#original query
	#query = '''SELECT  SUM(TIME_TO_SEC(TIMEDIFF(s.EndDateTime,s.StartDateTime))) as 'Total in Seconds' from statehistory s
	#		left join statereason st
	#		on s.StateReasonID = st.ID
	#		where st.RecordDowntime = 1
	#		and s.LineID = ?
	#		and StartDateTime > ?
	#		and (EndDateTime <= CURRENT_TIMESTAMP() or EndDateTime is NULL)'''
	
	# SQL Server compatible query
	
	query = '''SELECT SUM(DATEDIFF(SECOND, s.StartDateTime, s.EndDateTime)) AS [Total in Seconds]
			FROM statehistory s
			LEFT JOIN statereason st ON s.StateReasonID = st.ID
			WHERE st.RecordDowntime = 1
			AND s.NodeID = ?
			AND s.StartDateTime > ?
			AND (s.EndDateTime <= CURRENT_TIMESTAMP OR s.EndDateTime IS NULL)'''


	data = system.db.runPrepQuery(query,[id,startTimeFormated],db)
	mes_core.misc.printDatasetresultado(data)
	
	for row in data:
		unplannedDowntime = row[0]
		
		if unplannedDowntime == None:
			system.tag.writeBlocking([unplannedDowntimePath],[0])
		else:
			system.tag.writeBlocking([unplannedDowntimePath],[unplannedDowntime])
	
	print 'Unplanned Downtime: ' + str(unplannedDowntime)
	print ''		
	return unplannedDowntime

def getPlannedDowntimeSeconds(db,startTimePath,plannedDowntimePath,nodeID):
	print 'for getPlannedDowntimeSeconds()'
	print locals().keys()
	print 'db: ' + db
	print 'startTimePath: ' + startTimePath
	print 'plannedDowntimePath: ' + plannedDowntimePath
	print 'NodeID: ' + nodeID
	
	startTime = system.tag.readBlocking(startTimePath)[0].value
	startTimeFormated = formatDateTime(startTime)
	id = system.tag.readBlocking(nodeID)[0].value
	
	#original query
	#query = '''SELECT  SUM(TIME_TO_SEC(TIMEDIFF(s.EndDateTime,s.StartDateTime))) as 'Total in Seconds' from statehistory s
	#		left join statereason st
	#		on s.StateReasonID = st.ID
	#		where st.PlannedDowntime = 1
	#		and s.LineID = ?
	#		and StartDateTime > ?
	#		and (EndDateTime <= CURRENT_TIMESTAMP() or EndDateTime is NULL)'''
	
	# SQL Server compatible query
	query = '''SELECT SUM(DATEDIFF(SECOND, s.StartDateTime, s.EndDateTime)) AS [Total in Seconds]
			FROM statehistory s
			LEFT JOIN statereason st ON s.StateReasonID = st.ID
			WHERE st.PlannedDowntime = 1
			AND s.NodeID = ?
			AND s.StartDateTime > ?
			AND (s.EndDateTime <= CURRENT_TIMESTAMP OR s.EndDateTime IS NULL)'''

	#fecha formateada a str
	data = system.db.runPrepQuery(query,[id,startTimeFormated],db)
	mes_core.misc.printDatasetresultado(data)
	
	for row in data:
		plannedDowntime = row[0]
		
		if plannedDowntime == None:
			system.tag.writeBlocking([plannedDowntimePath],[0])
		else:
			system.tag.writeBlocking([plannedDowntimePath],[plannedDowntime])
			
	print 'Planned Downtime: ' + str(plannedDowntime)
	print ''
	return plannedDowntime

'''getOEE calls all of the functions that calculates then writes the updated values to our tags.  this is our parent function.  This parent function will change and can be 
used to build reports for shift, run or daily OEE
'''

def getOee(parentPath): #parentPath is the same as linePath and gets us all the way up to /Line
	print 'Starting getOee() for ' + parentPath
	print locals().keys()
	print ''
	
	#declare all of the tags to write to--these will be declared in the script
	nodeID = parentPath +'/OEE/ID'
	unplannedDowntimePath = parentPath + '/OEE/Unplanned Downtime'
	totalTimePath = parentPath + '/OEE/Total Time'
	schTimePath = parentPath + '/OEE/Schedule Time'
	totalCountPath = parentPath + '/OEE/Total Count'
	targetCountPath = parentPath + '/OEE/Target Count'
	startTimePath = parentPath + '/OEE/Start Time'
	standardRatePath = parentPath + '/OEE/Standard Rate'
	scheduleRatePath = parentPath + '/OEE/Schedule Rate'
	runTimePath = parentPath + '/OEE/Run Time'
	plannedDowntimePath = parentPath + '/OEE/Planned Downtime'
	oeeQualityPath = parentPath + '/OEE/OEE Quality'
	oeePerformancePath = parentPath + '/OEE/OEE Performance'
	oeeAvailabilityPath = parentPath + '/OEE/OEE Availability'
	goodCountPath = parentPath + '/OEE/Good Count'
	currentTimePath = parentPath + '/OEE/Current Time'
	badCountPath = parentPath + '/OEE/Bad Count'
	runIDPath = parentPath + '/OEE/RunID' #runID is not used yet... and this may be moved to a separate function called getRunOee(parentPath,runID)
	goodCountIDPath = parentPath + '/Dispatch/OEE Outfeed/TagID'
	badCountIDPath = parentPath + '/Dispatch/OEE Waste/TagID'
	endTimePath = currentTimePath
	
	goodCountID = system.tag.readBlocking(goodCountIDPath)[0].value
	badCountID = system.tag.readBlocking(badCountIDPath)[0].value
	
	# call all of our functions, in order, to run our calculations and then update all of the tags in OEE udt (from the parentPath argument)
	getUnplannedDowntimeSeconds(db,startTimePath,unplannedDowntimePath,nodeID)
	getPlannedDowntimeSeconds(db,startTimePath,plannedDowntimePath,nodeID)
	badCount = getBadCount(badCountPath,startTimePath,endTimePath,badCountID,3,db) #this has hard-coded values
	getGoodCount(goodCountPath,startTimePath,endTimePath,goodCountID,2,badCount,db)#this has hard-coded values
	getTotalCount(db,nodeID,totalCountPath,startTimePath,endTimePath)
	calcQuality(totalCountPath,goodCountPath,oeeQualityPath)
	calcAvailability(runTimePath,schTimePath,oeeAvailabilityPath)
	#calcAvailability(runTimePath,totalTimePath,oeeAvailabilityPath)
	calcPerformance(totalCountPath,targetCountPath,oeePerformancePath)
	
	print 'Completed getOee() for ' + parentPath
	
def getOeeActHr(parentPath): #parentPath is the same as linePath and gets us all the way up to /Line
	print 'Starting getOeeActHr() for ' + parentPath
	print locals().keys()
	print ''
	
	#declare all of the tags to write to--these will be declared in the script
	nodeID = parentPath +'/OEE Actual Hr/ID'
	unplannedDowntimePath = parentPath + '/OEE Actual Hr/Unplanned Downtime'
	totalTimePath = parentPath + '/OEE Actual Hr/Total Time'
	totalCountPath = parentPath + '/OEE Actual Hr/Total Count'
	targetCountPath = parentPath + '/OEE Actual Hr/Target Count'
	startTimePath = parentPath + '/OEE Actual Hr/Start Time'
	standardRatePath = parentPath + '/OEE Actual Hr/Standard Rate'
	scheduleRatePath = parentPath + '/OEE Actual Hr/Schedule Rate'
	runTimePath = parentPath + '/OEE Actual Hr/Run Time'
	plannedDowntimePath = parentPath + '/OEE Actual Hr/Planned Downtime'
	oeeQualityPath = parentPath + '/OEE Actual Hr/OEE Quality'
	oeePerformancePath = parentPath + '/OEE Actual Hr/OEE Performance'
	oeeAvailabilityPath = parentPath + '/OEE Actual Hr/OEE Availability'
	goodCountPath = parentPath + '/OEE Actual Hr/Good Count'
	currentTimePath = parentPath + '/OEE Actual Hr/Current Time'
	badCountPath = parentPath + '/OEE Actual Hr/Bad Count'
	runIDPath = parentPath + '/OEE Actual Hr/RunID' #runID is not used yet... and this may be moved to a separate function called getRunOee(parentPath,runID)
	goodCountIDPath = parentPath + '/Dispatch/OEE Outfeed/TagID'
	badCountIDPath = parentPath + '/Dispatch/OEE Waste/TagID'
	endTimePath = currentTimePath
	
	goodCountID = system.tag.readBlocking(goodCountIDPath)[0].value
	badCountID = system.tag.readBlocking(badCountIDPath)[0].value
	
	# call all of our functions, in order, to run our calculations and then update all of the tags in OEE udt (from the parentPath argument)
	getUnplannedDowntimeSeconds(db,startTimePath,unplannedDowntimePath,nodeID)
	getPlannedDowntimeSeconds(db,startTimePath,plannedDowntimePath,nodeID)
	badCount = getBadCount(badCountPath,startTimePath,endTimePath,badCountID,3,db) #this has hard-coded values
	getGoodCount(goodCountPath,startTimePath,endTimePath,goodCountID,2, badCount)#this has hard-coded values

	getTotalCount(db,nodeID,totalCountPath,startTimePath,endTimePath)
	calcQuality(totalCountPath,goodCountPath,oeeQualityPath)
	calcAvailability(runTimePath,totalTimePath,oeeAvailabilityPath)
	calcPerformance(totalCountPath,targetCountPath,oeePerformancePath)
	
	print 'Completed getOeeActHr() for ' + parentPath
	
def getOeeActShf(parentPath): #parentPath is the same as linePath and gets us all the way up to /Line
	print 'Starting getOeeActShf() for ' + parentPath
	print locals().keys()
	print ''
	
	#declare all of the tags to write to--these will be declared in the script
	nodeID = parentPath +'/OEE Actual Shf/ID'
	unplannedDowntimePath = parentPath + '/OEE Actual Shf/Unplanned Downtime'
	totalTimePath = parentPath + '/OEE Actual Shf/Total Time'
	totalCountPath = parentPath + '/OEE Actual Shf/Total Count'
	targetCountPath = parentPath + '/OEE Actual Shf/Target Count'
	startTimePath = parentPath + '/OEE Actual Shf/Start Time'
	standardRatePath = parentPath + '/OEE Actual Shf/Standard Rate'
	scheduleRatePath = parentPath + '/OEE Actual Shf/Schedule Rate'
	runTimePath = parentPath + '/OEE Actual Shf/Run Time'
	plannedDowntimePath = parentPath + '/OEE Actual Shf/Planned Downtime'
	oeeQualityPath = parentPath + '/OEE Actual Shf/OEE Quality'
	oeePerformancePath = parentPath + '/OEE Actual Shf/OEE Performance'
	oeeAvailabilityPath = parentPath + '/OEE Actual Shf/OEE Availability'
	goodCountPath = parentPath + '/OEE Actual Shf/Good Count'
	currentTimePath = parentPath + '/OEE Actual Shf/Current Time'
	badCountPath = parentPath + '/OEE Actual Shf/Bad Count'
	runIDPath = parentPath + '/OEE Actual Shf/RunID' #runID is not used yet... and this may be moved to a separate function called getRunOee(parentPath,runID)
	goodCountIDPath = parentPath + '/Dispatch/OEE Outfeed/TagID'
	badCountIDPath = parentPath + '/Dispatch/OEE Waste/TagID'
	endTimePath = currentTimePath
	
	goodCountID = system.tag.readBlocking(goodCountIDPath)[0].value
	badCountID = system.tag.readBlocking(badCountIDPath)[0].value
	
	# call all of our functions, in order, to run our calculations and then update all of the tags in OEE udt (from the parentPath argument)
	getUnplannedDowntimeSeconds(db,startTimePath,unplannedDowntimePath,nodeID)
	getPlannedDowntimeSeconds(db,startTimePath,plannedDowntimePath,nodeID)
	getGoodCount(goodCountPath,startTimePath,endTimePath,goodCountID,2)#this has hard-coded values
	getBadCount(badCountPath,startTimePath,endTimePath,badCountID,3,db) #this has hard-coded values
	getTotalCount(db,nodeID,totalCountPath,startTimePath,endTimePath)
	calcQuality(totalCountPath,goodCountPath,oeeQualityPath)
	calcAvailability(runTimePath,totalTimePath,oeeAvailabilityPath)
	calcPerformance(totalCountPath,targetCountPath,oeePerformancePath)
	
	print 'Completed getOeeActShf() for ' + parentPath
	
def getOeeActDay(parentPath): #parentPath is the same as linePath and gets us all the way up to /Line
	print 'Starting getOeeActDay() for ' + parentPath
	print locals().keys()
	print ''
	
	#declare all of the tags to write to--these will be declared in the script
	nodeID = parentPath +'/OEE Actual Day/ID'
	unplannedDowntimePath = parentPath + '/OEE Actual Day/Unplanned Downtime'
	totalTimePath = parentPath + '/OEE Actual Day/Total Time'
	totalCountPath = parentPath + '/OEE Actual Day/Total Count'
	targetCountPath = parentPath + '/OEE Actual Day/Target Count'
	startTimePath = parentPath + '/OEE Actual Day/Start Time'
	standardRatePath = parentPath + '/OEE Actual Day/Standard Rate'
	scheduleRatePath = parentPath + '/OEE Actual Day/Schedule Rate'
	runTimePath = parentPath + '/OEE Actual Day/Run Time'
	plannedDowntimePath = parentPath + '/OEE Actual Day/Planned Downtime'
	oeeQualityPath = parentPath + '/OEE Actual Day/OEE Quality'
	oeePerformancePath = parentPath + '/OEE Actual Day/OEE Performance'
	oeeAvailabilityPath = parentPath + '/OEE Actual Day/OEE Availability'
	goodCountPath = parentPath + '/OEE Actual Day/Good Count'
	currentTimePath = parentPath + '/OEE Actual Day/Current Time'
	badCountPath = parentPath + '/OEE Actual Day/Bad Count'
	runIDPath = parentPath + '/OEE Actual Day/RunID' #runID is not used yet... and this may be moved to a separate function called getRunOee(parentPath,runID)
	goodCountIDPath = parentPath + '/Dispatch/OEE Outfeed/TagID'
	badCountIDPath = parentPath + '/Dispatch/OEE Waste/TagID'
	endTimePath = currentTimePath
	
	goodCountID = system.tag.readBlocking(goodCountIDPath)[0].value
	badCountID = system.tag.readBlocking(badCountIDPath)[0].value
	
	# call all of our functions, in order, to run our calculations and then update all of the tags in OEE udt (from the parentPath argument)
	getUnplannedDowntimeSeconds(db,startTimePath,unplannedDowntimePath,nodeID)
	getPlannedDowntimeSeconds(db,startTimePath,plannedDowntimePath,nodeID)
	getGoodCount(goodCountPath,startTimePath,endTimePath,goodCountID,2)#this has hard-coded values
	getBadCount(badCountPath,startTimePath,endTimePath,badCountID,3,db) #this has hard-coded values
	getTotalCount(db,nodeID,totalCountPath,startTimePath,endTimePath)
	calcQuality(totalCountPath,goodCountPath,oeeQualityPath)
	calcAvailability(runTimePath,totalTimePath,oeeAvailabilityPath)
	calcPerformance(totalCountPath,targetCountPath,oeePerformancePath)
	
	print 'Completed getOeeActDay() for ' + parentPath

#test on script console
#parentPath = "[UNS]Clarios/Pacifico/Cubiertas/IMM 15/Line"	
#getOee(parentPath)