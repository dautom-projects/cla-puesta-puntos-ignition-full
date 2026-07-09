#* DAUTOM SAS CONFIDENTIAL
#*_________________________
#*
#* [2013] - [2025] DAUTOM SAS
#* All Rights Reserved.
#*
#* NOTICE: All information contained herein is, and remains the property
#* of DAUTOM SAS and its suppliers, if any. The intellectual and 
#* technical concepts contained here in are proprietary to DAUTOM SAS
#* and its suppliers and may be covered by U.S and Foreign Patents, 
#* patents in process, and are protected by trade secret or copyright law. 
#* Dissemination of this information or reproduction of this material
#* is strictly forbidden unless prior written permission is obtained
#* from DAUTOM SAS.
"""
This script updates a run based on its ID. It retrieves relevant information 
such as NodeID and nodePath, calculates the estimated finish time of the run, 
reads tag values, and updates the run table accordingly.
"""

from mes_core.sql import SQLTableBase
import system
class RunTable(SQLTableBase):
	def __init__(self, dbConnection=None):
		columns = {
			'ID': 'int',
			'ScheduleID': 'int',
			'RunStartDateTime': 'datetime',
			'RunStopDateTime': 'datetime',
			'StartInfeed': 'int',
			'CurrentInfeed': 'int',
			'StartOutfeed': 'int',
			'CurrentOutfeed': 'int',
			'StartWaste': 'int',
			'CurrentWaste': 'int',
			'TotalCount': 'int',
			'WasteCount': 'int',
			'GoodCount': 'int',
			'Availability': 'real',
			'Performance': 'real',
			'Quality': 'real',
			'OEE': 'real',
			'SetupStartDateTime': 'datetime',
			'SetupEndDateTime': 'datetime',
			'RunTime': 'int',
			'UnplannedDowntime': 'int',
			'PlannedDowntime': 'int',
			'TotalTime': 'int',
			'TimeStamp': 'datetime',
			'Closed': 'tinyint',
			'EstimatedFinishedTime': 'datetime',
		}
		SQLTableBase.__init__(self, 'run', columns, dbConnection)

	def insert(self,
	           schedule_id,
	           run_start=None,
	           run_stop=None,
	           start_infeed=None,
	           current_infeed=None,
	           start_outfeed=None,
	           current_outfeed=None,
	           start_waste=None,
	           current_waste=None,
	           total_count=None,
	           waste_count=None,
	           good_count=None,
	           availability=None,
	           performance=None,
	           quality=None,
	           oee=None,
	           setup_start=None,
	           setup_end=None,
	           runtime=None,
	           unplanned_downtime=None,
	           planned_downtime=None,
	           total_time=None,
	           timestamp=None,
	           closed=0,
	           estimated_finished=None):
		"""
		Inserta un nuevo registro en la tabla 'run' con todos los campos.
		"""
		if timestamp is None:
			timestamp = system.date.now()
		values = {
			'ScheduleID': schedule_id,
			'RunStartDateTime': run_start,
			'RunStopDateTime': run_stop,
			'StartInfeed': start_infeed,
			'CurrentInfeed': current_infeed,
			'StartOutfeed': start_outfeed,
			'CurrentOutfeed': current_outfeed,
			'StartWaste': start_waste,
			'CurrentWaste': current_waste,
			'TotalCount': total_count,
			'WasteCount': waste_count,
			'GoodCount': good_count,
			'Availability': availability,
			'Performance': performance,
			'Quality': quality,
			'OEE': oee,
			'SetupStartDateTime': setup_start,
			'SetupEndDateTime': setup_end,
			'RunTime': runtime,
			'UnplannedDowntime': unplanned_downtime,
			'PlannedDowntime': planned_downtime,
			'TotalTime': total_time,
			'TimeStamp': timestamp,
			'Closed': closed,
			'EstimatedFinishedTime': estimated_finished,
		}
		SQLTableBase.insert(self, values)

	def selectID(self, run_id, columns=None):
		return self.select('ID = ?', [run_id], columns)

	def updateID(self, run_id, set_values):
		self.update(set_values, 'ID = ?', [run_id])

	def deleteID(self, run_id):
		self.delete('ID = ?', [run_id])

	def show(self):
		print("Tabla: run")
		print("-" * 50)
		for col_name, col_type in self.columns.items():
			print("{}: {}".format(col_name, col_type))
		print("-" * 50)

	def selectAll(self, columns=None, order_by=None, order_direction='ASC'):
		"""
		Selecciona todos los registros de standardrate con columnas opcionales y ordenamiento.
		columns: list, lista de columnas específicas a seleccionar (opcional)
		order_by: str, nombre de la columna por la cual ordenar (opcional)
		order_direction: str, dirección del ordenamiento ('ASC' o 'DESC', por defecto 'ASC')
		"""
		return SQLTableBase.selectAll(self, columns, order_by, order_direction)
	
	def selectCustom(self, columns=None, where_clause=None, where_args=None):
		"""
		Realiza una consulta SELECT personalizada sobre la tabla molde.
		columns: list, lista de columnas específicas a seleccionar (opcional, si es None selecciona todas)
		where_clause: str, condición SQL opcional (ej: 'MoldeCode = ?', 'Disable = ? AND Description LIKE ?')
		where_args: list, valores para el where_clause
		Devuelve los resultados de la consulta.
		"""
		return SQLTableBase.select(self, where_clause, where_args, columns) 

