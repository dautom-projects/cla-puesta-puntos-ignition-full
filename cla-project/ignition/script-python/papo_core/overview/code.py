"""
papo_core.overview

Logic for the PAPO card overview view.
Handles filtered card listing and card path building.

Version: 1.0.0

Changelog:
	2026-07-06 | William | v1.0.0 - Initial Project Library version
"""

logger = system.util.getLogger("papo_core.overview")

# Statuses visible to non-admin users
NON_ADMIN_STATUSES = ("Sin Iniciar", "En proceso", None)


def getPapoListFiltered(value):
	"""
	Filter the cached Papo list by full hierarchy and role.

	Args:
		value (dict): Contains entID, sitID, areID, linID, wksID,
		              refID, rol, paposData (JSON string)

	Returns:
		list: Filtered list of Papo dicts
	"""
	try:
		enterpriseId = value.get("entID")
		siteId = value.get("sitID")
		areaId = value.get("areID")
		lineId = value.get("linID")
		workstationId = value.get("wksID")
		refId = value.get("refID")
		rol = value.get("rol")
		cachedJson = value.get("paposData")

		# Normalize workstationId to set
		if workstationId is None:
			workstationIdSet = set()
		elif isinstance(workstationId, list):
			workstationIdSet = set(workstationId)
		else:
			workstationIdSet = set([workstationId]) if workstationId != 0 else set()

		# Non-admin without workstation sees nothing
		if rol == "false" and len(workstationIdSet) == 0:
			return []

		if cachedJson is None or cachedJson == "":
			return []

		import json
		allPapos = json.loads(cachedJson)

		filteredPapos = []
		for papo in allPapos:
			if len(workstationIdSet) > 0 and papo.get("workstationID") not in workstationIdSet:
				continue
			if enterpriseId and papo.get("enterpriseID") != enterpriseId:
				continue
			if siteId and papo.get("siteID") != siteId:
				continue
			if areaId and papo.get("areaID") != areaId:
				continue
			if lineId and papo.get("lineID") != lineId:
				continue
			if refId and papo.get("papoID") != refId:
				continue
			# Non-admin users only see Sin Iniciar / En proceso
			if rol == "false" and papo.get("status") not in NON_ADMIN_STATUSES:
				continue

			filteredPapos.append(papo)

		return filteredPapos

	except Exception as e:
		logger.error("Error filtering Papo list: " + str(e))
		return []


def getCardPath(value):
	"""
	Build the card origin path string "De: topic/workstation".

	Args:
		value (dict): Contains dbConnection, nodeID, workstationID

	Returns:
		str: Formatted path string
	"""
	try:
		dbConnection = value["dbConnection"]
		nodeID = value["nodeID"]
		workstationID = value.get("workstationID")

		query = "SELECT topic FROM node WHERE ID = ?"
		data = system.db.runPrepQuery(query, [nodeID], dbConnection)
		topic = data.getValueAt(0, 0)

		if workstationID:
			query2 = "SELECT Description FROM workstation WHERE ID = ?"
			data2 = system.db.runPrepQuery(query2, [workstationID], dbConnection)
			if data2.getRowCount() > 0:
				return "De: " + topic + "/" + data2.getValueAt(0, 0)

		return "De: " + topic

	except Exception as e:
		logger.error("Error building card path: " + str(e))
		return ""