def createDateRange(start, end, dateRangeDateFormat, spaceBetween, canRenderChart):
	"""
	Creates the date range for the detailed chart utilizing the
		dateRangeDateFormat to format the start/end dates.
		
	Args:
		start: Start date of the data.
		end: End date of the data.
		dateRangeDateFormat: Format string such as "MM/dd/yyyy h:mm a".
		spaceBetween: Flag that denotes if a flex-container with justify-content=
			space-between will be used to display the date range.
		canRenderChart: Flag that denotes whether the data passed the checks.
	
	Returns:
		A string representing the date range of the chart.
	"""	
	# If data did not pass the checks, return empty string.
	if canRenderChart == False:
		return ''
	
	# If dateRange.dateFormat is empty or null, set it to the default.
	dateRangeDateFormat = exchange.simple_rectangle_chart.helper.checkStringParam(dateRangeDateFormat, 'MM/dd h:mm a')
	
	# Create the start and end date objects (from the start and end millis).
	startDate = system.date.fromMillis(start)
	endDate = system.date.fromMillis(end)
	
	# Create the start label and end label.
	startLabel = system.date.format(startDate, dateRangeDateFormat)
	endLabel = system.date.format(endDate, dateRangeDateFormat)
	
	if not spaceBetween:
		return '{start} - {end}'.format(start = startLabel, end = endLabel)
	else:
		# Display date range in a flex-container with justify-content set to space-between.
		return '<html> \
				<head> \
				<style> \
				.flexContainerDateRange {{ display: flex; justify-content: space-between}} \
				</style> \
				</head> \
				<body> \
				<div class="flexContainerDateRange"> \
				<div>{start}</div> \
				<div>{end}</div> \
				</div> \
				</body> \
				</html>'.format(start = startLabel, end=endLabel)

def handleParams(title, legend, dateRange):
	"""
	Ensures that the title, legend, and dateRange object parameters 
		have the expected object members.
		
	Args:
		title: Object parameter containing the title text, display,
			and style.
		legend: Object parameter containing the legend icon width
			and height, display, and style.
		dateRange: Object parameter containing the date range date
			format, display, and style.
	
	Returns:
		An object containing the title, legend, and dateRange settings.
	"""
	# If title does not contain the expected object members, set it to default.
	title = exchange.simple_rectangle_chart.helper.checkObjParam(title, {'text': {'default': '', 'type': 'string'}, \
		'display': {'default': True, 'type': 'boolean'}, 'textStyle': {'default': {}, 'type': 'object'}})	
	
	# If legend does not contain the expected object members, set it to default.
	legend = exchange.simple_rectangle_chart.helper.checkObjParam(legend, {'display': {'default': True, 'type': 'boolean'}, \
		'icon': {'default': {'width': 24, 'height': 24}, 'type': 'object'}, 'textStyle': {'default': {}, 'type': 'object'}})
		
	# If dateRange does not contain the expected object members, set it to default.
	dateRange = exchange.simple_rectangle_chart.helper.checkObjParam(dateRange, {'dateFormat': {'default': 'MM/dd/yyyy h:mm a', 'type': 'string'}, \
		'display': {'default': True, 'type': 'boolean'}, 'textStyle': {'default': {}, 'type': 'object'}, 'spaceBetween': {'default': False, 'type': 'boolean'}})
		
	return {'title': title, 'legend': legend, 'dateRange': dateRange}
	

def createLegendItems(definitions, icon, textStyle, canRenderChart):
	"""
	Creates the list of instances for the legend.
		
	Args:
		definitions: List containing the color (rect fill) and label
			(rect tooltip) for each value.
		icon: Object that defines the width and height of the legend
			item icons.
		textStyle: Style object containing for the legend item labels.
		canRenderChart: Flag that denotes whether the data passed the checks.
	
	Returns:
		A list of instances for the legend.
	"""	
	# Create the instances list for the legend.
	instances = []
	
	# If data did not pass the checks, do not attempt to render legend.
	if canRenderChart == False:
		return instances
		
	# Create an instance for each definition.
	for defValue, definition in definitions.iteritems():
		# Only create the legend item if the definition contains a color.
		if 'color' in definition:
			color = definition['color']
		
			# See if definition has a label.
			if 'label' in definition:
				# Definition contains a label.
				label = definition['label']
			else:
				# Definition does not contain a label, utilizing the value.
				label = defValue
				
			# Create the instance and add it to the list.
			instances.append({'color': color, 'label': label, 'icon': icon, 'textStyle': textStyle})
	
	return instances