from datetime import datetime, timedelta
from java.lang import Exception

db = 'mes_core'


def startRun(scheduleID, nodeid, db=db):
	# Build a query to retrieve NodeID and nodePath
	query = """
		SELECT TOP 1
		n.ID AS NodeID,
		CONCAT('[UNS]', n.Topic, '/line') AS nodePath,
		str.StandardRate AS StandardRate,
		str.ProductCodeID,
		str.MoldID,
		sch.ScheduleFinishDateTime AS ScheduledFinishTime,
		sch.ScheduleStartDateTime AS ScheduledStartTime,
		sch.Quantity,
		m.Slot
		
	FROM schedule sch
		LEFT JOIN node n ON n.ID = sch.NodeID 
		LEFT JOIN mold m ON m.ID = sch.MoldID
		LEFT JOIN workorder wo ON wo.ID = sch.WorkOrderID
		LEFT JOIN productcode pc ON pc.ID = wo.ProductCodeID
		LEFT JOIN standardrate str 
			ON str.ProductCodeID = pc.ID 
			AND str.MoldID = sch.MoldID
			AND str.NodeID = n.ID

	WHERE sch.ID = ?

	"""
	data = system.db.runPrepQuery(query, [scheduleID], db)

	
	for row in data:
		NodeID = row['NodeID']
		nodePath = row['nodePath']
		startTime = system.date.now() #row['startTime']
		standardRate = row['StandardRate']
		scheduledFinish = row['ScheduledFinishTime']
		scheduledStart = row['ScheduledStartTime']
		quantity = row['Quantity']
		cavities = row['Slot']

	
	#tagPaths
	runIDPath =  nodePath + '/OEE/RunID'
	
	#these tags were added on 7/25 WDR to update the starttime tag and the runenabled tag
	startTimePath = nodePath + '/Start Time'
	runEnabledPath = nodePath + '/Run Enabled'
	infeedPath = nodePath + '/infeed'
	outfeedPath = nodePath + '/outfeed'
	wastePath = nodePath + '/waste'
	schedulePath = nodePath + '/OEE/Schedule ID'
	quantityPath =  nodePath + '/OEE/Quantity'
	EstimateFinishPath = nodePath + '/OEE/Estimated Finish Time'
	cavitiesPath = nodePath + '/Cavities'
	statePath =  nodePath + "/State"
	
	infeed = system.tag.readBlocking(infeedPath)[0].value #get the starting raw infeed count to insert into the db record
	outfeed = system.tag.readBlocking(outfeedPath)[0].value #get the starting raw outfeed count to insert into the db record
	waste = system.tag.readBlocking(wastePath)[0].value #get the starting raw waste count to insert into the db record
	
	print waste
	queryRun = '''
		INSERT INTO run (
			  ScheduleID,
			  EstimatedFinishedTime,
			  RunStartDateTime,
			  TimeStamp,
			  StartInfeed,
			  StartOutfeed,
			  StartWaste
		) 
		VALUES(?, ?, GETDATE(), GETDATE(), ? , ? , ? ); 
	'''
	
	estimatedMillis = system.date.millisBetween(scheduledStart, scheduledFinish)
	estimatedFinish = system.date.addMillis(startTime, estimatedMillis)
	
	argsRun = [scheduleID, estimatedFinish,infeed * cavities, outfeed * cavities, waste]
	
	querySch = '''
		UPDATE schedule
		SET 
			RunID = ?,
			RunStartDateTime = GETDATE()
		WHERE 
			ID = ?
	'''
	
	queryScada = ''' 
				SELECT WorkOrderID, Quantity
				FROM schedule 
				WHERE ID = ?
				'''
	argsScada = [scheduleID]
	
	datasetScada = system.db.runPrepQuery(queryScada, argsScada, db)
	workOrderID = datasetScada.getValueAt(0,"WorkOrderID")
	schQty = datasetScada.getValueAt(0,"Quantity")
	
	try:
		
		runID = system.db.runPrepUpdate(queryRun, argsRun, db, getKey=True) 
		
		argsSch = [runID, scheduleID]
		system.db.runPrepUpdate(querySch, argsSch, db, getKey=True) 
		
		runIDPath = nodePath + '/OEE/RunID'
		standardRatePath = nodePath + '/OEE/Standard Rate'
		
		system.tag.writeBlocking([runIDPath],[runID])#write the runID to the runID tag in the OEE udt
		system.tag.writeBlocking([startTimePath],[startTime])
		system.tag.writeBlocking([runEnabledPath],[1])
		system.tag.writeBlocking([standardRatePath],[standardRate/3600.0])
		system.tag.writeBlocking([schedulePath], [scheduleID])
		system.tag.writeBlocking([quantityPath], [quantity])
		system.tag.writeBlocking([EstimateFinishPath], [estimatedFinish])
		system.tag.writeBlocking([cavitiesPath], [cavities])
		

	
	# Creating a new insert on state history with current runID 
	
	
	
		query = """
			SELECT 
			    rn.ID AS RunID,
			    n.Name as NodeName
			FROM run rn
			INNER JOIN schedule sch 
			    ON sch.ID = rn.ScheduleID
			INNER JOIN node n 
			    ON n.ID = sch.NodeID
			WHERE n.ID = ?
			AND rn.Closed = 0;
		"""
		
		# Execute the query and return the dataset
		dataset = system.db.runPrepQuery(query, [nodeid], db)
	
	
	
		print("Query executed successfully.")
		
		runID = dataset.getValueAt(0,0)
		nodeName = dataset.getValueAt(0,1)
		
	
		
		
		
		
		
	
		tableSH = mes_core.model.statehistoryTable(db)
		tableSR = mes_core.model.statereasonTable(db)
		
		
		results = tableSH.selectCustom(columns=["TOP 1 ID"] , where_clause="NodeID=? AND EndDateTime is NULL ORDER BY StartDateTime DESC" , where_args=[nodeid]).getValueAt(0,0)
		
		tableSH.updateID(results, {"EndDateTime": system.date.now()})
		
		
		
		stateCode = system.tag.readBlocking(statePath)[0].value
		
		stateReasonID = tableSR.selectCustom(columns=["ID"], where_clause = "ReasonCode = ?", where_args=[stateCode])
		stateReasonID = stateReasonID.getValueAt(0,0)
		
		stateReasonName = tableSR.selectCustom(columns=["ReasonName"], where_clause = "ReasonCode = ?", where_args=[stateCode])
		stateReasonName = stateReasonName.getValueAt(0,0)
		
		tableSH.insert(stateReasonID , system.date.now(), stateReasonName,stateCode , runID=runID , nodeID=nodeid)
		#print "INSERTAR -> " + str(stateReasonID) + ' ' +str(system.date.now()) + ' ' +stateReasonName + ' ' +str(stateCode) + ' ' +str(runID) + ' ' +str(nodeid)
		
		
		return 1
	
	except:
		return 0
		
