from mes_core.sql import SQLTableBase
import system

class moldeTable(SQLTableBase):
	def __init__(self, dbConnection=None):
		columns = {
			'ID': 'int',
			'MoldCode': 'varchar(100)',
			'Description': 'varchar(255)',
			'Slot': 'int',
			'Disable': 'tinyint',
			'TimeStamp': 'datetime',
		}
		SQLTableBase.__init__(self, 'mold', columns, dbConnection)

	def insert(self, moldecode, slot, description=None, disable=0, timestamp=None):
		import system
		if timestamp is None:
			timestamp = system.date.now()
		values = {
			'MoldCode': moldecode,
			'Slot':slot,
			'Disable': disable,
			'TimeStamp': timestamp,
		}
		if description is not None:
			values['Description'] = description
		SQLTableBase.insert(self, values)

	def selectID(self, molde_id, columns=None):
		"""
		Selecciona un molde por su ID.
		columns: list, lista de columnas específicas a seleccionar (opcional)
		"""
		return self.select('ID = ?', [molde_id], columns)

	def updateID(self, molde_id, set_values):
		"""
		Actualiza un molde por su ID.
		set_values: dict con los campos a actualizar
		"""
		self.update(set_values, 'ID = ?', [molde_id])

	def deleteID(self, molde_id):
		"""
		Elimina un molde por su ID.
		"""
		self.delete('ID = ?', [molde_id])

	def show(self):
		"""
		Muestra las columnas de la tabla Molde con sus tipos de datos.
		"""
		print("Tabla: molde")
		print("-" * 50)
		for col_name, col_type in self.columns.items():
			print("{}: {}".format(col_name, col_type))
		print("-" * 50)
		
	def selectAll(self, columns=None, order_by=None, order_direction='ASC'):
		"""
		Selecciona todos los registros de schedule con columnas opcionales y ordenamiento.
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
		
	def validateColumn(self, column_data):
		"""
		Verifica si ya existe una orden de trabajo.
		column_data: dict, {'column': valor} a validar
		Retorna: bool (True si existe, False si no) and IDs
		"""
		result = self.validateExists(column_data=column_data)
		exists = result['exists']
		ids = result['ids']
		return exists, ids

class productcodeTable(SQLTableBase):
	def __init__(self, dbConnection=None):
		columns = {
			'ID': 'int',
			'ProductCode': 'varchar(100)',
			'Description': 'varchar(255)',
			'Disable': 'tinyint',
			'TimeStamp': 'datetime',
		}
		SQLTableBase.__init__(self, 'productcode', columns, dbConnection)

	def insert(self, productcode, description=None, disable=0, timestamp=None):
		import system
		if timestamp is None:
			timestamp = system.date.now()
		values = {
			'ProductCode': productcode,
			'Disable': disable,
			'TimeStamp': timestamp,
		}
		if description is not None:
			values['Description'] = description
		SQLTableBase.insert(self, values)

	def selectID(self, productcode_id, columns=None):
		"""
		Selecciona un código de producto por su ID.
		columns: list, lista de columnas específicas a seleccionar (opcional)
		"""
		return self.select('ID = ?', [productcode_id], columns)

	def updateID(self, productcode_id, set_values):
		"""
		Actualiza un código de producto por su ID.
		set_values: dict con los campos a actualizar
		"""
		self.update(set_values, 'ID = ?', [productcode_id])

	def deleteID(self, productcode_id):
		"""
		Elimina un código de producto por su ID.
		"""
		
		self.delete('ID = ?', [productcode_id])


	def show(self):
		"""
		Muestra las columnas de la tabla ProductCode con sus tipos de datos.
		"""
		print("Tabla: productcode")
		print("-" * 50)
		for col_name, col_type in self.columns.items():
			print("{}: {}".format(col_name, col_type))
		print("-" * 50)
		
	def selectAll(self, columns=None, order_by=None, order_direction='ASC'):
		"""
		Selecciona todos los registros de schedule con columnas opcionales y ordenamiento.
		columns: list, lista de columnas específicas a seleccionar (opcional)
		order_by: str, nombre de la columna por la cual ordenar (opcional)
		order_direction: str, dirección del ordenamiento ('ASC' o 'DESC', por defecto 'ASC')
		"""
		return SQLTableBase.selectAll(self, columns, order_by, order_direction)

	def validateColumn(self, column_data):
		"""
		Verifica si ya existe una orden de trabajo.
		column_data: dict, {'column': valor} a validar
		Retorna: bool (True si existe, False si no) and IDs
		"""
		result = self.validateExists(column_data=column_data)
		exists = result['exists']
		ids = result['ids']
		return exists, ids
		
	def selectCustom(self, columns=None, where_clause=None, where_args=None):
		"""
		Realiza una consulta SELECT personalizada sobre la tabla molde.
		columns: list, lista de columnas específicas a seleccionar (opcional, si es None selecciona todas)
		where_clause: str, condición SQL opcional (ej: 'MoldeCode = ?', 'Disable = ? AND Description LIKE ?')
		where_args: list, valores para el where_clause
		Devuelve los resultados de la consulta.
		"""
		return SQLTableBase.select(self, where_clause, where_args, columns)

class productcodemoldeTable(SQLTableBase):
	def __init__(self, dbConnection=None):
		columns = {
			'ID': 'int',
			'MoldID': 'int',
			'ProductCodeID': 'int',
			'Disable': 'tinyint',
			'TimeStamp': 'datetime',
		}
		SQLTableBase.__init__(self, 'productcodemold', columns, dbConnection)

	def insert(self, moldeid, productcodeid, disable=1, timestamp=None):
		import system
		if timestamp is None:
			timestamp = system.date.now()
		values = {
			'MoldID': moldeid,
			'ProductCodeID': productcodeid,
			'Disable': disable,
			'TimeStamp': timestamp,
		}
		SQLTableBase.insert(self, values)

	def selectID(self, productcodemolde_id, columns=None):
		"""
		Selecciona una relación molde-producto por su ID.
		columns: list, lista de columnas específicas a seleccionar (opcional)
		"""
		return self.select('ID = ?', [productcodemolde_id], columns)

	def updateID(self, productcodemolde_id, set_values):
		"""
		Actualiza una relación molde-producto por su ID.
		set_values: dict con los campos a actualizar
		"""
		self.update(set_values, 'ID = ?', [productcodemolde_id])

	def deleteID(self, productcodemolde_id):
		"""
		Elimina una relación molde-producto por su ID.
		"""
		self.delete('ID = ?', [productcodemolde_id])

	def selectAll(self, columns=None):
		"""
		Selecciona todas las relaciones molde-producto con columnas opcionales.
		columns: list, lista de columnas específicas a seleccionar (opcional)
		"""
		return self.select(columns=columns)

	def show(self):
		"""
		Muestra las columnas de la tabla ProductCodeMolde con sus tipos de datos.
		"""
		print("Tabla: productcodemold")
		print("-" * 50)
		for col_name, col_type in self.columns.items():
			print("{}: {}".format(col_name, col_type))
		print("-" * 50)

	def validateColumn(self, column_data):
		"""
		Verifica si ya existe una orden de trabajo.
		column_data: dict, {'column': valor} a validar
		Retorna: bool (True si existe, False si no) and IDs
		"""
		result = self.validateExists(column_data=column_data)
		exists = result['exists']
		ids = result['ids']
		return exists, ids
		
	def selectCustom(self, columns=None, where_clause=None, where_args=None):
		"""
		Realiza una consulta SELECT personalizada sobre la tabla molde.
		columns: list, lista de columnas específicas a seleccionar (opcional, si es None selecciona todas)
		where_clause: str, condición SQL opcional (ej: 'MoldeCode = ?', 'Disable = ? AND Description LIKE ?')
		where_args: list, valores para el where_clause
		Devuelve los resultados de la consulta.
		"""
		return SQLTableBase.select(self, where_clause, where_args, columns)

class productcodelineTable(SQLTableBase):
	def __init__(self, dbConnection=None):
		columns = {
			'ID': 'int',
			'ProductCodeID': 'int',
			'NodeID': 'int',
			'Disable': 'tinyint',
			'TimeStamp': 'datetime',
		}
		SQLTableBase.__init__(self, 'productcodenode', columns, dbConnection)

	def insert(self, productcodeid, lineid, disable=1, timestamp=None):
		import system
		if timestamp is None:
			timestamp = system.date.now()
		values = {
			'ProductCodeID': productcodeid,
			'NodeID': lineid,
			'Disable': disable,
			'TimeStamp': timestamp,
		}
		SQLTableBase.insert(self, values)

	def selectID(self, productcodeline_id, columns=None):
		"""
		Selecciona una relación producto-línea por su ID.
		columns: list, lista de columnas específicas a seleccionar (opcional)
		"""
		return self.select('ID = ?', [productcodeline_id], columns)

	def updateID(self, productcodeline_id, set_values):
		"""
		Actualiza una relación producto-línea por su ID.
		set_values: dict con los campos a actualizar
		"""
		self.update(set_values, 'ID = ?', [productcodeline_id])

	def deleteID(self, productcodeline_id):
		"""
		Elimina una relación producto-línea por su ID.
		"""
		self.delete('ID = ?', [productcodeline_id])

	def show(self):
		"""
		Muestra las columnas de la tabla ProductCodeLine con sus tipos de datos.
		"""
		print("Tabla: productcodeline")
		print("-" * 50)
		for col_name, col_type in self.columns.items():
			print("{}: {}".format(col_name, col_type))
		print("-" * 50)

	def selectAll(self, columns=None, order_by=None, order_direction='ASC'):
		"""
		Selecciona todas las relaciones producto-línea con columnas opcionales y ordenamiento.
		columns: list, lista de columnas específicas a seleccionar (opcional)
		order_by: str, nombre de la columna por la cual ordenar (opcional)
		order_direction: str, dirección del ordenamiento ('ASC' o 'DESC', por defecto 'ASC')
		"""
		return SQLTableBase.selectAll(self, columns, order_by, order_direction)

	def selectCustom(self, columns=None, where_clause=None, where_args=None):
		"""
		Realiza una consulta SELECT personalizada sobre la tabla productcodeline.
		columns: list, lista de columnas específicas a seleccionar (opcional, si es None selecciona todas)
		where_clause: str, condición SQL opcional (ej: 'ProductCodeID = ?', 'LineID = ? AND Disable = ?')
		where_args: list, valores para el where_clause
		Devuelve los resultados de la consulta.
		"""
		return SQLTableBase.select(self, where_clause, where_args, columns)

	def validateColumn(self, column_data):
		"""
		Verifica si ya existe una relación producto-línea.
		column_data: dict, {'column': valor} a validar
		Retorna: bool (True si existe, False si no) and IDs
		"""
		result = self.validateExists(column_data=column_data)
		exists = result['exists']
		ids = result['ids']
		return exists, ids

class standardrateTable(SQLTableBase):
	def __init__(self, dbConnection=None):
		columns = {
			'ID': 'int',
			'ProductCodeID': 'int',
			'MoldID': 'int',
			'StandardRate': 'int',
			'NodeID': 'int',
			'Disable': 'tinyint',
			'TimeStamp': 'datetime',
		}
		SQLTableBase.__init__(self, 'standardrate', columns, dbConnection)

	def insert(self, productcodeid, moldid,nodeid, standardrate, disable=1, timestamp=None):
		import system
		if timestamp is None:
			timestamp = system.date.now()
		values = {
			'ProductCodeID': productcodeid,
			'MoldID': moldid,
			'NodeID':nodeid,
			'StandardRate': standardrate,
			'Disable': disable,
			'TimeStamp': timestamp,
		}
		SQLTableBase.insert(self, values)

	def selectID(self, standardrate_id, columns=None):
		"""
		Selecciona una tasa estándar por su ID.
		columns: list, lista de columnas específicas a seleccionar (opcional)
		"""
		return self.select('ID = ?', [standardrate_id], columns)

	def updateID(self, standardrate_id, set_values):
		"""
		Actualiza una tasa estándar por su ID.
		set_values: dict con los campos a actualizar
		"""
		self.update(set_values, 'ID = ?', [standardrate_id])

	def deleteID(self, standardrate_id):
		"""
		Elimina una tasa estándar por su ID.
		"""
		self.delete('ID = ?', [standardrate_id])

	def show(self):
		"""
		Muestra las columnas de la tabla StandardRate con sus tipos de datos.
		"""
		print("Tabla: standardrate")
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
		Realiza una consulta SELECT personalizada sobre la tabla standardrate.
		columns: list, lista de columnas específicas a seleccionar (opcional, si es None selecciona todas)
		where_clause: str, condición SQL opcional (ej: 'ProductCodeLineID = ?', 'Disable = ? AND StandardRate > ?')
		where_args: list, valores para el where_clause
		Devuelve los resultados de la consulta.
		"""
		return SQLTableBase.select(self, where_clause, where_args, columns)
		
	def validateColumn(self, column_data):
		"""
		Verifica si ya existe una tasa estándar.
		column_data: dict, {'column': valor} a validar
		Retorna: bool (True si existe, False si no) and IDs
		"""
		result = self.validateExists(column_data=column_data)
		exists = result['exists']
		ids = result['ids']
		return exists, ids

