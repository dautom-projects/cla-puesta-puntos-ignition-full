lineRangePaths = []
lineRangePaths.append("[default]Formation/Config/Tables/lineTableMin1")
lineRangePaths.append("[default]Formation/Config/Tables/lineTableMax1")
lineRangePaths.append("[default]Formation/Config/Tables/lineTableMin2")
lineRangePaths.append("[default]Formation/Config/Tables/lineTableMax2")
lineRanges = system.tag.readBlocking(lineRangePaths)
LINE_MIN_TABLE_1 = lineRanges[0].value
LINE_MAX_TABLE_1 = lineRanges[1].value
LINE_MIN_TABLE_2 = lineRanges[2].value
LINE_MAX_TABLE_2 = lineRanges[3].value
#Source Path comes from constants; could be different across plants
SOURCE_PATH = "Formation/Tables"
lineNamesPath = ["[default]Formation/Config/lineName1","[default]Formation/Config/lineName2"]
lineNames = system.tag.readBlocking(lineNamesPath)
LINE_NAME_1 = lineNames[0].value
LINE_NAME_2 = lineNames[1].value
DATA_PATH = "[default]Formation/Tables"
InitConst1 = "[default]Formation/Lockup Tool/LoadTableTime"
InitConst2 = "[default]Formation/Lockup Tool/NormalTableTime"
CALC_FOLDER = "[default]Formation/Lockup Tool/Line "
EMPTY_STATES = ['0','1','11', '999']
PROJECT_NAME = "Formation_Overview_Scheduling"

def triggerUpdate():
	try:
		getCurrentData(1)
		if(LINE_MAX_TABLE_2>LINE_MIN_TABLE_2):
			getCurrentData(2)
		path = "[default]Formation/Lockup Tool/SuccessCount"
		tag = system.tag.readBlocking([path])
		if tag[0].value < 10000:
			tagVal = tag[0].value + 1
		else:
			tagVal = 0
		system.tag.writeBlocking([path], [tagVal])
		return True
	except:
		pass

def browseTags(path, filter):
		"""
		Recursively browses a path for tags based on a filter
		
		Args:
			path: A valid path string to browse
			filter: A dictionary of filter items. See the valid filter keys in the help documentation at docs.inductiveautomation.com
			
		Returns:
			filteredTagPaths: A list containing all the tag paths matching the filter
		"""
		
		tagPaths = []
		
		# Function which browses tags recursively
		def browseTags(path, filter):
				
			# Call this function again at the current path, but apply the filter.
			results = system.tag.browse(path, filter)
			for result in results.getResults():
				#Here's where you'd want to do something more useful. For now, we print.
				#print result ('fullPath')
				tagPaths.append(str(result['fullPath']))
			
			return tagPaths
			
		# Call the browseTags function, filtered by "filter"
		filteredTagPaths = browseTags(path, filter)
		return filteredTagPaths
		
def getTableTags(LineNumber=1):
			"""
			Browses the table data folder (SOURCE_PATH, defined at top) and returns a list of
			dictionaries containing table data information.
			
			Args:
				Line Number (integer): Specify line 1 or line 2 to filter
				
			Returns:
				tagPaths (list): List of tags that meet line criteria
			"""
			if LineNumber == 1:
				filterSide = LINE_NAME_1
			elif LineNumber == 2:
				filterSide = LINE_NAME_2

			filter = {"tagType": "UdtInstance", "typeId": "Table"}
			udtTags = browseTags(SOURCE_PATH, filter)
			
			tagPaths = []
				
			for udt in udtTags:
				tag = system.tag.readBlocking([udt + "/Parameters.Side"])
				if tag[0].value is not None:
					if len(tag[0].value)>0:
						if tag[0].value == filterSide:
							tagPaths.append(udt)
					elif LineNumber==2:
						tagPaths.append(udt)
				elif LineNumber==2:
					tagPaths.append(udt)
			return tagPaths
def getTableTagPaths(LineNumber):
	
	tagPaths = []
	parentPath = DATA_PATH+'/'
	if LineNumber == 1:
		minTable = LINE_MIN_TABLE_1
		maxTable = LINE_MAX_TABLE_1+1
	else:
		minTable = LINE_MIN_TABLE_2
		maxTable = LINE_MAX_TABLE_2+1
	
	for x in range(minTable, maxTable):
		tagPaths.append(parentPath+str(x))
	return tagPaths
	