def getRunBynode(NodeID, db=db):
	"""
    Retrieves work order data with associated material code and other attributes like quantity, closed status, and timestamp.

    Returns:
    Dataset: The result of the query containing work order data.
    """
    # SQL query to fetch work order data and associated material code
	query = """
		SELECT TOP 1 *
		FROM (
			SELECT 
				wo.ID AS WorkOrderID,
				pc.ProductCode,
				pc.Description AS ProductCodeDescription,
				rn.RunStartDateTime,
				sch.ScheduleFinishDateTime AS ScheduleFinishDateTime,
				mld.MoldCode AS MoldeCode,
				mld.Description AS MoldeName,
				mld.Slot AS Cavities,
				str.StandardRate AS StandardRate,
				rn.ID AS RunID,
				rn.WasteCount AS Waste,
				rn.EstimatedFinishedTime,
				sch.Quantity AS Quantity,
				rn.StartOutfeed AS StartOutfeed,
				rn.CurrentOutfeed AS CurrentOutfeed,
				rn.GoodCount AS GoodCount,
				rn.TotalCount AS TotalCount,			
				n.name AS nodeName,
				
				
				ROW_NUMBER() OVER (ORDER BY rn.RunStartDateTime DESC) AS rnOrder
			FROM run rn
			INNER JOIN schedule sch 
				ON sch.ID = rn.ScheduleID
			INNER JOIN workorder wo 
				ON wo.ID = sch.WorkOrderID
			INNER JOIN productcode pc 
				ON pc.ID = wo.ProductCodeID
			INNER JOIN mold mld 
				ON mld.ID = sch.MoldID
			INNER JOIN node n 
				ON n.ID = sch.NodeID
			LEFT JOIN standardrate str 
				ON str.ProductCodeID = pc.ID 
				AND str.MoldID = mld.ID 
				AND str.NodeID = n.ID
			WHERE n.ID = ?
			AND rn.Closed != 1
		) t
		WHERE rnOrder = 1;
	"""
	
	try:
	    # Execute the query and return the dataset
	    dataset = system.db.runPrepQuery(query, [NodeID], db)
	    print("Query executed successfully.")
	    return dataset
	except Exception as e:
	    # Print an error message if the query fails
	    print("Error executing query: ", str(e))
	    return None
	    