class counthistoryTable(SQLTableBase):
	def __init__(self, dbConnection=None):
		columns = {
			'ID': 'int',
			'TagID': 'int',
			'RunID': 'int',
			# 'CountTypeID': 'int',  # Descomentarlo si lo agregas nuevamente
			'Count': 'int',
			'TimeStamp': 'datetime',
		}
		SQLTableBase.__init__(self, 'counthistory', columns, dbConnection)

	def insert(self, tagID, count, timestamp=None, runID=None):
		"""
		Inserta un nuevo registro en counthistory.
		- tagID: int, obligatorio
		- count: int, obligatorio
		- timestamp: datetime, opcional (usa hora actual si no se pasa)
		- runID: int, opcional
		"""
		import system
		if timestamp is None:
			timestamp = system.date.now()

		values = {
			'TagID': tagID,
			'Count': count,
			'TimeStamp': timestamp
		}

		if runID is not None:
			values['RunID'] = runID

		SQLTableBase.insert(self, values)

	def selectID(self, row_id, columns=None):
		"""
		Selecciona un registro de counthistory por su ID.
		"""
		return self.select('ID = ?', [row_id], columns)

	def updateID(self, row_id, set_values):
		"""
		Actualiza un registro de counthistory por su ID.
		"""
		self.update(set_values, 'ID = ?', [row_id])

	def deleteID(self, row_id):
		"""
		Elimina un registro de counthistory por su ID.
		"""
		self.delete('ID = ?', [row_id])

	def show(self):
		"""
		Muestra las columnas de la tabla counthistory con sus tipos de datos.
		"""
		print("Tabla: counthistory")
		print("-" * 50)
		for col_name, col_type in self.columns.items():
			print("{}: {}".format(col_name, col_type))
		print("-" * 50)

	def selectAll(self, columns=None):
		"""
		Selecciona todos los registros de counthistory.
		"""
		return self.select(columns=columns)
		
	def selectCustom(self, columns=None, where_clause=None, where_args=None):
		"""
		Executes a custom SELECT on the counthistory table.

		Parameters:
			columns (list|None): Specific columns to select, or None for all.
			where_clause (str|None): Optional SQL WHERE clause with '?' placeholders.
				Examples: 'RunID = ?', 'TagID = ? AND TimeStamp >= ?'
			where_args (list|tuple|None): Values for the placeholders in where_clause.

		Returns:
			PyDataSet: Query result for the requested projection and filter.
		"""
		return SQLTableBase.select(self, where_clause, where_args, columns)
		
