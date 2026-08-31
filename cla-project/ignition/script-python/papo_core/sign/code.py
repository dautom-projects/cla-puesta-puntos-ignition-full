"""
papo_core.sign

Supervisor signature logic for PAPO forms.
Handles direct signing, authentication popup flow, and
IP validation by role.

Version: 1.2.0

Changelog:
	2026-07-30 | William M. | v1.2.0 - Added signSupervisorFromSelection for
		management/audit tables (e.g. Gestion) that sign a selected
		registerhistory row instead of the PAPO's own form view
	2026-07-23 | William M. | v1.1.1 - Fix autoCloseOpenForms picking a stale
		row when RegisterCode repeats for the same PapoID/WorkstationNodeID
		(pre-existing historical duplicates); added Timestamp/ID tiebreak
	2026-07-23 | William M. | v1.1.0 - Added autoCloseOpenForms for
		Gateway-driven shift-end auto-close of forms left "En proceso"
	2026-07-06 | William | v1.0.0 - Initial Project Library version
"""

ALLOWED_ROLES = {"INTEGRADOR", "Administrator", "Supervisor_PAPO"}
IP_EXEMPT_ROLES = {"INTEGRADOR", "Administrator"}

# Nodes excluded from shift-end auto-close (forms that intentionally span shifts)
AUTO_CLOSE_EXCLUDED_NODE_ID = 29  # Granja de acidos
AUTO_CLOSE_EXCLUDED_PARENT_NODE_ID = 4  # Metalurgia area - covers all its lines


# ==================== INTERNAL HELPERS ====================

def _normalizeIp(ip):
	"""Normalize IPv6-mapped addresses to IPv4."""
	if ip and ip.startswith("::ffff:"):
		return ip.split(":")[-1]
	return (ip or "").strip()


def _getClientIp(session):
	"""Get the current session's client IP address."""
	sessionId = session.props.id
	sessionInfoList = system.perspective.getSessionInfo()
	sessionInfo = next((s for s in sessionInfoList if s.get("id") == sessionId), {})
	return _normalizeIp(sessionInfo.get("clientAddress", ""))


def _validateWorkstationIp(session, allowedIp):
	"""Return True if the client IP matches the allowed workstation IP."""
	clientIp = _getClientIp(session)
	return clientIp == str(allowedIp).strip()


def _insertSignature(dbConnection, dataAnswerStr, papoId, userName, workstationNodeId, nodeId, workstationId, registerCode):
	"""Insert a supervisor signature record (type 10, Revisado)."""
	sql = """
		INSERT INTO registerhistory 
		(Timestamp, DataAnswer, Status, PapoID, RegisterTypeID, [User], 
		 WorkstationNodeID, NodeID, WorkstationID, RegisterCode)
		VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?, ?, ?, ?)
	"""
	args = [
		dataAnswerStr, "Revisado", papoId, 10, userName,
		workstationNodeId, nodeId, workstationId, registerCode
	]
	system.db.runPrepUpdate(sql, args, dbConnection)


# ==================== PUBLIC FUNCTIONS ====================

def supervisorOpt(root):
	"""
	Get list of supervisor full names for dropdown population.

	Filters users with the Supervisor_PAPO role and returns their
	full names (firstName + lastName), sorted alphabetically.

	Args:
		root (Component): The root component (for session access)

	Returns:
		list: Sorted list of supervisor full names
	"""
	logger = system.util.getLogger("papo_core.sign")

	try:
		targetRole = "Supervisor_PAPO"
		userSource = root.session.custom.userSource

		allUsers = system.user.getUsers(userSource)
		supervisorList = []

		for user in allUsers:
			username = user.get("Username")
			userRoles = user.getRoles()

			if targetRole in userRoles:
				firstName = user.get("FirstName")
				lastName = user.get("LastName")

				if firstName and lastName:
					fullName = "{} {}".format(firstName, lastName)
				elif firstName:
					fullName = firstName
				elif lastName:
					fullName = lastName
				else:
					fullName = username

				supervisorList.append(fullName)

		supervisorList.sort()
		return supervisorList

	except Exception as e:
		logger.error("Error populating supervisor dropdown: " + str(e))
		return []