def getRunBynode2(NodeID, db=db):
	"""
    Retrieves work order data with associated material code and other attributes like quantity, closed status, and timestamp.

    Returns:
    Dataset: The result of the query containing work order data.
    """
    # SQL query to fetch work order data and associated material code
	query = """
		SELECT TOP 1 *
		FROM (
			SELECT 
				wo.ID AS WorkOrderID,
				pc.ProductCode,
				rn.RunStartDateTime,
				rn.RunStopDateTime,
				sch.ScheduleFinishDateTime AS ScheduleFinishDateTime,
				mld.MoldCode AS MoldeCode,
				mld.Description AS MoldeName,
				str.StandardRate AS StandardRate,
				rn.ID AS RunID,
				rn.WasteCount AS Waste,
				rn.EstimatedFinishedTime,
				sch.Quantity AS Quantity,
				rn.StartOutfeed AS StartOutfeed,
				rn.CurrentOutfeed AS CurrentOutfeed,
				rn.GoodCount AS GoodCount,
				rn.TotalCount AS TotalCount,
				n.name AS nodeName,
				
				
				ROW_NUMBER() OVER (ORDER BY rn.RunStartDateTime DESC) AS rnOrder
			FROM run rn
			INNER JOIN schedule sch 
				ON sch.ID = rn.ScheduleID
			INNER JOIN workorder wo 
				ON wo.ID = sch.WorkOrderID
			INNER JOIN productcode pc 
				ON pc.ID = wo.ProductCodeID
			INNER JOIN mold mld 
				ON mld.ID = sch.MoldID
			INNER JOIN node n 
				ON n.ID = sch.NodeID
			LEFT JOIN standardrate str 
				ON str.ProductCodeID = pc.ID 
				AND str.MoldID = mld.ID 
				AND str.NodeID = n.ID
			WHERE n.ID = ?
			AND rn.Closed = 1
		) t

	"""
	
	try:
	    # Execute the query and return the dataset
	    dataset = system.db.runPrepQuery(query, [NodeID], db)
	    print("Query executed successfully.")
	    return dataset
	except Exception as e:
	    # Print an error message if the query fails
	    print("Error executing query: ", str(e))
	    return None
	    
def getPenultimateRunByNode(NodeID, db=db):
	"""
	Retrieves the penultimate run for a given NodeID.
	"""
	query = """
		SELECT TOP 1 *
		FROM (
			SELECT 
				wo.ID AS WorkOrderID,
				pc.ProductCode,
				rn.RunStartDateTime,
				sch.ScheduleFinishDateTime AS ScheduleFinishDateTime,
				mld.MoldCode AS MoldeCode,
				mld.Description AS MoldeName,
				str.StandardRate AS StandardRate,
				rn.ID AS RunID,
				rn.EstimatedFinishedTime,
				sch.Quantity AS Quantity,
				rn.StartOutfeed AS StartOutfeed,
				rn.CurrentOutfeed AS CurrentOutfeed,
				n.name AS nodeName,
				ROW_NUMBER() OVER (ORDER BY rn.RunStartDateTime DESC) AS rnOrder
			FROM run rn
			INNER JOIN schedule sch 
				ON sch.ID = rn.ScheduleID
			INNER JOIN workorder wo 
				ON wo.ID = sch.WorkOrderID
			INNER JOIN productcode pc 
				ON pc.ID = wo.ProductCodeID
			INNER JOIN mold mld 
				ON mld.ID = sch.MoldID
			INNER JOIN node n 
				ON n.ID = sch.NodeID
			LEFT JOIN standardrate str 
				ON str.ProductCodeID = pc.ID 
				AND str.MoldID = mld.ID 
				AND str.NodeID = n.ID
			WHERE n.ID = ? 
		) t
		WHERE rnOrder = 2;
	"""
	try:
		dataset = system.db.runPrepQuery(query, [NodeID], db)
		return dataset
	except Exception as e:
		print("Error executing query: ", str(e))
		return None
	
def IDRun (NodeID, db=db):
	try:
		# Build a query to retrieve NodeID and nodePath
		query = """
			SELECT 
				rn.ID
			FROM
				run rn
			LEFT JOIN
				schedule sch ON rn.ScheduleID = sch.ID
			LEFT JOIN
				node n ON n.ID = sch.NodeID
			LEFT JOIN
				area a ON l.ParentID = a.ID
			LEFT JOIN
				site s ON a.ParentID = s.ID
			LEFT JOIN
				enterprise e ON s.ParentID = e.ID
			WHERE rn.Closed = 0 and l.ID = ?	
		"""
		
		data = system.db.runPrepQuery(query, [NodeID], db)
		data = data.getValueAt(0,0)
		return data
	except Exception as e:
		print("Error in IDRun: {e}")
		return 0
		
