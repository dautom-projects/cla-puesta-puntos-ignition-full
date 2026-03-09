def browseTagsRecursive(initPath, filter):
	"""
	browseTagsRecursive uses the built in system.tag.browse function and recursively walks through the tag folder structure of the initPath folder path.
	This spreads the workload of the browse function accross multiple calls for the various folders contained within the initPath folder path.
	
	Args:
		initPath (string): Parent folder path. If browsing all tags in the project, leave blank.
		filter (dictionary): A dictionary of browse filter parameters. Parameters include name (with wildcards '*'), dataType, valueSource, tagType,
									typeId, quality (specify Good or Bad), and maxResults.
	
	Returns:
		tags (list of dictionaries): Contains a list of tag dictionaries, one for each tag found during the browse.
		
	"""
	def getTagList(initPath, filter):
		# Call the browse function and place 'Result' object in results
		results = system.tag.browse(initPath, filter)
		tagList = results.getResults()
		
		# Loop through every item in the tag list of dictionaries from results and append it to a tag list
		for result in tagList:
			tags.append(result)
			# If the item has children, call the function to repeat the process but starting at the child.
			if result['hasChildren'] == True:
				getTagList(result['fullPath'], filter)
			
	# Create empty list for tag dictionaries to populate
	tags = []
	getTagList(initPath, filter)
			
	# Returns the list of tag dictionaries
	return tags

def enableTags(initPath):
	"""
	enableTags will set the "Enabled" attribute of the tags contained within the folder path initPath to "True"
	
	Args:
		initPath (string): Parent folder path. All tags contained in this folder and its subfolders will be enabled.
	
	Returns:
		None
	
	"""
	print "Browsing tags in %s" % initPath
	filter = {}
	tags = browseTagsRecursive(initPath, filter)
	
	print "Enabling tags under %s" %initPath
	collisionPolicy = 'm'
	for tag in tags:
		if str(tag['tagType']) != "Folder":
			configs = system.tag.getConfiguration(tag['fullPath'],False)
			configs[0]['enabled'] = True
			tagPath = str(tag['fullPath'])
			index = tagPath.rfind('/')
			rootPath = tagPath[:index]		
			system.tag.configure(rootPath, configs, collisionPolicy)
	print "tags enabled."
	
def disableTags(initPath):
		"""
		disableTags will set the "Enabled" attribute of the tags contained within the folder path initPath to "False"		
		
		Args:
			initPath (string): Parent folder path. All tags contained in this folder and its subfolders will be disabled.
			
		Returns:
			None
				
		"""
		print "Browsing tags in %s" % initPath
		filter = {}
		tags = browseTagsRecursive(initPath, filter)
		
		print "Disabling tags under %s" %initPath
		collisionPolicy = 'm'
		for tag in tags:
			if str(tag['tagType']) != "Folder":
				configs = system.tag.getConfiguration(tag['fullPath'],False)
				configs[0]['enabled'] = False
				tagPath = str(tag['fullPath'])
				index = tagPath.rfind('/')
				rootPath = tagPath[:index]		
				system.tag.configure(rootPath, configs, collisionPolicy)
		print "tags disabled."