class statehistoryTable(SQLTableBase):
	def __init__(self, dbConnection=None):
		# Defines the columns and their data types for the statehistory table
		columns = {
			'ID': 'int',
			'StateReasonID': 'int',
			'StartDateTime': 'datetime',
			'EndDateTime': 'datetime',
			'ReasonName': 'varchar(50)',
			'ReasonCode': 'int',
			'Note': 'varchar(100)',
			'RunID': 'int',
			'NodeID': 'int'
		}
		SQLTableBase.__init__(self, 'statehistory', columns, dbConnection)
	
	def insert(self, stateReasonID, startDateTime, reasonName, reasonCode,
	           endDateTime=None, note=None, runID=None, nodeID=None):
		"""
		Inserts a new record into statehistory.
		- stateReasonID: int, required
		- startDateTime: datetime, required
		- reasonName: str, required
		- reasonCode: int, required
		- endDateTime: datetime, optional
		- note: str, optional
		- runID: int, optional
		- NodeID: int, optional
		"""
		import system
		values = {
			'StateReasonID': stateReasonID,
			'StartDateTime': startDateTime,
			'ReasonName': reasonName,
			'ReasonCode': reasonCode,
			'EndDateTime': endDateTime,
			'Note': note,
			'RunID': runID,
			'NodeID': nodeID,
		}
		if endDateTime is not None:
			values['EndDateTime'] = endDateTime
		if note is not None:
			values['Note'] = note
		if runID is not None:
			values['RunID'] = runID
		if nodeID is not None:
			values['NodeID'] = nodeID
	
		SQLTableBase.insert(self, values)
	
	def selectID(self, row_id, columns=None):
		"""
		Selects a record from statehistory by its ID.
		"""
		return self.select('ID = ?', [row_id], columns)
	
	def updateID(self, row_id, set_values):
		"""
		Updates a record from statehistory by its ID.
		"""
		self.update(set_values, 'ID = ?', [row_id])
	
	def deleteID(self, row_id):
		"""
		Deletes a record from statehistory by its ID.
		"""
		self.delete('ID = ?', [row_id])
	
	def show(self):
		"""
		Displays the columns of the statehistory table with their data types.
		"""
		print("Table: statehistory")
		print("-" * 50)
		for col_name, col_type in self.columns.items():
			print("{}: {}".format(col_name, col_type))
		print("-" * 50)
	
	def selectAll(self, columns=None):
		"""
		Selects all records from statehistory.
		"""
		return self.select(columns=columns)

	def selectCustom(self, columns=None, where_clause=None, where_args=None):
		"""
		Realiza una consulta SELECT personalizada sobre la tabla standardrate.
		columns: list, lista de columnas específicas a seleccionar (opcional, si es None selecciona todas)
		where_clause: str, condición SQL opcional (ej: 'ProductCodeLineID = ?', 'Disable = ? AND StandardRate > ?')
		where_args: list, valores para el where_clause
		Devuelve los resultados de la consulta.
		"""
		return SQLTableBase.select(self, where_clause, where_args, columns)
		