def stopRun(runID, nodeID, writeTags=True, db=db):
	logger = system.util.getLogger("Button stop order")
	logger.info("Empece")
	try:
		# Build a query to retrieve NodeID and nodePath
		query = """
			SELECT 
				n.ID AS 'NodeID',
				CONCAT('[UNS]',n.Topic ,'/line') AS 'nodePath',
				rn.RunStartDateTime AS 'StartTime',
				sch.WorkOrderID
			FROM
				run rn
			LEFT JOIN
				schedule sch ON rn.ScheduleID = sch.ID
			LEFT JOIN
				node n ON n.ID = sch.NodeID
		
			WHERE rn.ID = ?	
		"""
		
		data = system.db.runPrepQuery(query, [runID], db)
		
		for row in data:
			NodeID = row['NodeID']
			nodePath = row['nodePath']
			startTime = row['startTime']
			workOrderID =  row['WorkOrderID']
		
		
		# Define tag paths related to time and enable status
		runTimePath = nodePath + '/OEE/Runtime'
		unplannedDowntimePath = nodePath + '/OEE/Unplanned Downtime'
		plannedDowntimePath = nodePath + '/OEE/Planned Downtime'
		totalTimePath = nodePath + '/OEE/Total Time'
		runIDPath = nodePath + '/OEE/RunID'
		runEnabledPath = nodePath + '/Run Enabled'
		cavitiesPath = nodePath + '/Cavities'
		statePath = nodePath + "/State"
		
		# Read all the necessary tag values
		runTime = system.tag.readBlocking([runTimePath])[0].value
		unplannedDowntime = system.tag.readBlocking([unplannedDowntimePath])[0].value
		plannedDowntime = system.tag.readBlocking([plannedDowntimePath])[0].value
		totalTime = system.tag.readBlocking([totalTimePath])[0].value
		
		# Total Time calculation
		totalTimeMillis = system.date.millisBetween(startTime, system.date.now())
		totalMinutes = totalTimeMillis / (1000* 60)
		
		# Set Storage Status
		#run.setStorageStateFromID(state='Disponible', ID=runID, typeID='run')
		
		# Update only time-related and enable status fields in the database
		queryRun = '''
				UPDATE 
					Run 
				SET
					RunStopDateTime = GETDATE(),
					TimeStamp = GETDATE(),
					Closed = 1
				WHERE ID = ?
		        '''
		argsRun = [runID]
		system.db.runPrepUpdate(queryRun, argsRun, db)
		
		# Update tags for RunID and RunEnabled status
		system.tag.writeBlocking([runIDPath], [-1])  # Set RunID to -1
		system.tag.writeBlocking([cavitiesPath], [1])  # Set Cavities to 1
		system.tag.writeBlocking([runEnabledPath], [0])  # Disable the run
		
		# Set Storage State
		#run.setStorageStateFromID(state="Disponible", ID=runID, typeID='run')
		
		#nodeDict = {"Recibo":"node01", "Trasiego":"node02", "Trasiego Molino":"node03"}
		
		# Write SCADA Tags
		#if writeTags:	
		#	system.tag.writeBlocking(["[DAUTOM_Provider]D_obj/{}_Ctrl/HMI_I_BinReceiverPos01".format(nodeDict[nodeName])], 0)
		#	system.tag.writeBlocking(["[DAUTOM_Provider]D_obj/{}_Ctrl/HMI_I_BinSenderPos01".format(nodeDict[nodeName])], 0)
		#	system.tag.writeBlocking(["[DAUTOM_Provider]D_obj/{}_Ctrl/HMI_I_JobNum".format(nodeDict[nodeName])], 0)
		#	system.tag.writeBlocking(["[DAUTOM_Provider]D_obj/{}_Ctrl/HMI_I_BatchWeight_SP".format(nodeDict[nodeName])], 0)
		
		# def insert(self, stateReasonID, startDateTime, reasonName, reasonCode,endDateTime=None, note=None, runID=None, nodeID=None)
		
		tableWO = mes_core.workOrder.workOrderTable(db)
		
		set_values = {
			"Closed":1
		}
		
		tableWO.updateID(workorder_id=workOrderID, set_values=set_values)
		
		tableSH = mes_core.model.statehistoryTable(db)
		tableSR = mes_core.model.statereasonTable(db)
		
		results = tableSH.selectCustom(columns=["TOP 1 ID"] , where_clause="NodeID=? AND EndDateTime is NULL ORDER BY StartDateTime DESC" , where_args=[nodeID]).getValueAt(0,0)
		
		tableSH.updateID(results, {"EndDateTime": system.date.now()})
		
		
		stateCode = system.tag.readBlocking(statePath)[0].value
		
		stateReasonID = tableSR.selectCustom(columns=["ID"], where_clause = "ReasonCode = ?", where_args=[stateCode])
		stateReasonID = stateReasonID.getValueAt(0,0)
		
		stateReasonName = tableSR.selectCustom(columns=["ReasonName"], where_clause = "ReasonCode = ?", where_args=[stateCode])
		stateReasonName = stateReasonName.getValueAt(0,0)
		
		tableSH.insert(stateReasonID , system.date.now(), stateReasonName,stateCode , runID=-1 , nodeID=nodeID)
		
		
	
	except Exception as e:
		logger.info("No pude: {e}")
		print("Error in stopRun: {e}")
		return 0
		
