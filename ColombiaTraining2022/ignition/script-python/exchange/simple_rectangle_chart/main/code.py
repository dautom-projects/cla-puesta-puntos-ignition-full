def createChart(inputData, inputDefinitions, fallbackColor, tooltipDateFormat, historicalMode, detailed = False):
	"""
	Creates a chart containing a series of SVG rects that represent time
		series data.
		
	Args:
		inputData: List containing time series data.
		inputDefinitions: List containing the color (rect fill) and label
			(rect tooltip) for each value.
		fallbackColor: Color that is used for values that do not contain
			a corresponding definion.
		tooltipDateFormat: Format string used to format the start and
			end datetime in the tooltips.
		historicalMode: Object containing both a flag that denotes whether 
			the data being displayed is historical and an end date that is
			used as the end date for the last row in the data (if 
			historicalMode.enabled = true).
		detailed: Flag denoting whether the detailed chart is being
			displayed, and if it is returns the start/end of the data and
			the checked definitions.
	
	Returns:
		An HTML string containing the SVG chart.
	"""			
	# Check the data to make sure that it can be rendered properly in this chart.
	results = exchange.simple_rectangle_chart.data_handler.handleData(inputData)
	
	if results['canRenderChart'] == False:
		# Data did not pass the checks. Display the reason.
		# If detailed version, return object expected by
		# the detailed chart.
		if detailed == False:
			return results['reason']
		else: 
			return {'html': results['reason'], 'canRenderChart': False}
	else:
		# Data passed the checks, can proceed to create the chart.
		data = results['data']
		
		# Check the definitions and put them in a dictionary {value: {'color': color, 'label': label}}.
		definitions = exchange.simple_rectangle_chart.definition_handler.handleDefinitions(inputDefinitions)
		
		# Check to see if tooltipDateFormat is the correct type and if it isn't then use the default.
		tooltipDateFormat = exchange.simple_rectangle_chart.helper.checkStringParam(tooltipDateFormat, 'MM/dd h:mm a')
		
		# Check to see if fallbackColor is the correct type and if it isn't then use the default.
		fallbackColor = exchange.simple_rectangle_chart.helper.checkStringParam(fallbackColor, 'var(--neutral-80)')
		
		# If historicalMode does not contain the expected object members, set it to default.
		historicalMode = exchange.simple_rectangle_chart.helper.checkObjParam(historicalMode, {'enabled': {'default': False, 'type': 'boolean'}, 'endDate': {'default': None, 'type': 'date'}})
		
		# Get the start datetime of the first row.
		dataStart = data[0]['t_stamp']
		
		# Figure out the end datetime based on the historicalMode.enabled flag.
		if historicalMode['enabled']:
			if historicalMode['endDate'] != None and historicalMode['endDate'] > data[-1]['t_stamp']:
				# End date for historical mode is set to non-null date that is greater than
				# the t_stamp of the final row. Using historical mode end date as dataEnd.
				dataEnd = historicalMode['endDate']
			else:
				# End date for historical mode is either null or is a date less than or equal
				# to the t_stamp of the final row. Using t_stamp of final row as dataEnd.
				dataEnd = data[-1]['t_stamp']
		else:
			# Viewing in realtime mode. Using now() as dataEnd.
			dataEnd = system.date.toMillis(system.date.now())
		
		# Get total duration of data (ms), divide by 1000, and use the result as the width of the viewBox.
		viewboxWidth = (dataEnd - dataStart) / 1000.0
		
		# Create the series of rects.
		rects = createRects(data, definitions, tooltipDateFormat, dataEnd, fallbackColor)
		
		html = '<html> \
			<head> \
			<style> \
			.flexContainerSimpleRectangle {{ display: flex; flex-direction: column; height: 100vh}} \
			</style> \
			</head> \
			<body> \
			<div class="flexContainerSimpleRectangle"> \
			<svg style="flex: 1 1 100px" viewBox="0 0 {viewboxWidth} 10" preserveAspectRatio="none"> \
			<g height = "10">{rects}</g> \
			</svg> \
			</div> \
			</body> \
			</html>'.format(rects = rects, viewboxWidth=viewboxWidth)
		
		# Return just the html if detailed param is False, otherwise also return the start and
		# end of the data for the date range of the detailed version.
		if detailed == False:
			return html
		else:
			return {'html': html, 'canRenderChart': True, 'start': dataStart, 'end': dataEnd, 'definitions': definitions}
			