class lineTable(SQLTableBase):
	def __init__(self, dbConnection=None):
		columns = {
			'ID': 'int',
			'Name': 'varchar(50)',
			'TimeStamp': 'datetime',
			'Disable': 'tinyint',
			'ParentID': 'int',
			'Description': 'varchar(255)',
		}
		SQLTableBase.__init__(self, 'line', columns, dbConnection)

	def insert(self, name, parent_id, description=None, disable=0, timestamp=None):
		import system
		if timestamp is None:
			timestamp = system.date.now()
		values = {
			'Name': name,
			'ParentID': parent_id,
			'Disable': disable,
			'TimeStamp': timestamp,
		}
		if description is not None:
			values['Description'] = description
		SQLTableBase.insert(self, values)

	def selectID(self, line_id, columns=None):
		"""
		Selecciona una línea por su ID.
		columns: list, lista de columnas específicas a seleccionar (opcional)
		"""
		return self.select('ID = ?', [line_id], columns)

	def updateID(self, line_id, set_values):
		"""
		Actualiza una línea por su ID.
		set_values: dict con los campos a actualizar
		"""
		self.update(set_values, 'ID = ?', [line_id])

	def deleteID(self, line_id):
		"""
		Elimina una línea por su ID.
		"""
		self.delete('ID = ?', [line_id])

	def show(self):
		"""
		Muestra las columnas de la tabla Line con sus tipos de datos.
		"""
		print("Tabla: line")
		print("-" * 50)
		for col_name, col_type in self.columns.items():
			print("{}: {}".format(col_name, col_type))
		print("-" * 50)
		
	def selectAll(self, columns=None, order_by=None, order_direction='ASC'):
		"""
		Selecciona todos los registros de line con columnas opcionales y ordenamiento.
		columns: list, lista de columnas específicas a seleccionar (opcional)
		order_by: str, nombre de la columna por la cual ordenar (opcional)
		order_direction: str, dirección del ordenamiento ('ASC' o 'DESC', por defecto 'ASC')
		"""
		return SQLTableBase.selectAll(self, columns, order_by, order_direction)

	def selectCustom(self, columns=None, where_clause=None, where_args=None):
		"""
		Realiza una consulta SELECT personalizada sobre la tabla line.
		columns: list, lista de columnas específicas a seleccionar (opcional, si es None selecciona todas)
		where_clause: str, condición SQL opcional (ej: 'Name = ?', 'Disable = ? AND ParentID = ?')
		where_args: list, valores para el where_clause
		Devuelve los resultados de la consulta.
		"""
		return SQLTableBase.select(self, where_clause, where_args, columns)
		
	def validateColumn(self, column_data):
		"""
		Verifica si ya existe un valor en una columna específica.
		column_data: dict, {'column': valor} a validar
		Retorna: bool (True si existe, False si no) and IDs
		"""
		result = self.validateExists(column_data=column_data)
		exists = result['exists']
		ids = result['ids']
		return exists, ids
		
