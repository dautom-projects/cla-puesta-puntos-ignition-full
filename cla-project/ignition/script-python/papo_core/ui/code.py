"""
papo_core.ui

Visual behavior logic for PAPO forms.
Handles accordion toggle, form initialization, and title labels.

Version: 1.2.1

Changelog:
	2026-10-28 | William M. | v1.2.1 - preInsight takes the shift and time in plant local time
		(java.util.Calendar America/Bogota) instead of system.date.getHour24
	2026-10-22 | William M. | v1.2.0 - Added getShift (java.util.Calendar, America/Bogota)
	2026-07-21 | William M. | v1.1.0 - Added confirmSave for save button onClick standardization
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

	from java.util import Calendar, TimeZone
	cal = Calendar.getInstance(TimeZone.getTimeZone("America/Bogota"))
	cal.setTime(dateTime)
	shift = getShift(dateTime)

	timeStr = "{:02d}:{:02d}".format(cal.get(Calendar.HOUR_OF_DAY), cal.get(Calendar.MINUTE))
	return " | T: {}, H: {} - ".format(shift, timeStr) + value


def confirmSave():
	"""
	Show the standard save confirmation dialog for form save buttons.

	Fires saveDataRoot on confirm. Message is fixed across all forms.

	Returns:
		None
	"""
	alerts.showAlert(
		state="warning",
		title="Guardar registro",
		message="Esta seguro de que desea guardar el registro?",
		btnTextPrimary="Si",
		btnTextSecondary="No",
		btnActionPrimary="saveDataRoot"
	)
	
def getSecurityImage(papoItemID,dbConnection):

	db = dbConnection
	
	# 1. Query
	query = "SELECT Description FROM papoitem WHERE ID = ?"
	ds = system.db.runPrepQuery(query, [papoItemID], db)
	
	if ds and ds.getRowCount() > 0:
	    descripcion = str(ds.getValueAt(0, "Description")).strip().lower()
	    print "Descripcion encontrada:", descripcion
	
	    # 2. Diccionario normalizado
	    paths = {
	        "botas de seguridad": "EPP/botas.png",
	        "botas de pvc": "EPP/botaspvc.png",
	        "careta respirador": "EPP/caretarespirador.png",
	        "gafas de seguridad": "EPP/gafas.png",
	        "gafas de seguridad de sello": "EPP/gafassello.png",
	        "guante quimico": "EPP/guantequimico.png",
	        "guantes nitrilo": "EPP/guantesnitrilo.png",
	        "guantes poli/algodon": "EPP/guantespolialgodon.png",
	        "multimetro": "EPP/multimetro.png",
	        "protector auditivo tipo diadema": "EPP/protectortipocopa.png",
	        "tapabocas": "EPP/tapaboca.png",
	        "tapon oido": "EPP/tapones.png",
	        "valvula de cierre": "EPP/valvulacierre.png"
	    }
	
	    # 3. Obtener ruta
	    url = paths.get(descripcion, "EPP/default.png")
	    print "Ruta asignada:", url
	else:
	    print "No se encontró descripción para ID:", papoItemID
	
	return '/system/images/'+url


def getShift(dateTime=None):
	"""
	Return the plant shift (1, 2 or 3) for a timestamp in plant local time.

	Uses java.util.Calendar with TimeZone America/Bogota so the result does
	not depend on the gateway timezone.
	T1 22:00-06:00, T2 06:00-14:00, T3 14:00-22:00.

	Version: 1.0.0

	Changelog:
		2026-10-22 | William M. | v1.0.0 - Initial version

	Args:
		dateTime (java.util.Date): Timestamp to evaluate. None uses the current time

	Returns:
		int: Shift number (1, 2 or 3), or None on error
	"""
	from java.util import Calendar, TimeZone

	logger = system.util.getLogger("papo_core.ui.getShift")

	try:
		cal = Calendar.getInstance(TimeZone.getTimeZone("America/Bogota"))
		if dateTime is not None:
			cal.setTime(dateTime)
		hour = cal.get(Calendar.HOUR_OF_DAY)

		if hour >= 22 or hour < 6:
			return 1
		elif hour < 14:
			return 2
		return 3

	except Exception as e:
		logger.error("Error computing shift for {}: {}".format(dateTime, str(e)))
		return None
