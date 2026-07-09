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
			ORDER BY Name ASC
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
            FROM nodepapo np
            INNER JOIN papo p ON p.ID = np.PapoID
            INNER JOIN node n ON n.ID = np.NodeID
            WHERE n.ID = ?
            ORDER BY p.ID DESC
        '''
        
        result = system.db.runPrepQuery(query, [nodeId], database=db)
        return result

    except Exception as e:
        logger.error("Error en papoByNode(nodeId=%s): %s" % (str(nodeId), str(e)))
        return None



def getRegisterHistory(nodeId=None, papoId=None, startDate=None, endDate=None, db='papo_db'):
    """
    Recupera el último registro válido (Status != 'Sin Iniciar') 
    para cada combinación (NodeID, PapoID, RegisterCode) desde registerhistory,
    incluyendo StartTime (último Timestamp del tipo RegisterTypeID=7 de la misma combinación,
    anterior o igual al registro actual).
    """
    logger = system.util.getLogger("getRegisterHistory")

    # Normalización de parámetros
    nodeId = None if not nodeId else nodeId
    papoId = None if not papoId else papoId
    startDate = None if not startDate else startDate
    endDate = None if not endDate else endDate

    try:
        query = """
            -- Últimos registros válidos por combinación
            WITH ranked AS (
                SELECT 
                	--Script SQL
                    rh.ID as RegisterID,
                    rh.Timestamp,
                    rh.Status,
                    rh.[User],
                    rh.DataAnswer,
                    rh.RegisterTypeID,
                    rh.RegisterCode,
                    rh.NodeID,
                    rh.PapoID,
                    rh.WorkstationNodeID,
                    rh.WorkstationID,
                    n.Name AS NodeName,
                    n.DisplayName AS NodeDisplayName,
                    n.Topic AS Path,
                    p.Reference AS PapoReference,
                    p.Description AS PapoDescription,
                    w.Description AS WorkstationDescription,
                    
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
            ),

            -- Registros de inicio de turno (tipo 7)
            start_records AS (
                SELECT 
                    rh.NodeID,
                    rh.PapoID,
                    rh.RegisterCode,
                    rh.Timestamp AS StartTime
                FROM registerhistory rh
                WHERE rh.RegisterTypeID = 7
            ),

            -- Emparejar cada registro con su StartTime (máximo previo o igual)
            joined_start AS (
                SELECT 
                    r.RegisterID,
                    MAX(s.StartTime) AS StartTime
                FROM ranked r
                LEFT JOIN start_records s
                  ON r.NodeID = s.NodeID
                 AND r.PapoID = s.PapoID
                 AND r.RegisterCode = s.RegisterCode
                 AND s.StartTime <= r.Timestamp
                GROUP BY r.RegisterID
            )

            SELECT 
                r.RegisterID,
                r.Timestamp,
                r.Status,
                r.[User],
                r.DataAnswer,
                r.RegisterTypeID,
                r.RegisterCode,
                r.NodeID,
                r.NodeName,
                r.NodeDisplayName,
                r.Path,
                r.PapoID,
                r.PapoReference,
                r.PapoDescription,
                r.WorkstationNodeID,
                r.WorkstationID,
                r.WorkstationDescription,
                j.StartTime
            FROM ranked r
            LEFT JOIN joined_start j ON r.RegisterID = j.RegisterID
            WHERE r.rn = 1
              AND r.Status != 'Sin Iniciar'
            ORDER BY r.Timestamp DESC
        """

        args = [
            nodeId, nodeId,
            papoId, papoId,
            startDate, startDate,
            endDate, endDate
        ]

        result = system.db.runPrepQuery(query, args, database=db)
        return result

    except Exception as e:
        logger.error(
            "Error en getRegisterHistory(nodeId=%s, papoId=%s, startDate=%s, endDate=%s): %s" %
            (str(nodeId), str(papoId), str(startDate), str(endDate), str(e))
        )
        return None
def lineAll(db='papo_db'):
	"""
	Get all lines without filtering by area.
	
	Args:
		db (str): Database connection name.
	
	Returns:
		Dataset: All lines with ID and Name columns.
	"""
	logger = system.util.getLogger("sql/lineAll")
	
	query = '''
		SELECT
			ID,
			Name
		FROM
			node
		WHERE 
			Type = 'LINE'
		ORDER BY Name ASC
	'''
	
	try:
		result = system.db.runQuery(query, database=db)
		return result
	except Exception as e:
		logger.error("Error in lineAll(): %s" % str(e))
		return None


def papoAll(db='papo_db'):
	"""
	Get all papos (forms) without filtering.
	
	Args:
		db (str): Database connection name.
	
	Returns:
		Dataset: All papos with ID and Reference columns.
	"""
	logger = system.util.getLogger("sql/papoAll")
	
	query = '''
		SELECT DISTINCT
			p.ID,
			p.Reference
		FROM
			papo p
		INNER JOIN nodepapo np ON p.ID = np.PapoID
		ORDER BY p.Reference ASC
	'''
	
	try:
		result = system.db.runQuery(query, database=db)
		return result
	except Exception as e:
		logger.error("Error in papoAll(): %s" % str(e))
		return None


def papoByArea(areaId, db='papo_db'):
	"""
	Get all papos (forms) associated with lines under a specific area.
	
	Args:
		areaId (int): The area node ID.
		db (str): Database connection name.
	
	Returns:
		Dataset: Papos with ID and Reference columns.
	"""
	logger = system.util.getLogger("sql/papoByArea")
	
	query = '''
		SELECT DISTINCT
			p.ID,
			p.Reference
		FROM
			papo p
		INNER JOIN nodepapo np ON p.ID = np.PapoID
		INNER JOIN node n ON n.ID = np.NodeID
		WHERE
			n.ParentNodeID = ?
		ORDER BY p.Reference ASC
	'''
	
	try:
		result = system.db.runPrepQuery(query, [areaId], database=db)
		return result
	except Exception as e:
		logger.error("Error in papoByArea(areaId=%s): %s" % (str(areaId), str(e)))
		return None