def signOperator(root):
	"""
	Finalize current form cycle and create next Idle record.

	Inserts operator signature (type 10, Finalizado) + new Idle
	(type 12, RegisterCode + 1, Sin Iniciar) to start next cycle.

	Args:
		root (Component): The root component

	Returns:
		None
	"""
	try:
		dbConnection = root.view.custom.dbConnection
		ref = str(getattr(root.view.custom, "referencePapo", "papo_core.sign"))
		logger = system.util.getLogger(ref)
		papoID = root.view.params.papoID
		user = root.session.props.auth.user.userName
		workstationNodeID = root.view.params.workstationnodeID
		workstationID = root.view.params.workstationID
		nodeID = root.view.params.nodeID
		now = system.date.now()

		# Get current RegisterCode (highest, not most recent by time)
		queryLastCode = """
			SELECT TOP 1 RegisterCode
			FROM registerhistory
			WHERE WorkstationNodeID = ? AND PapoID = ?
			ORDER BY RegisterCode DESC
		"""
		result = system.db.runPrepQuery(queryLastCode, [workstationNodeID, papoID], dbConnection)
		regCode = result.getValueAt(0, 0) if result.getRowCount() > 0 else 0
		if regCode is None:
			regCode = 0

		def insertRecord(registerTypeID, answerJson, registerCode, status):
			"""Insert a single record into registerhistory."""
			insertSql = """
				INSERT INTO registerhistory (
					[Timestamp], DataAnswer, Status, PapoID, RegisterTypeID,
					[User], WorkstationNodeID, NodeID, WorkstationID, RegisterCode
				)
				VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
			"""
			params = [
				now, answerJson, status, papoID, registerTypeID,
				user, workstationNodeID, nodeID, workstationID, registerCode
			]
			system.db.runPrepUpdate(insertSql, params, dbConnection)

		# Sign (Finalizado) + new Idle (Sin Iniciar)
		regPayload = root.view.custom.sign
		insertRecord(10, system.util.jsonEncode(regPayload), regCode, "Finalizado")
		insertRecord(12, "{}", regCode + 1, "Sin Iniciar")

		# UI refresh
		system.perspective.sendMessage("refreshPeriodic", {"min": 0}, scope="session")
		system.perspective.sendMessage("refreshPreviewTable", payload=[], scope="session")

	except Exception as e:
		system.util.getLogger("papo_core.sign").error("Error in operator signature: " + str(e))


def requestSupervisorAuth(button):
	"""
	Entry point for the Firma Supervisor button.

	Validates status, then either signs directly (if current user
	has a supervisor role) or opens the authentication popup.
	IP is validated only for Supervisor_PAPO on direct signing.

	Args:
		button (Component): The Firma Supervisor button component

	Returns:
		None
	"""
	try:
		dbConnection = button.view.custom.dbConnection
		ref = str(getattr(button.view.custom, "referencePapo", "papo_core.sign"))
		logger = system.util.getLogger(ref)
		papoId = button.view.params.papoID
		nodeId = button.view.params.nodeID
		workstationId = button.view.params.workstationID
		workstationNodeId = button.view.params.workstationnodeID

		# Get current status, register code and allowed IP
		statusQuery = """
			SELECT TOP (1) rh.[Status], rh.RegisterCode, ws.IpAddress
			FROM registerhistory rh
			JOIN workstation ws ON ws.ID = rh.WorkstationID
			WHERE rh.WorkstationNodeID = ? AND rh.PapoID = ?
			ORDER BY rh.RegisterCode DESC, rh.[Timestamp] DESC
		"""
		statusResult = system.db.runPrepQuery(statusQuery, [workstationNodeId, papoId], dbConnection)

		if statusResult.getRowCount() == 0:
			alerts.noValidOption('No se encontro registro para este formulario')
			return

		currentStatus = statusResult.getValueAt(0, "Status")
		registerCode = statusResult.getValueAt(0, "RegisterCode")
		allowedIp = str(statusResult.getValueAt(0, "IpAddress")).strip()

		# Validate form not already signed
		if currentStatus in ('Revisado', 'Finalizado'):
			alerts.noValidOption('El formulario ya esta firmado')
			return

		# Check current user roles
		currentUserRoles = set(button.session.props.auth.user.roles)
		currentRolesUpper = set([r.upper() for r in currentUserRoles])
		allowedRolesUpper = set([r.upper() for r in ALLOWED_ROLES])
		hasRequiredRole = bool(currentRolesUpper & allowedRolesUpper)

		if hasRequiredRole:
			# Direct sign - validate IP only for Supervisor_PAPO
			isIpExempt = bool(currentUserRoles & IP_EXEMPT_ROLES)

			if not isIpExempt:
				if not _validateWorkstationIp(button.session, allowedIp):
					alerts.noValidOption('No se encuentra en la estacion de trabajo correspondiente para firmar este formulario')
					return

			alerts.showAlert(
				state="warning",
				title="Firmar PAPO",
				message="Esta seguro de que desea firmar el puesta a punto?",
				btnTextPrimary="Si",
				btnTextSecondary="No",
				btnActionPrimary="signSuper"
			)
		else:
			# Open authentication popup
			payload = {
				"papoId": papoId,
				"nodeId": nodeId,
				"registerCode": registerCode,
				"workstationNodeId": workstationNodeId,
				"workstationId": workstationId,
				"dbConnection": dbConnection,
				"pageId": button.page.id,
				"reference": button.view.custom.referencePapo
			}
			system.perspective.openPopup(
				id="supervisorAuthPopup",
				view="Page/PopUps/Authenticator",
				params=payload,
				showCloseIcon=False,
				draggable=False,
				modal=True,
				overlayDismiss=False,
				position={'position': 'center'}
			)

	except Exception as e:
		system.util.getLogger("papo_core.sign").error("Error in supervisor signature flow: " + str(e))