class statereasonTable(SQLTableBase):
	def __init__(self, dbConnection=None):
		columns = {
			'ID': 'int',
			'NodeID': 'int',
			'ReasonName': 'varchar(50)',
			'ReasonCode': 'int',
			'RecordDowntime': 'tinyint',
			'PlannedDowntime': 'tinyint',
			'OperatorSelectable': 'tinyint',
			'SubReasonOf': 'int',
		}
		SQLTableBase.__init__(self, 'statereason', columns, dbConnection)

	def insert(self, nodeid, reasonname, reasoncode, recorddowntime=0, planneddowntime=0, operatorselectable=0, subreasonof=None):
		values = {
			'NodeID': nodeid,
			'ReasonName': reasonname,
			'ReasonCode': reasoncode,
			'RecordDowntime': recorddowntime,
			'PlannedDowntime': planneddowntime,
			'OperatorSelectable': operatorselectable,
		}
		if subreasonof is not None:
			values['SubReasonOf'] = subreasonof
		SQLTableBase.insert(self, values)

	def selectID(self, statereason_id, columns=None):
		"""
		Selecciona un motivo de estado por su ID.
		columns: list, lista de columnas específicas a seleccionar (opcional)
		"""
		return self.select('ID = ?', [statereason_id], columns)

	def updateID(self, statereason_id, set_values):
		"""
		Actualiza un motivo de estado por su ID.
		set_values: dict con los campos a actualizar
		"""
		self.update(set_values, 'ID = ?', [statereason_id])

	def deleteID(self, statereason_id):
		"""
		Elimina un motivo de estado por su ID.
		"""
		self.delete('ID = ?', [statereason_id])

	def show(self):
		"""
		Muestra las columnas de la tabla StateReason con sus tipos de datos.
		"""
		print("Tabla: statereason")
		print("-" * 50)
		for col_name, col_type in self.columns.items():
			print("{}: {}".format(col_name, col_type))
		print("-" * 50)
		
	def selectAll(self, columns=None, order_by=None, order_direction='ASC'):
		"""
		Selecciona todos los registros de statereason con columnas opcionales y ordenamiento.
		columns: list, lista de columnas específicas a seleccionar (opcional)
		order_by: str, nombre de la columna por la cual ordenar (opcional)
		order_direction: str, dirección del ordenamiento ('ASC' o 'DESC', por defecto 'ASC')
		"""
		return SQLTableBase.selectAll(self, columns, order_by, order_direction)

	def selectCustom(self, columns=None, where_clause=None, where_args=None):
		"""
		Realiza una consulta SELECT personalizada sobre la tabla statereason.
		columns: list, lista de columnas específicas a seleccionar (opcional, si es None selecciona todas)
		where_clause: str, condición SQL opcional (ej: 'ReasonName = ?', 'ParentID = ? AND RecordDowntime = ?')
		where_args: list, valores para el where_clause
		Devuelve los resultados de la consulta.
		"""
		return SQLTableBase.select(self, where_clause, where_args, columns)
		
	def validateColumn(self, column_data):
		"""
		Verifica si ya existe un valor en una columna específica.
		column_data: dict, {'column': valor} a validar
		Retorna: bool (True si existe, False si no) and IDs
		"""
		result = self.validateExists(column_data=column_data)
		exists = result['exists']
		ids = result['ids']
		return exists, ids


class nodeTable(SQLTableBase):
	def __init__(self, dbConnection=None):
		columns = {
			'ID': 'int',
			'Selectable': 'tinyint',
			'Type': 'varchar(255)',
			'DisplayName': 'varchar(255)',
			'ParentNodeID': 'int',
			'Name': 'varchar(255)',
			'Topic': 'varchar(255)',
		}
		SQLTableBase.__init__(self, 'node', columns, dbConnection)

	def insert(self, selectable=1, type=None, displayname=None, parentnodeid=None, name=None, topic=None):
		values = {
			'Selectable': selectable,
		}
		if type is not None:
			values['Type'] = type
		if displayname is not None:
			values['DisplayName'] = displayname
		if parentnodeid is not None:
			values['ParentNodeID'] = parentnodeid
		if name is not None:
			values['Name'] = name
		if topic is not None:
			values['Topic'] = topic
		SQLTableBase.insert(self, values)

	def selectID(self, node_id, columns=None):
		"""
		Selecciona un nodo por su ID.
		columns: list, lista de columnas específicas a seleccionar (opcional)
		"""
		return self.select('ID = ?', [node_id], columns)

	def updateID(self, node_id, set_values):
		"""
		Actualiza un nodo por su ID.
		set_values: dict con los campos a actualizar
		"""
		self.update(set_values, 'ID = ?', [node_id])

	def deleteID(self, node_id):
		"""
		Elimina un nodo por su ID.
		"""
		self.delete('ID = ?', [node_id])

	def show(self):
		"""
		Muestra las columnas de la tabla Node con sus tipos de datos.
		"""
		print("Tabla: node")
		print("-" * 50)
		for col_name, col_type in self.columns.items():
			print("{}: {}".format(col_name, col_type))
		print("-" * 50)
		
	def selectAll(self, columns=None, order_by=None, order_direction='ASC'):
		"""
		Selecciona todos los registros de node con columnas opcionales y ordenamiento.
		columns: list, lista de columnas específicas a seleccionar (opcional)
		order_by: str, nombre de la columna por la cual ordenar (opcional)
		order_direction: str, dirección del ordenamiento ('ASC' o 'DESC', por defecto 'ASC')
		"""
		return SQLTableBase.selectAll(self, columns, order_by, order_direction)

	def selectCustom(self, columns=None, where_clause=None, where_args=None):
		"""
		Realiza una consulta SELECT personalizada sobre la tabla node.
		columns: list, lista de columnas específicas a seleccionar (opcional, si es None selecciona todas)
		where_clause: str, condición SQL opcional (ej: 'Name = ?', 'Type = ? AND Selectable = ?')
		where_args: list, valores para el where_clause
		Devuelve los resultados de la consulta.
		"""
		return SQLTableBase.select(self, where_clause, where_args, columns)
		
	def validateColumn(self, column_data):
		"""
		Verifica si ya existe un valor en una columna específica.
		column_data: dict, {'column': valor} a validar
		Retorna: bool (True si existe, False si no) and IDs
		"""
		result = self.validateExists(column_data=column_data)
		exists = result['exists']
		ids = result['ids']
		return exists, ids

class counttagTable(SQLTableBase):
    def __init__(self, dbConnection=None):
        columns = {
            'ID': 'int',
            'TagPath': 'varchar(100)',
            'CountTypeID': 'int',
            'NodeID': 'int',
        }
        SQLTableBase.__init__(self, 'counttag', columns, dbConnection)

    def insert(self, tagpath, counttype_id, node_id):
        values = {
            'TagPath': tagpath,
            'CountTypeID': counttype_id,
            'NodeID': node_id,
        }
        SQLTableBase.insert(self, values)

    def selectID(self, counttag_id, columns=None):
        return self.select('ID = ?', [counttag_id], columns)

    def updateID(self, counttag_id, set_values):
        self.update(set_values, 'ID = ?', [counttag_id])

    def deleteID(self, counttag_id):
        self.delete('ID = ?', [counttag_id])

    def show(self):
        print("Tabla: counttag")
        print("-" * 50)
        for col_name, col_type in self.columns.items():
            print("{}: {}".format(col_name, col_type))
        print("-" * 50)

    def selectAll(self, columns=None, order_by=None, order_direction='ASC'):
        return SQLTableBase.selectAll(self, columns, order_by, order_direction)

    def validateColumn(self, column_data):
        result = self.validateExists(column_data=column_data)
        return result['exists'], result['ids']

    def selectCustom(self, columns=None, where_clause=None, where_args=None):
        return SQLTableBase.select(self, where_clause, where_args, columns)