def createRects(data, definitions, dateFormat, dataEnd, fallbackColor):
	"""
	Creates a series of SVG rects that represent the time series data.
		
	Args:
		data: List containing time series data.
		definitions: List containing the color (rect fill) and label
			(rect tooltip) for each value.
		dateFormat: Format string for the dates in the tooltips.
		dataEnd: End date of the data.
		fallbackColor: Color that is used for values that do not contain a 
			corresponding definition.
	
	Returns:
		A string containing the series of SVG rects.
	"""
	# Create the rects string.
	rectList = ''
	
	# Create the x-position for the first rect.
	xPos = 0
	
	# Create a rect for each row in the data.
	for x in range(0, len(data) - 1):
		# Get the value, start, end, and previous end.
		rectValue = data[x]['value']
		start = data[x]['t_stamp']
		end = data[x + 1]['t_stamp']
		
		# Get the rect definition.
		rectDefs = definitions.get(rectValue)
		
		# Get the color for the rect and the label for the tooltip.
		color, label = getDefinition(rectValue, definitions, fallbackColor)
			
		# Create the rect and add it to the rect list.
		rect, width = createRect(start, end, xPos, color, label, dateFormat)
		rectList += rect
		
		# Add the width of this rect to the prevX (starting point for the next rect).
		xPos += width
		
	# Create the final rect.
	lastRectValue = data[-1]['value']
	lastRectStart = data[-1]['t_stamp']
	
	color, label = getDefinition(lastRectValue, definitions, fallbackColor)
	
	rect, width = createRect(lastRectStart, dataEnd, xPos, color, label, dateFormat)
	rectList += rect
		
	return rectList

def createRect(start, end, x, color, label, dateFormat):
	"""
	Creates a SVG rect that represents a row in the time series data.
		
	Args:
		start: Start time of the row of data (unixtime).
		end: End time of the row of data (unixtime).
		x: X-position of the rect.
		color: Fill color for the rect.
		label: Text that is displayed in the tooltip.
		dateFormat: Format string for the dates in the tooltips.
	
	Returns:
		A string containing the rect and the width of the rect.
	"""
	# Create the startDate and endDate strings for the tooltip.
	tooltipStart = system.date.format(system.date.fromMillis(start), dateFormat)
	tooltipEnd = system.date.format(system.date.fromMillis(end), dateFormat)
	
	# Create the text for the tooltip.
	tooltip = '{label}: {start} to {end}'.format(label = label, start = tooltipStart, end = tooltipEnd)
	
	# Calculate the width of the rect.
	width = (end - start) / 1000.0
	
	# Create the rect.
	rect = '<rect x="{x}" y="0" width="{width}" height="10" fill="{color}"><title>{tooltip}</title></rect>'.format(x=x, width=width, color=color, tooltip=tooltip)
	
	return rect, width
	
def getDefinition(rectValue, definitions, fallbackColor):
	"""
	Attempts to retrieve a definition utilizing the value.
		
	Args:
		rectValue: Value from the time series data.
		definitions: List containing the color (rect fill) and label
			(rect tooltip) for each value.
		fallbackColor: Color that is used for values that do not contain a 
			corresponding definition.
	
	Returns:
		A color for the rect fill and a label for the tooltip.
	"""	
	# Get the definition for the first rect.
	rectDefs = definitions.get(rectValue)
	
	if rectDefs != None:
		# Get the label for the tooltip for the first rect.
		label = rectDefs.get('label', str(rectValue))
	
		# Get the fill color for the rect.
		color = rectDefs.get('color', fallbackColor)
	else:
		# Use value for the label.
		label = str(rectValue)
		
		# Use the fallback color.
		color = fallbackColor
		
	return color, label