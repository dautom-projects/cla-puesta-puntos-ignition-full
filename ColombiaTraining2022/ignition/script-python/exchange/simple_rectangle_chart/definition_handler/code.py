def handleDefinitions(inputDefinitions):
	"""
	Checks the definitions to make sure that they are in a
		supported format
		
	Args:
		inputDefinitions: List of definition objects.
	
	Returns:
		Dictionary containing the definitions.
	"""	
	# Define dict that will hold definitions.
	definitions = {}
	
	# Check if it is a list.
	if not exchange.simple_rectangle_chart.helper.isList(inputDefinitions):		
		return definitions
		
	# Iterate through the input definitions to check each one.
	for index, inputDefinition in enumerate(inputDefinitions):
		# See if input definition is an object.
		if exchange.simple_rectangle_chart.helper.isObject(inputDefinition):	
			# Check if the definition has a 'value' member.
			if 'value' in inputDefinition:
				# Get the definition value.
				defValue = inputDefinition['value']
				
				# Check if definition has color or label.
				hasColor = 'color' in inputDefinition
				hasLabel = 'label' in inputDefinition
				
				if hasColor or hasLabel:
					# Definition has a color or label, begin creating the definition.
					definitions[defValue] = {}
					
					if hasColor:
						# Add the color to the definition.
						definitions[defValue]['color'] = inputDefinition['color']
							
					if hasLabel:
						# Add the label to the definition.
						definitions[defValue]['label'] = inputDefinition['label']
			
	return definitions