def signSupervisor(root):
	"""
	Execute direct supervisor signature (current logged-in user).

	Args:
		root (Component): The root component

	Returns:
		None
	"""
	try:
		papoId = root.view.params.papoID
		reference = root.view.custom.referencePapo
		logger = system.util.getLogger(reference)
		nodeId = root.view.params.nodeID
		registerCode = root.view.custom.registerCode
		workstationNodeId = root.view.params.workstationnodeID
		workstationId = root.view.params.workstationID
		dbConnection = root.view.custom.dbConnection

		userName = root.view.custom.sign.user
		roleList = root.view.custom.sign.role
		name = root.view.custom.sign.name
		lastname = root.view.custom.sign.lastname

		role = str(roleList[0]) if isinstance(roleList, list) and roleList else (str(roleList) if roleList else '')
		nameStr = str(name) if name is not None else ''
		lastnameStr = str(lastname) if lastname is not None else ''

		dataAnswer = {
			"user": userName,
			"role": role,
			"name": nameStr,
			"lastname": lastnameStr
		}
		dataAnswerStr = system.util.jsonEncode(dataAnswer)

		_insertSignature(dbConnection, dataAnswerStr, papoId, userName,
		                 workstationNodeId, nodeId, workstationId, registerCode)

		fullName = (nameStr + ' ' + lastnameStr).strip() or userName
		alerts.actionSuccess(
			title='Firma Exitosa',
			message='El formulario ' + str(reference) + ' ha sido firmado correctamente por ' + fullName
		)

	except Exception as e:
		system.util.getLogger("papo_core.sign").error("Error in supervisor sign: " + str(e))


def signSupervisorFromSelection(root):
	"""
	Sign the currently selected row from a PAPO management table.

	Inserts a supervisor signature (type 10, Revisado) for the row
	selected in a Table component (root.view.custom.selection), using
	the logged-in user's identity. Meant for management/audit views
	(e.g. Gestion) where the user reviews a historical row instead of
	working inside the PAPO's own form view.

	Args:
		root (Component): The root component

	Returns:
		None
	"""
	try:
		dbConnection = root.view.custom.dbConnection
		selection = root.view.custom.selection

		papoId = selection.PapoID
		nodeId = selection.NodeID
		registerCode = selection.RegisterCode
		workstationNodeId = selection.WorkstationNodeID
		workstationId = selection.WorkstationID

		userName = root.session.props.auth.user.userName
		firstName = root.session.props.auth.user.firstName
		lastName = root.session.props.auth.user.lastName
		roles = root.session.props.auth.user.roles

		dataAnswer = {
			"user": userName,
			"role": list(roles),
			"name": firstName,
			"lastname": lastName
		}
		dataAnswerStr = system.util.jsonEncode(dataAnswer)

		_insertSignature(dbConnection, dataAnswerStr, papoId, userName,
		                 workstationNodeId, nodeId, workstationId, registerCode)

		alerts.actionSuccess('Formulario firmado', message='El formulario fue firmado correctamente')
		root.view.custom.refreshTable = root.view.custom.refreshTable + 1

	except Exception as e:
		system.util.getLogger("papo_core.sign").error("Error in supervisor sign from selection: " + str(e))