class counttypeTable(SQLTableBase):
    def __init__(self, dbConnection=None):
        columns = {
            'ID': 'int',
            'CountType': 'varchar(50)',
        }
        SQLTableBase.__init__(self, 'counttype', columns, dbConnection)

    def insert(self, counttype):
        values = {
            'CountType': counttype,
        }
        SQLTableBase.insert(self, values)

    def selectID(self, counttype_id, columns=None):
        return self.select('ID = ?', [counttype_id], columns)

    def updateID(self, counttype_id, set_values):
        self.update(set_values, 'ID = ?', [counttype_id])

    def deleteID(self, counttype_id):
        self.delete('ID = ?', [counttype_id])

    def show(self):
        print("Tabla: counttype")
        print("-" * 50)
        for col_name, col_type in self.columns.items():
            print("{}: {}".format(col_name, col_type))
        print("-" * 50)

    def selectAll(self, columns=None, order_by=None, order_direction='ASC'):
        return SQLTableBase.selectAll(self, columns, order_by, order_direction)

    def validateColumn(self, column_data):
        result = self.validateExists(column_data=column_data)
        return result['exists'], result['ids']

    def selectCustom(self, columns=None, where_clause=None, where_args=None):
        return SQLTableBase.select(self, where_clause, where_args, columns)
        
class scheduleTable(SQLTableBase):
	def __init__(self, dbConnection=None):
		"""
		Initializes schedule table wrapper with column metadata.
		"""
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
			'RunStartDateTime': 'datetime'
		}
		SQLTableBase.__init__(self, 'schedule', columns, dbConnection)

	def insert(self, nodeID, moldID, workOrderID, scheduleStartDateTime, scheduleFinishDateTime, quantity,
	           senderStorageID=None, receiverStorageID=None, scheduleType=None, note=None,
	           enteredBy=None, timeStamp=None, runID=None, actualStartDateTime=None,
	           actualFinishDateTime=None, actualQuantity=None, runStartDateTime=None):
		"""
		Inserts a new row into schedule.

		Parameters:
			nodeID (int): Required NodeID foreign key.
			moldID (int): Required MoldID foreign key.
			workOrderID (int): Required WorkOrderID foreign key.
			scheduleStartDateTime (Date): Required planned start datetime.
			scheduleFinishDateTime (Date): Required planned finish datetime.
			quantity (int): Required planned quantity.
			senderStorageID (int|None): Optional sender storage reference.
			receiverStorageID (int|None): Optional receiver storage reference.
			scheduleType (int|None): Optional schedule type.
			note (str|None): Optional note (<=255 chars).
			enteredBy (str|None): Optional user (<=50 chars).
			timeStamp (Date|None): Optional record timestamp; defaults to now if None.
			runID (int|None): Optional associated RunID.
			actualStartDateTime (Date|None): Optional actual start datetime.
			actualFinishDateTime (Date|None): Optional actual finish datetime.
			actualQuantity (int|None): Optional actual quantity.
			runStartDateTime (Date|None): Optional run start datetime.
		"""
		if timeStamp is None:
			import system
			timeStamp = system.date.now()

		values = {
			'NodeID': nodeID,
			'MoldID': moldID,
			'WorkOrderID': workOrderID,
			'ScheduleStartDateTime': scheduleStartDateTime,
			'ScheduleFinishDateTime': scheduleFinishDateTime,
			'Quantity': quantity,
			'TimeStamp': timeStamp
		}
		if senderStorageID is not None:
			values['SenderStorageID'] = senderStorageID
		if receiverStorageID is not None:
			values['ReceiverStorageID'] = receiverStorageID
		if scheduleType is not None:
			values['ScheduleType'] = scheduleType
		if note is not None:
			values['Note'] = note
		if enteredBy is not None:
			values['EnteredBy'] = enteredBy
		if runID is not None:
			values['RunID'] = runID
		if actualStartDateTime is not None:
			values['ActualStartDateTime'] = actualStartDateTime
		if actualFinishDateTime is not None:
			values['ActualFinishDateTime'] = actualFinishDateTime
		if actualQuantity is not None:
			values['ActualQuantity'] = actualQuantity
		if runStartDateTime is not None:
			values['RunStartDateTime'] = runStartDateTime

		SQLTableBase.insert(self, values)

	def selectID(self, rowID, columns=None):
		"""
		Selects a schedule row by primary key ID.

		Parameters:
			rowID (int): Row ID to fetch.
			columns (list|None): Optional projection.

		Returns:
			PyDataSet
		"""
		return self.select('ID = ?', [rowID], columns)

	def updateID(self, rowID, setValues):
		"""
		Updates a schedule row by primary key ID.

		Parameters:
			rowID (int): Row ID to update.
			setValues (dict): Column->value pairs to set.
		"""
		self.update(setValues, 'ID = ?', [rowID])

	def deleteID(self, rowID):
		"""
		Deletes a schedule row by primary key ID.

		Parameters:
			rowID (int): Row ID to delete.
		"""
		self.delete('ID = ?', [rowID])

	def show(self):
		"""
		Prints column names and data types for schedule.
		"""
		print("Tabla: schedule")
		print("-" * 50)
		for colName, colType in self.columns.items():
			print("{}: {}".format(colName, colType))
		print("-" * 50)

	def selectAll(self, columns=None, order_by=None, order_direction='ASC'):
		"""
		Returns all rows from schedule with optional projection and ordering.

		Parameters:
			columns (list|None): Optional column list to select.
			order_by (str|None): Column name to order by.
			order_direction (str): 'ASC' or 'DESC'. Default 'ASC'.

		Returns:
			PyDataSet
		"""
		return SQLTableBase.selectAll(self, columns, order_by, order_direction)

	def selectCustom(self, columns=None, where_clause=None, where_args=None):
		"""
		Executes a custom SELECT on schedule.

		Parameters:
			columns (list|None): Columns to select (None = all).
			where_clause (str|None): WHERE clause with '?' placeholders.
			where_args (list|tuple|None): Values for the placeholders.

		Returns:
			PyDataSet
		"""
		return SQLTableBase.select(self, where_clause, where_args, columns)

	def validateColumn(self, column_data):
		"""
		Checks if a given value already exists in a specific column.

		Parameters:
			column_data (dict): Mapping {'ColumnName': value} to validate.

		Returns:
			tuple(bool, list): (exists, ids)
				- exists (bool): True if at least one row matches.
				- ids (list): Matching row IDs.
		"""
		result = self.validateExists(column_data=column_data)
		exists = result['exists']
		ids = result['ids']
		return exists, ids



