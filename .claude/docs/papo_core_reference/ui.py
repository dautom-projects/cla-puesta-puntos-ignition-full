"""
papo_core.ui

Visual behavior logic for PAPO forms.
Handles accordion toggle, form initialization, and title labels.

Version: 1.0.0

Changelog:
	2026-07-06 | William | v1.0.0 - Initial Project Library version
"""

STYLE_ACTIVE = "button-questions"
STYLE_INACTIVE = "button-questions-2"


def toggleSection(root, sectionIndex):
	"""
	Toggle accordion section: expand clicked group, collapse others.

	Scans root children for FlexContainerGroups and Sections by name,
	independent of component hierarchy.

	Args:
		root (Component): The root component
		sectionIndex (int): Section number clicked (1-based)

	Returns:
		None
	"""
	thisSectionIndex = int(sectionIndex)

	groups = {}
	sections = {}

	# Scan root children for groups and sections
	for child in root.getChildren():
		childName = child.meta.name
		if childName.startswith("FlexContainerGroup"):
			try:
				idx = int(childName.replace("FlexContainerGroup", ""))
				groups[idx] = child
			except Exception:
				pass
		elif childName.startswith("Section"):
			try:
				idx = int(childName.replace("Section", ""))
				sections[idx] = child
			except Exception:
				pass

	# Toggle each group based on clicked section
	for idx, group in groups.items():
		if not group.custom.get("baseBasisPx", None):
			basisPx = int(str(group.position.basis).replace("px", "")) if group.position.basis else 100
			group.custom.baseBasisPx = basisPx

		groupBasePx = int(group.custom.get("baseBasisPx", 0))

		if idx == thisSectionIndex:
			currentDisplay = bool(group.position.display)
			newDisplay = not currentDisplay
			group.position.display = newDisplay
			group.position.basis = str(groupBasePx) + "px" if newDisplay else "0px"
		else:
			group.position.display = False
			group.position.basis = "0px"

	# Update section button styles
	for idx, section in sections.items():
		if idx == thisSectionIndex and groups.get(idx) and bool(groups[idx].position.display):
			section.props.style.classes = STYLE_ACTIVE
		else:
			section.props.style.classes = STYLE_INACTIVE


def initForm(root):
	"""
	Initialize a PAPO form on startup.

	Sets initialPapoDateTime to current time for shift/time display.

	Args:
		root (Component): The root component

	Returns:
		None
	"""
	root.custom.initialPapoDateTime = system.date.now()


def preInsight(root, value):
	"""
	Build the pre-insight prefix with shift and time for comments.

	Prepends shift number and time to the insight value so comments
	carry their turno and hora context.

	Args:
		root (Component): The root component (for custom access)
		value (str): The base insight value to append to

	Returns:
		str: Formatted " | T: {shift}, H: {HH:MM} - {value}"
	"""
	dateTime = root.custom.initialPapoDateTime
	if dateTime is None:
		return ""

	hour = system.date.getHour24(dateTime)
	minute = system.date.getMinute(dateTime)

	if hour >= 22 or hour < 6:
		shift = 1
	elif hour >= 6 and hour < 14:
		shift = 2
	else:
		shift = 3

	timeStr = "{:02d}:{:02d}".format(hour, minute)
	return " | T: {}, H: {} - ".format(shift, timeStr) + value
