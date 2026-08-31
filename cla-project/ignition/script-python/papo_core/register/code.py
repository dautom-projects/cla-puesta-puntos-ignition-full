"""
papo_core.register

Data collection and saving logic for PAPO forms.
Handles answer recopilation, saving to registerhistory,
and operator signature flow.

Version: 1.0.1

Changelog:
	2026-07-22 | William M. | v1.0.1 - Fix save() silently skipping flat forms
		(no FlexContainerGroup) since allItems is always empty for them
	2026-07-06 | William | v1.0.0 - Initial Project Library version
"""

from java.lang import String


# ==================== INTERNAL HELPERS ====================

def _appendItem(candidate, outList):
	"""Append a valid answer item dict to the output list."""
	if not candidate:
		return
	try:
		outList.append({
			"papoItemID": candidate.get("papoItemID"),
			"registerTypeID": candidate.get("registerTypeID"),
			"answer": candidate.get("answer")
		})
	except Exception:
		pass


def _gatherFromInstances(component):
	"""Extract items from Flex Repeater props.instances."""
	items = []
	try:
		if hasattr(component, "props") and hasattr(component.props, "instances"):
			for inst in component.props.instances:
				candidate = None
				if hasattr(inst, "get"):
					candidate = inst.get("item", None)
					if candidate is None:
						vp = inst.get("viewParams", None)
						if hasattr(vp, "get"):
							candidate = vp.get("item", None)

				if candidate is not None:
					if isinstance(candidate, (list, tuple)):
						for it in candidate:
							_appendItem(it, items)
					else:
						_appendItem(candidate, items)
	except Exception:
		pass
	return items


def _gatherItems(component):
	"""Recursively collect custom.item from a component tree."""
	items = []

	# Collect custom.item from current component
	try:
		if hasattr(component, "custom") and hasattr(component.custom, "item"):
			_appendItem(component.custom.item, items)
	except Exception:
		pass

	# Collect from Flex Repeater instances (skip children to avoid duplicates)
	if hasattr(component, "props") and hasattr(component.props, "instances"):
		items.extend(_gatherFromInstances(component))
		return items

	# Recurse into children
	try:
		for child in component.getChildren():
			items.extend(_gatherItems(child))
	except Exception:
		pass

	return items


def _getLastRegisterCode(workstationNodeID, papoID, dbConnection):
	"""Get the last RegisterCode for a workstation/papo combination."""
	query = """
		SELECT TOP 1 RegisterCode
		FROM registerhistory
		WHERE WorkstationNodeID = ? AND PapoID = ?
		ORDER BY ID DESC
	"""
	rs = system.db.runPrepQuery(query, [workstationNodeID, papoID], dbConnection)
	lastCode = rs.getValueAt(0, 0) if rs.getRowCount() > 0 else 0
	return int(lastCode) if lastCode is not None else 0


def _countFlexGroups(root):
	"""Count FlexContainerGroup children of root dynamically."""
	count = 0
	for child in root.getChildren():
		name = child.meta.name
		if name.startswith("FlexContainerGroup") and name != "FlexContainerSupervisor":
			count += 1
	return count


# ==================== PUBLIC FUNCTIONS ====================

def recopile(flexContainer, root):
	"""
	Collect all answers from a FlexContainer recursively.

	Args:
		flexContainer (Component): The container to traverse
		root (Component): The root component (for view.custom access)

	Returns:
		dict: {"items": [{papoItemID, registerTypeID, answer}, ...]}
	"""
	allItems = _gatherItems(flexContainer)

	# Append insights metadata as last item
	insightText = getattr(root.view.custom, "insights", None)
	registerType = getattr(root.view.custom, "registerTypeID", None)
	user = getattr(root.view.custom, "user", None)
	now = system.date.now()

	if insightText is not None:
		allItems.append({
			"user": user,
			"timestamp": str(now),
			"insights": insightText,
			"registerTypeID": registerType
		})

	return {"items": allItems}


def save(root):
	"""
	Collect answers from all FlexContainerGroups and save a single
	record to registerhistory. Works for both start and end forms.

	Args:
		root (Component): The root component

	Returns:
		None
	"""
	try:
		# Input variables
		dbConnection = root.view.custom.dbConnection
		ref = str(getattr(root.view.custom, "referencePapo", "papo_core.register"))
		logger = system.util.getLogger(ref)
		papoID = root.view.params.papoID
		userName = root.session.props.auth.user.userName
		firstName = root.session.props.auth.user.get("firstName", "")
		lastName = root.session.props.auth.user.get("lastName", "")
		user = "{} {}".format(firstName, lastName).strip() if firstName or lastName else userName
		workstationNodeID = root.view.params.workstationnodeID
		workstationID = root.view.params.workstationID
		nodeID = root.view.params.nodeID
		status = "En proceso"
		now = system.date.now()

		flexGroupCount = _countFlexGroups(root)
		regCode = _getLastRegisterCode(workstationNodeID, papoID, dbConnection)

		# Collect all items from all groups
		allItems = []
		for groupIndex in range(1, flexGroupCount + 1):
			flexGroup = root.getChild("FlexContainerGroup{}".format(groupIndex))
			answersObj = recopile(flexGroup, root)

			items = answersObj.get("items", []) if answersObj else []
			if not items:
				continue

			# Keep only actual answers with papoItemID
			for item in items:
				if isinstance(item, dict) and "papoItemID" in item:
					allItems.append(item)

		# Skip only when the form has sections AND no answers were collected
		if flexGroupCount > 0 and not allItems:
			return

		# Append supervisor answer if present
		supervisorContainer = root.getChild("FlexContainerSupervisor")
		if supervisorContainer is not None:
			supervisorAnswers = recopile(supervisorContainer, root)
			if supervisorAnswers is not None:
				supervisorItems = supervisorAnswers.get("items", [])
				if supervisorItems:
					allItems.append(dict(supervisorItems[0]))

		# Get registerTypeID from view custom
		registerTypeID = int(root.view.custom.registerTypeID)

		# Get insights from view custom
		insightText = root.view.custom.insights if hasattr(root.view.custom, "insights") else ""

		# Append metadata as last item
		allItems.append({
			"insights": insightText,
			"registerTypeID": registerTypeID,
			"user": user,
			"timestamp": str(now)
		})

		# Build final JSON and insert
		answersJson = {"items": allItems}
		dataAnswerStr = String(system.util.jsonEncode(answersJson))

		insertSql = """
			INSERT INTO registerhistory (
				[Timestamp], DataAnswer, Status, PapoID, RegisterTypeID,
				[User], WorkstationNodeID, NodeID, WorkstationID, RegisterCode
			)
			VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
		"""
		params = [
			now, dataAnswerStr, status, papoID, registerTypeID,
			user, workstationNodeID, nodeID, workstationID, regCode
		]
		system.db.runPrepUpdate(insertSql, params, dbConnection)

		# UI refresh
		system.perspective.sendMessage("refreshTable", {"estado": True}, scope="session")
		system.perspective.sendMessage("closeEmbeded", {"estado": False}, scope="session")
		system.perspective.sendMessage("refreshPeriodic", {"min": 0}, scope="session")
		system.perspective.sendMessage("refreshPreviewTable", payload=[], scope="session")

	except Exception as e:
		system.util.getLogger("papo_core.register").error("Error saving form data: " + str(e))