def getRelationTable(dbConnection):
	query = '''
		SELECT 
			pcm.ID AS ID,
			pcm.Disable AS Disable,
			m.MoldCode,
			p.ProductCode
		FROM 
			productcodemold pcm
		INNER JOIN 
			mold m ON pcm.MoldID = m.ID
		INNER JOIN 
			productcode p ON pcm.ProductCodeID = p.ID
		'''
	return system.db.runQuery(query, dbConnection)
	
def getProductLineRelation(nodeid, dbConnection):
	"""
	Consulta la relación entre un código de producto y una línea.

	Parámetros:
	- lineid: int -> ID de la línea en la tabla line
	- dbConnection: str -> nombre de la conexión a la base de datos

	Retorna:
	- Dataset con columnas: productcode, relationid, disable
	- str con mensaje de error si ocurre una excepción
	"""
	query = """
	SELECT 
		pc.ProductCode AS productcode,
		pc.ID AS productid,
		pcl.ID AS relationid,
		pcl.Disable AS disable,
		pc.Description
	FROM productcodenode pcl
	JOIN productcode pc ON pcl.ProductCodeID = pc.ID
	WHERE pcl.NodeID = ?
	"""

	parametros = [nodeid]

	try:
		return system.db.runPrepQuery(query, parametros, dbConnection)
	except Exception as error:
		return "Error en consulta SKU-Línea: {}".format(str(error))
		
def getStandardRateRelation(dbConnection, where_clause=None, where_args=None):
	"""
	Realiza un INNER JOIN entre las tablas para obtener:
	- MoldeCode (de la tabla molde)
	- ProductCode (de la tabla productcode)
	- StandardRate (de la tabla standardrate)
	- StandardRateID (ID de la tabla standardrate)
	- StandardRate.Disable (de la tabla standardrate)
	
	Parámetros:
	dbConnection: str, nombre de la conexión a la base de datos (opcional)
	where_clause: str, condición SQL adicional opcional (ej: 'sr.Disable = ?')
	where_args: list, valores para el where_clause adicional
	
	Retorna: dataset con los resultados del JOIN
	"""
	
	# Query con INNER JOIN
	sql = """
		SELECT 
			m.MoldCode,
			pc.ProductCode,
			sr.StandardRate,
			sr.ID AS StandardRateID,
			sr.Disable,
			n.ID AS NodeID
		FROM standardrate sr
		INNER JOIN productcode pc ON sr.ProductCodeID = pc.ID
		INNER JOIN mold m ON sr.MoldID = m.ID
		INNER JOIN node n ON sr.NodeID = n.ID
	"""
	
	# Añadir condición WHERE adicional si se proporciona
	if where_clause:
		sql += " WHERE " + where_clause
		args = where_args if where_args else []
	else:
		args = []
	
	# Ejecutar la consulta
	if dbConnection:
		return system.db.runPrepQuery(sql, args, dbConnection)
	else:
		return system.db.runPrepQuery(sql, args)
		
def getProductCodeLine(nodeID, disable, dbConnection = None):
	"""
	Realiza un INNER JOIN entre las tablas productcodeline y productcode para obtener:
	- ID de productcodeline
	- ProductCode de la tabla productcode
	
	Parámetros:
	dbConnection: str, nombre de la conexión a la base de datos (opcional)
	where_clause: str, condición SQL adicional opcional (ej: 'pcl.Disable = ?')
	where_args: list, valores para el where_clause adicional
	
	Retorna: dataset con los resultados del JOIN
	"""

	args = [nodeID,disable]
	# Query con INNER JOIN
	sql = """
		SELECT 
			pcn.ID as ProductCodeNodeID,
			pc.ProductCode
		FROM productcodenode pcn
		INNER JOIN productcode pc ON pcn.ProductCodeID = pc.ID
		WHERE pcn.NodeID = ? AND pcn.Disable = ? ORDER BY pcn.ID ASC
	"""

	if dbConnection:
		return system.db.runPrepQuery(sql, args, dbConnection)
	else:
		return system.db.runPrepQuery(sql, args)
		
		
def getProductCodeMoldeIDByLineAndProductCodeLine(lineID, productCodeLineID, dbConnection=None):
	"""
	Obtiene el ProductCodeMoldeID relacionando las tablas productcode y productcodemolde
	usando LineID y ProductCodeLineID como parámetros de entrada.
	
	Parámetros:
	line_id: int, ID de la línea
	productcodeline_id: int, ID de productcodeline
	dbConnection: str, nombre de la conexión a la base de datos (opcional)
	
	Retorna: dataset con el ProductCodeMoldeID y información relacionada
	"""

	
	# Query con INNER JOIN
	sql = """
		SELECT 
			pcm.ID as ProductCodeMoldeID,
			pc.ProductCode,
			pcl.LineID,
			pcl.ID as ProductCodeLineID,
			m.MoldeCode
		FROM productcodeline pcl
		INNER JOIN productcode pc ON pcl.ProductCodeID = pc.ID
		INNER JOIN productcodemold pcm ON pc.ID = pcm.ProductCodeID
		INNER JOIN molde m ON pcm.MoldeID = m.ID
		WHERE pcl.LineID = ? AND pcl.ID = ?
	"""
	
	args = [lineID, productCodeLineID]
	
	# Ejecutar la consulta
	if dbConnection:
		return system.db.runPrepQuery(sql, args, dbConnection)
	else:
		return system.db.runPrepQuery(sql, args)
		
		
