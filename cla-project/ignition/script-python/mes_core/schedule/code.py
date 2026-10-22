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

from mes_core.sql import SQLTableBase
import system

class scheduleTable(SQLTableBase):
    def __init__(self, dbConnection=None):
        columns = {
            'ID': 'int',
            'NodeID': 'int',
            'SenderStorageID': 'int',
            'ReceiverStorageID': 'int',
            'MoldID': 'int',
            'WorkOrderID': 'int',
            'ScheduleType': 'int',
            'Note': 'varchar(255)',
            'ScheduleStartDateTime': 'datetime',
            'ScheduleFinishDateTime': 'datetime',
            'Quantity': 'int',
            'EnteredBy': 'varchar(50)',
            'TimeStamp': 'datetime',
            'RunID': 'int',
            'ActualStartDateTime': 'datetime',
            'ActualFinishDateTime': 'datetime',
            'ActualQuantity': 'int',
            'RunStartDateTime': 'datetime',
        }
        SQLTableBase.__init__(self, 'schedule', columns, dbConnection)

    def insert(self, lineid, moldeid, workorderid, schedulestart, schedulefinish, quantity, enteredby, senderstorageid=None, receiverstorageid=None, scheduletype=None, note=None, timestamp=None, runid=None, actualstart=None, actualfinish=None, actualquantity=None, runstart=None):
        import system
        if timestamp is None:
            timestamp = system.date.now()
        values = {
            'NodeID': lineid,
            'MoldID': moldeid,
            'WorkOrderID': workorderid,
            'ScheduleStartDateTime': schedulestart,
            'ScheduleFinishDateTime': schedulefinish,
            'Quantity': quantity,
            'EnteredBy': enteredby,
            'TimeStamp': timestamp,
        }
        if senderstorageid is not None:
            values['SenderStorageID'] = senderstorageid
        if receiverstorageid is not None:
            values['ReceiverStorageID'] = receiverstorageid
        if scheduletype is not None:
            values['ScheduleType'] = scheduletype
        if note is not None:
            values['Note'] = note
        if runid is not None:
            values['RunID'] = runid
        if actualstart is not None:
            values['ActualStartDateTime'] = actualstart
        if actualfinish is not None:
            values['ActualFinishDateTime'] = actualfinish
        if actualquantity is not None:
            values['ActualQuantity'] = actualquantity
        if runstart is not None:
            values['RunStartDateTime'] = runstart
        SQLTableBase.insert(self, values)

    def selectID(self, schedule_id, columns=None):
        """
        Selecciona un registro de schedule por su ID.
        columns: list, lista de columnas específicas a seleccionar (opcional)
        """
        return self.select('ID = ?', [schedule_id], columns)

    def updateID(self, schedule_id, set_values):
        self.update(set_values, 'ID = ?', [schedule_id])

    def deleteID(self, schedule_id):
        self.delete('ID = ?', [schedule_id])

    def show(self):
        """
        Muestra las columnas de la tabla Schedule con sus tipos de datos.
        """
        print("Tabla: schedule")
        print("-" * 50)
        for col_name, col_type in self.columns.items():
            print("{}: {}".format(col_name, col_type))
        print("-" * 50)

    def selectAll(self, columns=None):
        """
        Selecciona todas las órdenes de trabajo con columnas opcionales.
        columns: list, lista de columnas específicas a seleccionar (opcional)
        """
        return self.select(columns=columns)
    def selectCustom(self, columns=None, where_clause=None, where_args=None):
		"""
		Realiza una consulta SELECT personalizada sobre la tabla molde.
		columns: list, lista de columnas específicas a seleccionar (opcional, si es None selecciona todas)
		where_clause: str, condición SQL opcional (ej: 'MoldeCode = ?', 'Disable = ? AND Description LIKE ?')
		where_args: list, valores para el where_clause
		Devuelve los resultados de la consulta.
		"""
		return SQLTableBase.select(self, where_clause, where_args, columns)    


def es_duplicado_con_tolerancia(fecha_nueva, fechas_ms, tol_ms):
	"""Devuelve (True, delta_ms) si fecha_nueva está a <= tol_ms de alguna fecha en fechas_ms."""
	try:
		t_new = long(fecha_nueva.getTime())
	except:
		t_new = long(fecha_nueva)
	for t_exist in fechas_ms:
		diff = t_new - t_exist
		if abs(diff) <= tol_ms:
			return True, diff
	return False, 0


