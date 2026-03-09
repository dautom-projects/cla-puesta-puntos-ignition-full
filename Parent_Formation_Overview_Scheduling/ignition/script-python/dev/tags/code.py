def addOPCTag(row):
	COLLISION_POLICY = 'o'
	basePath = row.get('parentPath')
	tag = 	{
				'name':row.get('tagName'),
				'dataType':row.get('dataType'),
				'valueSource':row.get('valueSource'),
				'opcServer':row.get('opcServer'),
				'opcItemPath':row.get('opcItemPath'),
				'tagGroup':row.get('tagGroup'),
				'sampleMode':'tagGroup'
			}
	
	system.tag.configure(basePath,[tag],COLLISION_POLICY)

def addUDTTag(row):
	COLLISION_POLICY = 'o'
	basePath = row.get('parentPath')
	tag = 	{
				'name':row.get('tagName'),
				'typeID':row.get('typeID'),
				'tagType':'UdtInstance',
				'parameters': 	{
									'aoiDeviceName':row.get('aoiDeviceName'),
									'aoiDirectTG':row.get('aoiDirectTG'),
									'aoiHistoricalTG':row.get('aoiHistoricalTG'),
									'aoiLeasedTG':row.get('aoiLeasedTG'),
									'aoiNode':row.get('aoiNode'),
									'aoiServer':row.get('aoiServer'),
									'aoiTag':row.get('aoiTag')
								}
			}
	
	system.tag.configure(basePath,[tag],COLLISION_POLICY)

def getTagConfig(path):
	# This example will get the configuration of a single Tag
 
	# Update the path here with the Tag path you're trying to reach
	 
	# Get the configurations
	tags = system.tag.getConfiguration(path)
	 
	for tagDict in tags:
		 
		# Iterate over the dictionary with the iteritems function
		for key, value in tagDict.iteritems():
			 
			# Do something with the keys and values
			print key, ' : ', value

def exportTags(initPath):
	import csv
	tagListAtomic = tags.util.browseTagsRecursive(initPath, filter = {'tagType':'AtomicTag'})
	#filter = 'UdtInstance'	
	#tagListUDT = tags.util.browseTagsRecursive(initPath,filter)

	#for tag in tagListAtomic:
		#path = 
		#tagConfig = system.tag.getConfiguration(path)
	headers = ['fullPath','name','dataType']
	tagList = []
	for tagDict in tagListAtomic:
		values = []
		for key, value in tagDict.iteritems():
			if key == 'fullPath':
				values.append(value)
			if key == 'name':
				values.append(value)
			if key == 'dataType':
				values.append(value)
		tagList.append(values)
		print values
	dataset = system.dataset.toDataSet(headers,tagList)
	return dataset

def getAlarms(tagPath):	
	
		from com.inductiveautomation.ignition.common.tags.paths.parser import TagPathParser
		alarms = []
		def iterTagConfig(dictIn, folderIn = ''):
			keys = dictIn.keys()
			#Move tags and alarms to end of list.  I do not recall why, but it is really, really important.
			if 'tags' in keys:
				keys.append(keys.pop(keys.index('tags')))
			if 'alarms' in keys:
				keys.append(keys.pop(keys.index('alarms')))
				
			for key in keys:
				#If the value of dictIn[key] is a dict, then it is a folder like structure that has child tags.  Iterate through this
				if isinstance(dictIn[key], dict):
					iterTagConfig(dictIn[key])
				elif key == 'tags':
					for tag in dictIn[key]:
						if str(tag["path"]) != "_types_":
							iterTagConfig(tag, folderIn = folderIn + str(dictIn['path']) + '/' if folderIn else str(dictIn['path']))      
				elif key == 'alarms':
					#This is what we are looking for.  Each tag in this alarm item is an alarm, so we add them to the list.  Use qualified tag paths because they are exact, and I hear they make you look cooler.
					for tag in dictIn[key]:
						tp = TagPathParser.parseSafe(folderIn+"/"+str(dictIn['path']) if folderIn else str(dictIn['path']))
						qp = "prov:%s:/tag:%s:/alm:%s"%(tp.source,tp.toStringPartial(),tag["name"])
						alarms.append([qp])
						iterTagConfig(tag,folderIn = folderIn + str(dictIn['path']))	
		if tagPath:
			folder = tagPath
			#Root level browse
			nodes = system.tag.getConfiguration(folder, True)
		
			for item in nodes:
				iterTagConfig(item)
		
		return alarms	