def cancelRun(runID, NodeID, db=db):
	
	logger = system.util.getLogger("Button cancel order")
	logger.info("Empece")
	try:
		
			# Build a query to retrieve NodeID and nodePath
		query = """
			SELECT 
				n.ID AS NodeID,
				CONCAT('[UNS]',n.Topic ,'/line') AS nodePath,
				rn.RunStartDateTime AS StartTime
			FROM
				run rn
			LEFT JOIN
				schedule sch ON rn.ScheduleID = sch.ID
			LEFT JOIN
				node n ON n.ID = sch.NodeID
			
			WHERE rn.ID = ?	
		"""
		
		data = system.db.runPrepQuery(query, [runID], db)
		mes_core.misc.printDatasetresultado(data)
		for row in data:
			NodeID = row['NodeID']
			nodePath = row['nodePath']
		print nodePath
		
		
		# Delete the record from the Run table for the given RunID
		runQuery = '''DELETE FROM Run WHERE ID = ?'''
		args = [runID]
		system.db.runPrepUpdate(runQuery, args, db)
		
		
		# Delete the record from the Run table for the given RunID
		runQuery = '''UPDATE schedule SET RunID = NULL, RunStartDateTime = NULL WHERE RunID = ?'''
		args = [runID]
		system.db.runPrepUpdate(runQuery, args, db)
		
		
		# Set RunEnabled tag to 0 (deactivate the run)
		runEnabledPath = nodePath + '/Run Enabled'
		system.tag.writeBlocking([runEnabledPath], [0])
		
		# Set RunID tag to -1 (reset the RunID tag to indicate no active run)
		runIDPath = nodePath + '/OEE/RunID'
		system.tag.writeBlocking([runIDPath], [-1])
		
		cavitiesPath = nodePath + '/Cavities'
		system.tag.writeBlocking([cavitiesPath], [1])
		statePath = nodePath + "/State"
		
		# Set Storage State
		#run.setStorageStateFromID(state="Agendado", ID=runID, typeID='run')
		
		# Write SCADA Tags
		#nodeDict = {"Recibo":"node01", "Trasiego":"node02", "Trasiego Molino":"node03"}
		#system.tag.writeBlocking(["[DAUTOM_Provider]D_obj/{}_Ctrl/HMI_I_BinReceiverPos01".format(nodeDict[nodeName])], 0)
		#system.tag.writeBlocking(["[DAUTOM_Provider]D_obj/{}_Ctrl/HMI_I_BinSenderPos01".format(nodeDict[nodeName])], 0)
		#system.tag.writeBlocking(["[DAUTOM_Provider]D_obj/{}_Ctrl/HMI_I_JobNum".format(nodeDict[nodeName])], 0)
		#system.tag.writeBlocking(["[DAUTOM_Provider]D_obj/{}_Ctrl/HMI_I_BatchWeight_SP".format(nodeDict[nodeName])], 0)
		
		
		tableSH = mes_core.model.statehistoryTable(db)
		tableSR = mes_core.model.statereasonTable(db)
		
		results = tableSH.selectCustom(columns=["TOP 1 ID"] , where_clause="NodeID=? AND EndDateTime is NULL ORDER BY StartDateTime DESC" , where_args=[NodeID]).getValueAt(0,0)
		
		tableSH.updateID(results, {"EndDateTime": system.date.now()})
		
		
		stateCode = system.tag.readBlocking(statePath)[0].value
		
		stateReasonID = tableSR.selectCustom(columns=["ID"], where_clause = "ReasonCode = ?", where_args=[stateCode])
		stateReasonID = stateReasonID.getValueAt(0,0)
		
		stateReasonName = tableSR.selectCustom(columns=["ReasonName"], where_clause = "ReasonCode = ?", where_args=[stateCode])
		stateReasonName = stateReasonName.getValueAt(0,0)
		
		tableSH.insert(stateReasonID , system.date.now(), stateReasonName,stateCode , runID=-1 , nodeID=NodeID)
		
		
		return 1  # Successfully cancelled the run

	except:
	    print("Error in CancelRun: {e}")
	    return 0  # Return 0 on failure