def getCurrentData(LineNumber):
	"""
	Browses the table data folder and returns relevant table data for the chosen line
	
	Args:
		Line Number (integer): Specify line 1 or line 2 to filter
		
	Returns:
		secondSortDS (dataset): dataset with table, time open, time left, calc time, and alarm
	"""
	dsHeaders = ['Table','TimeOpen','TimeLeft','CalcTime','State','Empty']
	headers = ['Table','TimeOpen','TimeLeft','CalcTime','Alarm']
	
	# Get table tags for chosen side
	valSide= []
	tagPaths = getTableTagPaths(LineNumber)
	# Get tag values for list of tags using table data function. Sorts out Empty tables
	for path in tagPaths:
		newValues = getTableData(path)
		if not newValues[5]:
			valSide.append(newValues)
			
	unsortedDS = system.dataset.toDataSet(dsHeaders, valSide)
	#Sort by Time Left ascending
	firstSortDS = system.dataset.sort(unsortedDS, "TimeLeft", 1)
	pyDS1 = system.dataset.toPyDataSet(firstSortDS)
	
	#Get time constants from configurable tags
	i = 0
	newRows1 = []
	minPath = CALC_FOLDER+str(LineNumber)+"/MinTimeToAlarm"
	initTimes = system.tag.readBlocking([InitConst1,InitConst2,minPath])
	timeSet = False
	timeAlarm = 0
	#date = system.date.getDate(2021, 6, 15)
	alarmTime = system.date.now() #system.date.setTime(date, 14, 59, 0)

	# Calculate time difference column and alarm state for each row. For first alarm row, calculate estimated lockup time
	for row in pyDS1:
		if i==0:
			timeCount =  initTimes[0].value
			timePrev = 0
		else:
			timePrev = timeCount
			timeCount += initTimes[1].value
		calcTime = timeCount - row[2]
		if calcTime < 0 and (timeCount<=int(initTimes[2].value*60) or int(initTimes[2].value)==0):
			inAlarm = True
			if not timeSet:
				timeSet = True
				alarmTime = system.date.addMinutes(alarmTime,timePrev)
				timeAlarm = timePrev
		elif timeSet and calcTime < 0:
			inAlarm = True
		else:
			inAlarm = False
		newRows1.append([row[0],timeCount,row[2],calcTime,inAlarm])
		i += 1
	secondSortDS = system.dataset.toDataSet(headers, newRows1)
	# Write to dataset, alarm, and lockup time tags
	dsTagPaths = [CALC_FOLDER+str(LineNumber)+"/CalculateDS"]
	system.tag.writeBlocking(dsTagPaths, [secondSortDS])
	tagWritePaths = [CALC_FOLDER+str(LineNumber)+"/Lockup Alarm", CALC_FOLDER+str(LineNumber)+"/LockupTime",CALC_FOLDER+str(LineNumber)+"/TimeUntilLockup"]
	alarmDate = str(system.date.format(alarmTime,"MM/dd hh:mm aa"))
	
	tagWriteVals = [inAlarm,alarmDate,timeAlarm]
	system.tag.writeBlocking(tagWritePaths, tagWriteVals)
	return secondSortDS
	
def getTableData(tagPath):
	"""
	Browses the table data folder and returns relevant table data for the chosen table UDT
	
	Args:
		tagPath(string): Tag path for specific table to read
		
	Returns:
		list of data (Table Number, Time Open placeholder, Time Left, Calc Time placeholder, State, Empty Status)
	"""
	# Define which states are considered empty/irrelevant
	emptyStates = EMPTY_STATES
	
	# Read values for table
	tagPaths = []
	pathState = tagPath + '/table/statusID'
	pathTime = tagPath + '/timeLeft'
	tableNumber = tagPath + "/Parameters.tableNumber"
	strScheduled = tagPath + "/enabledScheduling"
	tagPaths.append(pathState)
	tagPaths.append(pathTime)
	tagPaths.append(tableNumber)
	tagPaths.append(strScheduled)
	tagValues = system.tag.readBlocking(tagPaths)
	state = tagValues[0].value
	if str(state) in emptyStates or str(tagValues[1].quality) == "Bad" or str(tagValues[0].quality) == "Bad":
		isEmpty = True
	elif tagValues[3].value==True:
		isEmpty = False
	else:
		isEmpty = True
	
	return [tagValues[2].value,0,tagValues[1].value,0,tagValues[0].value,isEmpty]

	