def getDownTimeEvents(startTime, nodeID, dbConnection=None):
	"""
	Consulta eventos de downtime desde la tabla statehistory para una línea específica
	y una fecha de inicio dada.

	Args:
		startTime (str o datetime): Fecha y hora de inicio del rango.
		lineID (int): ID de la línea a consultar.
		dbConnection (str, optional): Nombre de la conexión a la base de datos.

	Returns:
		Dataset con los resultados de la consulta.
	"""


	query = """
			SELECT 
			    s.ID,
			    s.ReasonName,
			    s.ReasonCode,
			    s.StartDateTime,
			    s.EndDateTime, 
			    CASE 
			        WHEN s.EndDateTime IS NULL 
			            THEN DATEDIFF(SECOND, s.StartDateTime, CURRENT_TIMESTAMP)
			        ELSE DATEDIFF(SECOND, s.StartDateTime, s.EndDateTime)
			    END AS [Total in Seconds],
			    s.Note,
			    s.RunID,
			    sch.WorkOrderID
			FROM statehistory s
			LEFT JOIN statereason st ON s.StateReasonID = st.ID
			LEFT JOIN schedule sch ON s.RunID = sch.RunID
			WHERE st.ReasonCode IN (1,0)
			  AND s.StartDateTime >= ?
			  AND (
			        (s.EndDateTime < CURRENT_TIMESTAMP AND s.EndDateTime > s.StartDateTime)
			        OR (s.EndDateTime IS NULL)
			      )
			  AND s.NodeID = ?
			ORDER BY s.StartDateTime DESC;
	"""

	params = [startTime, nodeID]

	if dbConnection:
		return system.db.runPrepQuery(query, params, dbConnection)
	else:
		return system.db.runPrepQuery(query, params)
		
		
def getReasonEvents(startTime, endTime, nodeID, dbConnection=None):
    """
    Obtiene los eventos de downtime según el rango de fechas y línea.
    El campo 'Texto' será True si hay contenido en la nota, False si está vacío o es NULL.
    
    :param startTime: Fecha/hora de inicio (datetime o string compatible con SQL Server)
    :param endTime: Fecha/hora de fin (datetime o string compatible con SQL Server)
    :param lineID: ID de la línea (int)
    :param dbConnection: Nombre de la conexión a base de datos en Ignition (opcional)
    :return: Dataset con los resultados de la consulta
    """
    query = """
    SELECT 
        s.ID,
        s.ReasonName,
        s.ReasonCode,
        s.StartDateTime,
        s.EndDateTime,
        s.RunID,
        sch.WorkOrderID,
        DATEDIFF(SECOND, s.StartDateTime, s.EndDateTime) AS [Total in Seconds],
        CASE 
            WHEN s.Note IS NULL OR LTRIM(RTRIM(s.Note)) = '' THEN 0
            ELSE 1
        END AS Texto
    FROM statehistory s
    LEFT JOIN statereason st ON s.StateReasonID = st.ID
    LEFT JOIN schedule sch ON s.RunID = sch.RunID
    WHERE st.ReasonCode NOT IN (0,1,3,4,10000)
      AND s.StartDateTime >= ?
      AND s.StartDateTime <= ?
      AND s.RunID IS NOT NULL
      AND (
        (s.EndDateTime < GETDATE() AND s.EndDateTime > s.StartDateTime)
        OR (s.EndDateTime IS NULL)
      )
      AND s.NodeID = ?
    ORDER BY s.StartDateTime DESC
    """
    
    params = [startTime, endTime, nodeID]
    
    if dbConnection:
        return system.db.runPrepQuery(query, params, dbConnection)
    else:
        return system.db.runPrepQuery(query, params)


def getStandardRateByNode(nodeID, description=None, dbConnection=None):
    """
    Obtiene la información de standard rate (producto, molde, nodo) filtrada por NodeID.
    - Si 'description' viene con valor, busca en ProductCode, Description y MoldCode.
    """

    query = """
        SELECT 
            n.Name,
            p.ProductCode,
            p.Description,
            m.MoldCode,
            m.Slot,
            s.StandardRate,
            n.ID as NodeID,
            pcm.ID as ProductMoldID,
            pcn.ID as ProductNodeID,
            s.ID as StandardID,
            m.ID as MoldID,
            p.ID as ProductID
        FROM standardrate s
        INNER JOIN productcode p ON p.ID = s.ProductCodeID
        INNER JOIN mold m ON m.ID = s.MoldID
        INNER JOIN node n ON n.ID = s.NodeID
        INNER JOIN productcodenode pcn 
		    ON pcn.ProductCodeID = p.ID 
		   AND pcn.NodeID = n.ID
        INNER JOIN productcodemold pcm ON pcm.MoldID = m.ID AND pcm.ProductCodeID = p.ID
        WHERE n.ID = ?
    """

    params = [nodeID]

    # Filtro único por texto (aplica a ProductCode, Description y MoldCode)
    if description:
        query += " AND (p.ProductCode LIKE ? OR p.Description LIKE ? OR m.MoldCode LIKE ?)"
        like_value = "%{}%".format(description)
        params.extend([like_value, like_value, like_value])

    if dbConnection:
        return system.db.runPrepQuery(query, params, dbConnection)
    else:
        return system.db.runPrepQuery(query, params)