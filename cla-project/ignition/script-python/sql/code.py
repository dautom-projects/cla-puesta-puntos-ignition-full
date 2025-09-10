def area(db='papo_db'):
	logger = system.util.getLogger("line")

	query = '''
			SELECT
				ID,
				Name
			FROM
				node
			WHERE 
				Type = 'AREA'
			ORDER BY ID DESC
			'''
	try:
		result = system.db.runQuery(query, database=db)
		return result
	except Exception as e:
		logger.error("Error en line(): %s" % str(e))
		return None

def line(nodeId , db='papo_db'):
	logger = system.util.getLogger("line")

	query = '''
			SELECT
				ID,
				Name
			FROM
				node
			WHERE 
				ParentNodeID = ?
			ORDER BY ID DESC
			'''
	try:
		args = [nodeId]
		result = system.db.runPrepQuery(query, args, database=db)
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
	logger = system.util.getLogger("papoByNode")

	try:
		
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

def getRegisterHistory(nodeId=None, papoId=None, startDate=None, endDate=None, db='papo_db'):
    logger = system.util.getLogger("getRegisterHistory")
    
    # Normalizamos vacíos a None
    if nodeId == '' or nodeId is None:
        nodeId = None
    if papoId == '' or papoId is None:
        papoId = None
    if startDate == '' or startDate is None:
        startDate = None
    if endDate == '' or endDate is None:
        endDate = None
    
    try:
        query = '''
            WITH ranked AS (
                SELECT 
                    rh.Status,
                    rh.[User],
                    rh.Timestamp,
                    n.Name AS NodeName,
                    p.Reference AS PapoReference,
                    p.Description AS PapoDescription,
                    w.Description AS WorkstationDescription,
                    rh.RegisterCode,
                    rh.NodeID,
                    rh.PapoID,
                    ROW_NUMBER() OVER (
                        PARTITION BY rh.NodeID, rh.PapoID, rh.RegisterCode
                        ORDER BY rh.Timestamp DESC
                    ) AS rn
                FROM registerhistory rh
                INNER JOIN node n ON n.ID = rh.NodeID
                INNER JOIN papo p ON p.ID = rh.PapoID
                INNER JOIN workstation w ON w.ID = rh.WorkstationID
                WHERE ( (? IS NULL OR n.ID = ?) )
                  AND ( (? IS NULL OR p.ID = ?) )
                  AND ( (? IS NULL OR rh.Timestamp >= ?) )
                  AND ( (? IS NULL OR rh.Timestamp <= ?) )
            )
            SELECT 
                Status,
                [User],
                Timestamp,
                NodeName,
                PapoReference,
                PapoDescription,
                WorkstationDescription,
                RegisterCode,
                NodeID,
                PapoID
            FROM ranked
            WHERE rn = 1
            ORDER BY NodeID, PapoID, RegisterCode
        '''
        
        args = [nodeId, nodeId, papoId, papoId, startDate, startDate, endDate, endDate]
        result = system.db.runPrepQuery(query, args, database=db)
        return result

    except Exception as e:
        logger.error("Error en getRegisterHistory(nodeId=%s, papoId=%s, startDate=%s, endDate=%s): %s" % 
                     (str(nodeId), str(papoId), str(startDate), str(endDate), str(e)))
        return None