def updateRun(runID, db=db):
	"""
	Updates the run entry in the database with current tag values and other run-related data.

	Args:
		runID (int): The ID of the run to be updated.

	Returns:
		int: 1 if the update is successful, 0 if an error occurs.
	"""
	try:
		# Build a query to retrieve NodeID and nodePath
		nodeQuery = """
			SELECT 
				n.ID AS 'NodeID',
				CONCAT('[UNS]',n.Topic, '/line') AS 'nodePath',
				r.EstimatedFinishedTime as EstimatedTime
			FROM
				run r
			LEFT JOIN
				schedule sch ON r.ScheduleID = sch.ID
			LEFT JOIN
				node n ON sch.NodeID = n.ID
			
			WHERE r.ID = ?	
		"""
		args = [runID]
		data = system.db.runPrepQuery(nodeQuery, args, db)
		
		for row in data:
			NodeID = row['NodeID']
			nodePath = row['nodePath']
			estimatedTime = row['EstimatedTime']
		
		# Calculate Finish Time
		finishTime = estimatedTime#calcFinishTime(nodePath)
		
		# Get Timestamp and Format
		timeStamp = system.date.now()#datetime.now().replace(microsecond=0)
		
		# Define all the TagPaths in a dictionary
		tagPaths = {
			'infeed': nodePath + '/Dispatch/OEE Infeed/Count',
			'outfeed': nodePath + '/Dispatch/OEE Outfeed/Count',
			'waste': nodePath + '/Dispatch/OEE Waste/Count',
			'totalCount': nodePath + '/OEE/Total Count',
			'badCount': nodePath + '/OEE/Bad Count',
			'goodCount': nodePath + '/OEE/Good Count',
			'oeeQuality': nodePath + '/OEE/OEE Quality',
			'oeePerformance': nodePath + '/OEE/OEE Performance',
			'oeeAvailability': nodePath + '/OEE/OEE Availability',
			'oee': nodePath + '/OEE/OEE',
			'runTime': nodePath + '/OEE/Run Time',
			'unplannedDowntime': nodePath + '/OEE/Unplanned Downtime',
			'plannedDowntime': nodePath + '/OEE/Planned Downtime',
			'totalTime': nodePath + '/OEE/Total Time',
			'scheduleTime': nodePath + '/OEE/Schedule Time',
			'cavities': nodePath + '/Cavities'
		}
		
		# Read all the tag values in one call
		tagValues = system.tag.readBlocking(list(tagPaths.values()))
		
		# Map the tag values to their respective keys
		tagData = {key: value.value for key, value in zip(tagPaths.keys(), tagValues)}
		
		# Example of how to use the tag values
		infeed = tagData['infeed']
		outfeed = tagData['outfeed']
		waste = tagData['waste']
		totalCount = tagData['totalCount']
		badCount = tagData['badCount']
		goodCount = tagData['goodCount']
		oeeQuality = tagData['oeeQuality']
		oeePerformance = tagData['oeePerformance']
		oeeAvailability = tagData['oeeAvailability']
		oee = tagData['oee']
		runTime = tagData['runTime']
		unplannedDowntime = tagData['unplannedDowntime']
		plannedDowntime = tagData['plannedDowntime']
		totalTime = tagData['totalTime']
		scheduleTime = tagData['scheduleTime']
		cavities = tagData['cavities']
		
		# Update Run
		query = """
			UPDATE 
				Run
			SET
				RunTime = ?,
				UnplannedDowntime = ?,
				PlannedDowntime = ?,
				TotalTime = ?,
				TimeStamp = ?,
				Closed = ?,
				CurrentInfeed = ?,
				CurrentOutfeed = ?,
				CurrentWaste = ?,
				TotalCount = ?,
				GoodCount = ?,
				Availability = ?,
				Performance = ?,
				Quality = ?,
				OEE = ?,
				WasteCount = ?,
				ScheduleTime=?
			
			WHERE
				ID = ?      
		"""
		args = [runTime, unplannedDowntime, plannedDowntime, 
				totalTime, timeStamp, 0, infeed *cavities, outfeed*cavities , waste , 
				totalCount , goodCount , oeeAvailability , oeePerformance,
				oeeQuality, oee,badCount,scheduleTime,
				runID]
		system.db.runPrepUpdate(query, args, db)
		
		# Assuming there are further steps in the update process
		# These might involve writing to tags or updating the database
		
		print("Update run completed for RunID {}".format(runID))
		return 1
		
	except Exception as e:
		print("Error updating run: {}".format(e))
		return 0


def checkRunAvailability(scheduleID, db=db):
	"""
	Checks if a specific run is available based on the schedule ID by evaluating the storage status.
	
	Parameters:
	scheduleID (int): The schedule ID to check.
	db (str): The database connection name (default is the provided db).
	
	Returns:
	int: Returns 1 if the run is available, or 0 if it is unavailable (occupied).
	"""
	
	# Retrieve source and destination storage codes based on the schedule ID
	[srcStg, dstStg] = order.getSrcDst(scheduleID)
	
	# Query to check the status of the specified storage locations
	query = """
	        SELECT
	        	StorageCode,
	            State
	        FROM
	            Storage
	        WHERE
	            StorageCode IN (?, ?)
	"""
	# Set the arguments for the query using the source and destination storage codes
	args = [srcStg, dstStg]
	
	# Execute the query to get the status of the specified storage codes
	dataset = system.db.runPrepQuery(query, args, db)
	
	# Retrieve the 'Status' column as a list to check the status of each storage location
	return [row['StorageCode'] for row in dataset if row['State'] == 'Ocupado']



def setStorageStateFromID(state, ID, typeID='schedule', db=db):
	"""
	Function to set the state of a storage based on ID and type.
	 
	Parameters:
	state (str): The new state to be set.
	ID (int): The ID associated with the schedule or run.
	typeID (str, optional): The type of ID, default is 'schedule'.
	db (str, optional): The database connection, default value is 'db'.
	
	Returns:
	None
	"""
	try:
	    # Check if the typeID is 'run' and fetch the corresponding ScheduleID
	    if typeID.lower() == 'run':
	        queryRun = '''SELECT ScheduleID FROM Run WHERE ID = ?'''
	        argsRun = [ID]
	        scheduleID = system.db.runScalarPrepQuery(queryRun, argsRun, db)
	    else:
	        scheduleID = ID  # Use the provided ID if typeID is not 'run'
	
	    # Get the source and destination storage codes
	    print scheduleID
	    [src, dst] = order.getSrcDst(scheduleID)
	    
	    # Update the state of the storage based on the source and destination
	    queryStg = '''UPDATE Storage SET State = ? WHERE StorageCode IN (?, ?)'''
	    argsStg = [state, src, dst]
	    system.db.runPrepUpdate(queryStg, argsStg, db)
	    
	    return 1
	  
	except:
		return 0