def writeData2Database(nodeid, db='mes_core'):
	# Creating the table objects
	tableSchedule = mes_core.schedule.scheduleTable(db)
	tablePC = mes_core.model.productcodeTable(db)
	tableMoldeSKU = mes_core.model.productcodemoldeTable(db)
	tableWork = mes_core.workOrder.workOrderTable(db)

	# Pulling the workOrder table
	workOrderDataset = system.dataset.toDataSet(tableWork.selectAll())

	# Turning the dataset into a list
	rows = []
	rowCount = workOrderDataset.getRowCount()
	colCount = workOrderDataset.getColumnCount()
	for r in range(rowCount):
		row = []
		for c in range(colCount):
			row.append(workOrderDataset.getValueAt(r, c))
		rows.append(row)

	# Extracting the created work orders into a list
	createdWorkOrders = []
	for i in rows:
		createdWorkOrders.append(float(i[1]))

	# Filtering the schedule dataset according if work order is created or not
	scheduleDataset = mes_core.workOrder.calcular_fechas(nodeid = nodeid, dbConnection = db)
	headers = scheduleDataset.getColumnNames()

	filteredData = []
	for row in range(scheduleDataset.getRowCount()):
		code_val = scheduleDataset.getValueAt(row, "Code")
		try:
			if float(code_val) in createdWorkOrders:
				filteredData.append([scheduleDataset.getValueAt(row, col) for col in headers])
		except:
			continue

	# --- Pulling moldeId y workorderId garantizando alineación 1:1 ---
	moldeIds = []
	workorderIDs = []
	notCreatedMolde = []

	usedWO = set()  # evita repetir el mismo ID de WO

	# Lista alineada de filas (solo las que tienen WO utilizable y molde válido)
	filteredData_aligned = []

	for row in filteredData:
		sku = row[0]

		# Product ID
		result = tablePC.selectCustom(columns=["ID"], where_clause="ProductCode = ?", where_args=[str(sku)])
		if result.getRowCount() == 0:
			# Sin ProductID → no hay nada que hacer para este SKU
			continue
		ProductId = result.getValueAt(0, 0)

		# Molde ID
		result = tableMoldeSKU.selectCustom(columns=["MoldID"], where_clause="ProductCodeID = ?", where_args=[str(ProductId)])
		try:
			molde_id_val = result.getValueAt(0, 0)
		except:
			molde_id_val = None

		if molde_id_val is None:
			# Registrar SKU sin molde configurado
			notCreatedMolde.append(sku)
			# No alineamos esta fila porque terminaría desfasando listas
			continue

		# WorkOrder IDs candidatos para el SKU (traemos Hide para filtrar)
		result = tableWork.selectCustom(columns=["ID", "Hide"], where_clause="WorkOrder = ?", where_args=[str(sku)])
		resultDataset = system.dataset.toDataSet(result)

		# Selecciona el primer WO no usado y no oculto (Hide != 1)
		wo_id_elegido = None
		for irow in range(resultDataset.getRowCount()):
			wo_id = resultDataset.getValueAt(irow, 0)
			try:
				hide_val = resultDataset.getValueAt(irow, 1)
			except:
				hide_val = 0
			if (hide_val is None or int(hide_val) == 0) and wo_id not in usedWO:
				wo_id_elegido = wo_id
				break

		if wo_id_elegido is None:
			# No hay WO disponible (todas usadas/ocultas) → saltar fila sin desalinear
			print("No hay WO disponible para SKU %s; se omite esta fila." % (sku,))
			continue

		# Bloqueo de WO para no reutilizarla en otra fila
		usedWO.add(wo_id_elegido)

		# Alinear listas
		filteredData_aligned.append(row)
		moldeIds.append(molde_id_val)
		workorderIDs.append(wo_id_elegido)

	# --- FILTRO DE DUPLICADOS CON TOLERANCIA (DB existentes) ---
	existingStarts = []
	scheduleExists = tableSchedule.selectCustom(
		columns=["ScheduleStartDateTime"],
		where_clause="NodeID = ?",
		where_args=[nodeid]
	)
	for r in range(scheduleExists.getRowCount()):
		try:
			existingStarts.append(long(scheduleExists.getValueAt(r, 0).getTime()))
		except:
			existingStarts.append(long(scheduleExists.getValueAt(r, 0)))

	print("Fechas de inicio (ms) ya en la base:", existingStarts)

	tolerancia_ms = 2000
	entered_by = "admin"

	# --- CONTROL DE DESALINEACIÓN (por seguridad) ---
	len_fd = len(filteredData_aligned)
	len_mi = len(moldeIds)
	len_wo = len(workorderIDs)
	min_len = min(len_fd, len_mi, len_wo)
	if not (len_fd == len_mi == len_wo):
		print("WARN desalineación -> filteredData:%d, moldeIds:%d, workorderIDs:%d; se iterará hasta:%d"
		      % (len_fd, len_mi, len_wo, min_len))

	# --- Inserción con filtro de duplicados; actualiza existingStarts en caliente ---
	hay_nuevos = False

	for i in range(min_len):
		# moldeIds[i] siempre válido aquí (filtrado arriba)
		startDate = filteredData_aligned[i][2]

		es_dup, delta = es_duplicado_con_tolerancia(startDate, existingStarts, tolerancia_ms)
		if es_dup:
			print("Duplicado detectado (Δ=%d ms), no se inserta:" % (delta), workorderIDs[i], startDate)
			continue

		# OK para insertar
		#print("Insertar:", nodeid, moldeIds[i], workorderIDs[i], startDate, filteredData_aligned[i][3], filteredData_aligned[i][1], entered_by)
		tableSchedule.insert(nodeid, moldeIds[i], workorderIDs[i], startDate, filteredData_aligned[i][3], filteredData_aligned[i][1], entered_by)

		# 1) Marcar WO como usada
		set_values = {"Hide": 1}
		tableWork.updateID(workorderIDs[i], set_values)

		# 2) Inyectar fecha recién insertada para bloquear duplicados del mismo batch
		try:
			existingStarts.append(long(startDate.getTime()))
		except:
			existingStarts.append(long(startDate))

		hay_nuevos = True

	# Retorna lista y flag
	return notCreatedMolde, (1 if hay_nuevos else 0)