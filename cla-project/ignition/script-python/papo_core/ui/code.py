"""
papo_core.ui

Visual behavior logic for PAPO forms.
Handles accordion toggle, form initialization, and title labels.

Version: 1.4.0

Changelog:
	2026-11-27 | William M. | v1.4.0 - Added signalIndicatorHtml (header indicator of the connection between the
		device and the gateway)
	2026-10-28 | William M. | v1.3.0 - initForm rebuilds custom.insights with the opening time (a record
		without comments saved the shift and time of the design)
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

	Sets initialPapoDateTime to current time for shift/time display and rebuilds
	custom.insights with it: its binding (Observaciones TextField + preInsight) ran
	before with the timestamp saved in the design and only runs again when the
	operator writes, so a record without comments kept the shift and time of the design.

	Version: 1.1.0

	Changelog:
		2026-10-28 | William M. | v1.1.0 - Rebuilds custom.insights with the opening time

	Args:
		root (View): The form view (self of the view onStartup)

	Returns:
		None
	"""
	root.custom.initialPapoDateTime = system.date.now()

	try:
		textField = root.getChild("root").getChild("TextField")
		text = textField.props.text if textField is not None else None
		root.custom.insights = preInsight(root, text or u"")
	except Exception as e:
		ref = str(getattr(root.custom, "referencePapo", "papo_core.ui"))
		system.util.getLogger(ref).error("initForm insights: {}".format(str(e)))


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


# Browser script of the header signal indicator (ASCII only: it travels base64-encoded and runs with eval(atob()))
SIGNAL_JS = """
(function () {
	var PING_URL = '/StatusPing';
	var INTERVAL_MS = 5000;
	var TIMEOUT_MS = 3000;
	var SAMPLES = 3;
	var IDLE_BAR = 'rgba(255, 255, 255, 0.3)';
	var LEVELS = [
		{maxMs: 300, bars: 4, color: '#4CAF50', text: 'Buena'},
		{maxMs: 800, bars: 3, color: '#FFC107', text: 'Regular'},
		{maxMs: Infinity, bars: 2, color: '#FF9800', text: 'D\\u00e9bil'}
	];
	var OFFLINE = {bars: 0, color: '#F44336', text: 'Sin conexi\\u00f3n'};
	var CHECKING = {bars: 0, color: '#FFFFFF', text: 'Midiendo'};

	// Already running in this tab (the header was drawn again): only repaint the new container. The global
	// name must differ from the container id: an element id is also a window property
	if (window.__papoSignalMonitor) {
		window.__papoSignalMonitor.render();
		return;
	}

	var state = {samples: [], level: CHECKING, ms: null};

	function build(root) {
		var ns = 'http://www.w3.org/2000/svg';
		var svg = document.createElementNS(ns, 'svg');
		svg.setAttribute('width', '22');
		svg.setAttribute('height', '18');
		svg.setAttribute('viewBox', '0 0 20 16');
		for (var i = 0; i < 4; i++) {
			var bar = document.createElementNS(ns, 'rect');
			bar.setAttribute('x', String(1 + i * 5));
			bar.setAttribute('y', String(12 - i * 3));
			bar.setAttribute('width', '3');
			bar.setAttribute('height', String(3 + i * 3));
			bar.setAttribute('rx', '1');
			svg.appendChild(bar);
		}
		var text = document.createElement('span');
		root.style.display = 'inline-flex';
		root.style.alignItems = 'center';
		root.style.gap = '6px';
		root.style.whiteSpace = 'nowrap';
		root.style.fontSize = '13px';
		root.appendChild(svg);
		root.appendChild(text);
	}

	function render() {
		var root = document.getElementById('papo-signal');
		if (!root) {
			return;
		}
		if (!root.firstChild) {
			build(root);
		}
		var level = state.level;
		var bars = root.getElementsByTagName('rect');
		for (var i = 0; i < bars.length; i++) {
			bars[i].setAttribute('fill', i < level.bars ? level.color : IDLE_BAR);
		}
		var text = root.getElementsByTagName('span')[0];
		text.textContent = state.ms === null ? level.text : level.text + ' ' + Math.round(state.ms) + ' ms';
		text.style.color = level === OFFLINE ? level.color : '#FFFFFF';
		root.title = 'Conexi\\u00f3n con el servidor: ' + (state.ms === null ? level.text : Math.round(state.ms) + ' ms');
	}

	function setLevel(level, ms) {
		state.level = level;
		state.ms = ms;
		render();
	}

	// Average round trip of the last SAMPLES requests decides the level
	function record(ms) {
		state.samples.push(ms);
		if (state.samples.length > SAMPLES) {
			state.samples.shift();
		}
		var sum = 0;
		for (var i = 0; i < state.samples.length; i++) {
			sum += state.samples[i];
		}
		var average = sum / state.samples.length;
		for (var j = 0; j < LEVELS.length; j++) {
			if (average <= LEVELS[j].maxMs) {
				setLevel(LEVELS[j], average);
				return;
			}
		}
	}

	function offline() {
		state.samples = [];
		setLevel(OFFLINE, null);
	}

	function ping() {
		if (!navigator.onLine) {
			offline();
			return;
		}
		var controller = window.AbortController ? new AbortController() : null;
		var timer = setTimeout(function () {
			if (controller) {
				controller.abort();
			}
		}, TIMEOUT_MS);
		var start = performance.now();
		fetch(PING_URL + '?t=' + Date.now(), {cache: 'no-store', signal: controller ? controller.signal : undefined})
			.then(function (response) {
				if (!response.ok) {
					throw new Error('HTTP ' + response.status);
				}
				return response.text();
			})
			.then(function () {
				clearTimeout(timer);
				record(performance.now() - start);
			})
			.catch(function () {
				clearTimeout(timer);
				offline();
			});
	}

	window.__papoSignalMonitor = {render: render, ping: ping};
	render();
	ping();
	setInterval(ping, INTERVAL_MS);
	window.addEventListener('online', ping);
	window.addEventListener('offline', ping);
})();
"""

# Container of the indicator plus a hidden image whose failed load runs the script
SIGNAL_HTML = '<span id="papo-signal"></span><img src="data:," alt="" style="display:none" onerror="eval(atob(\'{script}\'))">'


def signalIndicatorHtml():
	"""
	HTML of the header indicator of the connection between the device (tablet or PC) and the gateway.

	Perspective bindings run on the gateway, so the measurement runs in the browser: the script travels in a Markdown
	component (escapeHtml false) and runs when its hidden image fails to load. Every 5 s it requests /StatusPing and
	draws signal bars from the average round trip of the last 3 requests: Buena (300 ms or less, 4 bars), Regular
	(800 ms or less, 3), Debil (more, 2) and Sin conexion (no answer in 3 s or the device offline). Display only.

	Version: 1.0.0

	Changelog:
		2026-11-27 | William M. | v1.0.0 - Initial version (connection indicator for the tablets)

	Returns:
		str: HTML for the Markdown props.source, or "" on error
	"""
	import base64

	logger = system.util.getLogger("papo_core.ui.signalIndicatorHtml")

	try:
		return SIGNAL_HTML.format(script=base64.b64encode(SIGNAL_JS.strip()))

	except Exception as e:
		logger.error("Error building the signal indicator: {}".format(str(e)))
		return ""
