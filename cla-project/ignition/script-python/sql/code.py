def line(db='papo_db'):
	logger = system.util.getLogger("line")

	query = '''
			SELECT
				ID,
				Name
			FROM
				node
			WHERE 
				Type = 'LINE'
			ORDER BY ID DESC
			'''
	try:
		result = system.db.runQuery(query, database=db)
		return result
	except Exception as e:
		logger.error("Error en line(): %s" % str(e))
		return None


def workStationByNode(nodeId, db='papo_db'):
	logger = system.util.getLogger("workStationByNode")

	query = '''
			SELECT 
			    w.ID,
			    w.Description
			FROM 
			    node n
			INNER JOIN workstationnode wn ON wn.NodeID = n.ID
			INNER JOIN workstation w ON w.ID = wn.WorkstationID
			WHERE n.ID = ?
			ORDER BY w.ID DESC
			'''
	try:
		result = system.db.runPrepQuery(query, args=[nodeId], database=db)
		return result
	except Exception as e:
		logger.error("Error en workStationByNode(nodeId=%s): %s" % (str(nodeId), str(e)))
		return None


def papoByNode(nodeId=None, db='papo_db'):
	import system.util
	logger = system.util.getLogger("papoByNode")

	try:
		if nodeId is None or nodeId == "":  
			# Si nodeId es None o vacío, traer todos los formularios
			query = '''
					SELECT 
						p.ID,
						p.Reference
					FROM 
						papo p
					ORDER BY p.ID DESC
					'''
			result = system.db.runQuery(query, database=db)
		else:
			# Si hay nodeId válido, traer solo los relacionados
			query = '''
					SELECT 
						p.ID,
						p.Reference
					FROM 
						node n
					INNER JOIN papo p ON p.NodeID = n.ID
					WHERE n.ID = ?
					ORDER BY p.ID DESC
					'''
			result = system.db.runPrepQuery(query, args=[nodeId], database=db)

		return result

	except Exception as e:
		logger.error("Error en papoByNode(nodeId=%s): %s" % (str(nodeId), str(e)))
		return None