def authenticateAndSign(popup):
	"""
	Authenticate a supervisor via popup and execute signature.

	Validates credentials and role, then validates workstation IP
	for Supervisor_PAPO (Administrator/INTEGRADOR skip IP), then signs.

	Args:
		popup (Component): The popup AceptButton component

	Returns:
		None
	"""
	try:
		ref = getattr(popup.view.params, "reference", "papo_core.sign")
		logger = system.util.getLogger(ref)
		userName = popup.view.custom.user
		password = popup.view.custom.password

		if not userName or not password:
			alerts.showAlert(state='warning', title='Campos Requeridos',
			                 message='Ingrese usuario y contrasena',
			                 btnTextPrimary='Aceptar', btnActionPrimary='')
			return

		# Authenticate
		if not system.security.validateUser(userName, password):
			alerts.showAlert(state='error', title='Error de Autenticacion',
			                 message='Usuario o contrasena incorrectos',
			                 btnTextPrimary='Aceptar', btnActionPrimary='')
			return

		# Get user roles
		userSource = popup.session.custom.userSource
		try:
			userInfo = system.user.getUser(userSource, userName)
			userRoles = list(userInfo.getRoles())
		except Exception as e:
			logger.error("Failed to get roles: " + str(e))
			userRoles = []

		# Validate allowed roles
		userRolesUpper = set([r.upper() for r in userRoles])
		allowedRolesUpper = set([r.upper() for r in ALLOWED_ROLES])

		if not (userRolesUpper & allowedRolesUpper):
			alerts.showAlert(state='error', title='Acceso Denegado',
			                 message='El usuario ' + str(userName) + ' no cuenta con los permisos para firmar',
			                 btnTextPrimary='Aceptar', btnActionPrimary='')
			return

		# Validate IP for Supervisor_PAPO only
		isIpExempt = bool(set(userRoles) & IP_EXEMPT_ROLES)

		if not isIpExempt:
			dbConnection = popup.view.params.dbConnection
			workstationId = popup.view.params.workstationId

			ipQuery = "SELECT IpAddress FROM workstation WHERE ID = ?"
			ipResult = system.db.runPrepQuery(ipQuery, [workstationId], dbConnection)
			allowedIp = str(ipResult.getValueAt(0, 0)).strip() if ipResult.getRowCount() > 0 else ""

			if not _validateWorkstationIp(popup.session, allowedIp):
				alerts.showAlert(state='error', title='Estacion no valida',
				                 message='No se encuentra en la estacion de trabajo correspondiente para firmar este formulario',
				                 btnTextPrimary='Aceptar', btnActionPrimary='')
				return

		# Get user details
		try:
			firstName = userInfo.get("firstname") or ""
			lastName = userInfo.get("lastname") or ""
		except Exception:
			firstName = ""
			lastName = ""

		# Build and insert signature
		dataAnswer = {
			"user": userName,
			"role": userRoles,
			"name": firstName,
			"lastname": lastName
		}
		dataAnswerStr = system.util.jsonEncode(dataAnswer)

		papoId = popup.view.params.papoId
		nodeId = popup.view.params.nodeId
		registerCode = popup.view.params.registerCode
		workstationNodeId = popup.view.params.workstationNodeId
		workstationId = popup.view.params.workstationId
		dbConnection = popup.view.params.dbConnection
		reference = popup.view.params.reference

		_insertSignature(dbConnection, dataAnswerStr, papoId, userName,
		                 workstationNodeId, nodeId, workstationId, registerCode)

		fullName = (str(firstName) + ' ' + str(lastName)).strip() or userName
		alerts.actionSuccess(
			title='Firma Exitosa',
			message='El formulario ' + str(reference) + ' ha sido firmado correctamente por ' + fullName
		)
		system.perspective.closePopup("supervisorAuthPopup")

	except Exception as e:
		system.util.getLogger("papo_core.sign").error("Error in supervisor authentication: " + str(e))
		alerts.showAlert(state='error', title='Error del Sistema',
		                 message='Ocurrio un error inesperado. Contacte al administrador.',
		                 btnTextPrimary='Aceptar', btnActionPrimary='')