def writePlate(runID, plateNumber, description, db=db):
	"""
	Function to write the Plate number of a truck in a Recibo Run.
	 
	Parameters:
	runID (int): the ID of the run associated
	plateNumber (str): the Truck Plate
	
	Returns:
	None
	"""
	try:
		# Query to check the status of the specified storage locations
		query = '''
				INSERT INTO TruckPlates (
					PlateNumber,
					RunID,
					TimeStamp,
					Description
					) 
				VALUES(?, ?, NOW(), ?); 
			'''
		args = [plateNumber, runID, description]
		
		# Execute the query to insert the truck plate associated to RunID
		system.db.runPrepUpdate(query, args, db)
		return 1
	    
	except:
		return 0

def getSchQty(runID, db=db):
	"""
	Function to get the scheduled quantity of a run.
	 
	Parameters:
	runID (int): the ID of the run associated
	
	Returns:
	Scheduled quantity of the run
	"""
	try:
		# Query to check the status of the specified storage locations
		query = ''' SELECT Quantity FROM Schedule WHERE RunID = ? '''
		args = [runID]
		
		# Execute the query to insert the truck plate associated to RunID
		qty = system.db.runScalarPrepQuery(query, args, db)
		return qty or 0
	    
	except:
		return 0
		
def writeRunQty(runID, actualQty, db=db):
	"""
	Function to write the final quantity of a run
	 
	Parameters:
	runID (int): the ID of the run associated
	
	Returns:
	None
	"""
		
	try:
		# Query to check the status of the specified storage locations
		query = ''' UPDATE Schedule SET ActualQuantity = ? WHERE RunID = ? '''
		args = [actualQty, runID]
		
		# Execute the query to insert the truck plate associated to RunID
		system.db.runPrepUpdate(query, args, db)
		return 1
	    
	except:
		return 0
		
def getEstimatedFinish(scheduleID, db=db):
	"""
	Function to calculate the estimated finish of a run starting from the Schedule ID
	 
	Parameters:
	scheduleID (int): the ID of the schedule associated
	
	Returns:
	estimatedFinish (datetime): the estimated date finish 
	"""
	query = """
		SELECT ScheduleStartDateTime, ScheduleFinishDateTime
		FROM Schedule
		WHERE ID = ?
		"""
	args = [scheduleID]
	
	
	try:
		# Execute the query to insert the truck plate associated to RunID
		dataset = system.db.runPrepQuery(query, args, db)
		startTime = dataset.getValueAt(0,0)
		finishTime = dataset.getValueAt(0,1)
		timeDiff = system.date.millisBetween(startTime, finishTime)
		
		return system.date.addMillis(system.date.now(), timeDiff)
	    
	except:
		return 0
		
def getRunTable(db=db):
	"""
	Function to query the run table
	 
	Parameters:
	None
	
	Returns:
	dataset (dataset): the dataset of the query
	"""
	query = """
		SELECT 
			rn.ID,
			rn.ScheduleID,
			wo.ID AS WorkOrderID,
			l.Name AS nodeName,
			wo.WorkOrder,
			wo.Description,
			rn.RunStartDateTime AS RunStart,
			rn.RunStopDateTime AS RunStop,
			rn.RunTime,
			rn.TotalTime,
			rn.Closed,
			sch.Quantity AS SchQty,
			sch.ActualQuantity		
		FROM 
			Run rn
		JOIN
			Schedule sch ON rn.ID = sch.RunID
		JOIN
			WorkOrder wo ON sch.WorkOrderID = wo.ID
		JOIN 
			DestinationStoragenode dstl ON sch.DestinationStorageNodeID = dstl.ID
		JOIN
			node l ON l.ID = dstl.NodeID
		"""
	args = []
	
	
	try:
		# Execute the query to insert the truck plate associated to RunID
		dataset = system.db.runPrepQuery(query, args, db)	
		return dataset
	    
	except:
		logging.log("Error getting run history table", "fatal")
		return 0
		
def getOrderBynode(nodeName, db=db):
	"""
	Function to get orders created by node
	 
	Parameters:
	nodeName (str): the name of the node to query the orders
	
	Returns:
	orders (list): the list with the orders
	"""
	query = """
		SELECT DISTINCT wo.WorkOrder
		FROM Schedule sch
		JOIN WorkOrder wo ON wo.ID = sch.WorkOrderID
		JOIN DestinationStoragenode dstl ON sch.DestinationStorageNodeID = dstl.ID
		JOIN node l ON l.ID = dstl.NodeID
		WHERE l.Name = ?
		"""
	args = [nodeName]
	
	
	try:
		# Execute the query to insert the truck plate associated to RunID
		dataset = system.db.runPrepQuery(query, args, db)	
		return dataset.getColumnAsList(0)
	    
	except:
		logging.log("Error getting orders by node", "fatal")
		return 0

	
	
	try:
		# Execute the query to insert the truck plate associated to RunID
		dataset = system.db.runPrepQuery(query, args, db)	
		return dataset.getColumnAsList(1)
	    
	except:
		logging.log("Error getting orders by node", "fatal")
		return 0

 
		
		

def writeData2Database(SchID):
	
	tableRun=mes_core.run.RunTable("mes_core")

	
	
	
	
	runStartTime=system.date.now()
	start_infeed=0
	current_infeed = 0
	
	tableRun.insert(SchID, runStartTime)
		