def autoCloseOpenForms(dbConnection):
	"""
	Auto-close PAPO forms left "En proceso" past the shift boundary.

	Meant to run from a Gateway Timer/Scheduled Script shortly after each
	shift change (06:10, 14:10, 22:10). Finds the latest registerhistory
	row per PapoID/WorkstationNodeID pair still in "En proceso", then
	inserts the same closing pair signOperator() would (type 10 Finalizado
	+ type 12 Sin Iniciar, RegisterCode + 1), attributing the closure to
	the operator recorded on that last save and tagging the signature
	comment with turno/hora plus "Cierre automatico". Forms under Granja
	de acidos or any Metalurgia line are skipped since they intentionally
	span multiple shifts.

	Args:
		dbConnection (str): Database connection name.

	Returns:
		int: Number of forms auto-closed.
	"""
	try:
		logger = system.util.getLogger("papo_core.sign.autoCloseOpenForms")
		now = system.date.now()

		# Build turno/hora prefix for the closing comment
		hour = system.date.getHour24(now)
		minute = system.date.getMinute(now)

		if hour >= 22 or hour < 6:
			shift = 1
		elif hour >= 6 and hour < 14:
			shift = 2
		else:
			shift = 3

		timeStr = "{:02d}:{:02d}".format(hour, minute)
		comment = "T: {}, H: {} - Cierre automatico".format(shift, timeStr)

		# Get node IDs excluded from auto-close (Granja de acidos + Metalurgia lines)
		excludedQuery = "SELECT ID FROM node WHERE ID = ? OR ParentNodeID = ?"
		excludedResult = system.db.runPrepQuery(
			excludedQuery,
			[AUTO_CLOSE_EXCLUDED_NODE_ID, AUTO_CLOSE_EXCLUDED_PARENT_NODE_ID],
			dbConnection
		)
		excludedNodeIds = set(
			int(excludedResult.getValueAt(i, 0)) for i in range(excludedResult.getRowCount())
		)

		# Get the latest register per PapoID/WorkstationNodeID still "En proceso"
		# Tiebreak by Timestamp then ID: historical RegisterCode duplicates exist
		# for some stations (pre-dating the signOperator RegisterCode fix), so
		# RegisterCode alone is not always unique per PapoID/WorkstationNodeID
		openQuery = """
			SELECT PapoID, WorkstationNodeID, NodeID, WorkstationID, RegisterCode, [User]
			FROM (
				SELECT
					PapoID, WorkstationNodeID, NodeID, WorkstationID, RegisterCode, [User], Status,
					ROW_NUMBER() OVER (
						PARTITION BY PapoID, WorkstationNodeID
						ORDER BY RegisterCode DESC, [Timestamp] DESC, ID DESC
					) AS rn
				FROM registerhistory
			) latest
			WHERE rn = 1 AND Status = ?
		"""
		openResult = system.db.runPrepQuery(openQuery, ["En proceso"], dbConnection)

		insertSql = """
			INSERT INTO registerhistory (
				[Timestamp], DataAnswer, Status, PapoID, RegisterTypeID,
				[User], WorkstationNodeID, NodeID, WorkstationID, RegisterCode
			)
			VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
		"""

		closedCount = 0
		for i in range(openResult.getRowCount()):
			papoID = openResult.getValueAt(i, "PapoID")
			workstationNodeID = openResult.getValueAt(i, "WorkstationNodeID")
			nodeID = openResult.getValueAt(i, "NodeID")
			workstationID = openResult.getValueAt(i, "WorkstationID")
			regCode = int(openResult.getValueAt(i, "RegisterCode"))
			lastUser = openResult.getValueAt(i, "User")

			if workstationNodeID is None or int(workstationNodeID) in excludedNodeIds:
				continue

			regPayload = {
				"user": lastUser,
				"role": "SYSTEM",
				"name": "Cierre",
				"lastname": "Automatico",
				"comment": comment
			}

			system.db.runPrepUpdate(insertSql, [
				now, system.util.jsonEncode(regPayload), "Finalizado", papoID, 10,
				lastUser, workstationNodeID, nodeID, workstationID, regCode
			], dbConnection)

			system.db.runPrepUpdate(insertSql, [
				now, "{}", "Sin Iniciar", papoID, 12,
				lastUser, workstationNodeID, nodeID, workstationID, regCode + 1
			], dbConnection)

			closedCount += 1

		# logger.info("Auto-closed {} open PAPO forms at shift boundary".format(closedCount))
		return closedCount

	except Exception as e:
		system.util.getLogger("papo_core.sign").error("Error in auto-close job: " + str(e))
		return 0