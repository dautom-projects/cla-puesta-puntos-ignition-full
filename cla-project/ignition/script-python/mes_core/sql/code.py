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

class SQLTableBase:
	def __init__(self, table_name, columns, dbConnection=None):
		"""
		table_name: str, nombre de la tabla en la base de datos
		columns: dict, mapeo de nombre_columna -> tipo_dato (ej: {'id': 'INTEGER', 'nombre': 'VARCHAR'})
		dbConnection: str, nombre de la conexión a la base de datos (opcional)
		"""
		self.table_name = table_name
		self.columns = columns  # dict: {col_name: type}
		self.dbConnection = dbConnection

	def insert(self, values):
		"""
		Inserta un registro en la tabla.
		values: dict, mapeo de nombre_columna -> valor
		"""
		col_names = ', '.join(values.keys())
		placeholders = ', '.join(['?'] * len(values))
		sql = "INSERT INTO {} ({}) VALUES ({})".format(self.table_name, col_names, placeholders)
		args = list(values.values())
		import system
		if self.dbConnection:
			system.db.runPrepUpdate(sql, args, self.dbConnection)
		else:
			system.db.runPrepUpdate(sql, args)

	def delete(self, where_clause, where_args):
		"""
		Elimina registros según condición.
		where_clause: str, condición SQL (ej: 'id = ?')
		where_args: list, valores para el where_clause
		"""
		sql = "DELETE FROM {} WHERE {}".format(self.table_name, where_clause)
		import system
		if self.dbConnection:
			system.db.runPrepUpdate(sql, where_args, self.dbConnection)
		else:
			system.db.runPrepUpdate(sql, where_args)

	def update(self, set_values, where_clause, where_args):
		"""
		Actualiza registros según condición.
		set_values: dict, mapeo de nombre_columna -> nuevo_valor
		where_clause: str, condición SQL (ej: 'id = ?')
		where_args: list, valores para el where_clause
		"""
		set_expr = ', '.join(["{} = ?".format(col) for col in set_values.keys()])
		sql = "UPDATE {} SET {} WHERE {}".format(self.table_name, set_expr, where_clause)
		args = list(set_values.values()) + where_args
		import system
		if self.dbConnection:
			system.db.runPrepUpdate(sql, args, self.dbConnection)
		else:
			system.db.runPrepUpdate(sql, args)

	def get_columns(self):
		"""
		Devuelve los nombres y tipos de columnas.
		"""
		return self.columns

	def select(self, where_clause=None, where_args=None, columns=None):
		"""
		Realiza una consulta SELECT sobre la tabla.
		where_clause: str, condición SQL opcional (ej: 'id = ?')
		where_args: list, valores para el where_clause
		columns: list, lista de columnas específicas a seleccionar (opcional)
		Devuelve los resultados de la consulta.
		"""
		
		if columns:
			col_names = ', '.join(columns)
			select_clause = "SELECT {} FROM {}".format(col_names, self.table_name)
		else:
			select_clause = "SELECT * FROM {}".format(self.table_name)

		if where_clause:
			sql = "{} WHERE {}".format(select_clause, where_clause)
			args = where_args if where_args else []
		else:
			sql = select_clause
			args = []
		if self.dbConnection:
			return system.db.runPrepQuery(sql, args, self.dbConnection)
		else:
			return system.db.runPrepQuery(sql, args)

	def selectAll(self, columns=None, order_by=None, order_direction='ASC'):
		"""
		Selecciona todos los registros de la tabla con columnas opcionales y ordenamiento.
		columns: list, lista de columnas específicas a seleccionar (opcional)
		order_by: str, nombre de la columna por la cual ordenar (opcional)
		order_direction: str, dirección del ordenamiento ('ASC' o 'DESC', por defecto 'ASC')
		Devuelve todos los resultados de la tabla ordenados.
		"""
		if order_by and order_by not in self.columns:
			raise ValueError("La columna '{}' no existe en la tabla '{}'".format(order_by, self.table_name))
		
		if order_direction.upper() not in ['ASC', 'DESC']:
			raise ValueError("order_direction debe ser 'ASC' o 'DESC'")
		
		if columns:
			col_names = ', '.join(columns)
			select_clause = "SELECT {} FROM {}".format(col_names, self.table_name)
		else:
			select_clause = "SELECT * FROM {}".format(self.table_name)
		
		if order_by:
			sql = "{} ORDER BY {} {}".format(select_clause, order_by, order_direction.upper())
		else:
			sql = select_clause
		
		import system
		if self.dbConnection:
			return system.db.runPrepQuery(sql, [], self.dbConnection)
		else:
			return system.db.runPrepQuery(sql, [])

	def validateExists(self, column_data):
		"""
		Valida si existe un valor en una columna específica.
		column_data: dict, {nombre_columna: valor} a validar
		Retorna: dict con {'exists': bool, 'ids': list}
		"""
		if not isinstance(column_data, dict) or len(column_data) != 1:
			raise ValueError("column_data debe ser un diccionario con una sola clave-valor")

		column_name = list(column_data.keys())[0]
		value = list(column_data.values())[0]

		if column_name not in self.columns:
			raise ValueError("La columna '{}' no existe en la tabla '{}'".format(column_name, self.table_name))

		sql = "SELECT ID FROM {} WHERE {} = ?".format(self.table_name, column_name)

		import system
		if self.dbConnection:
			result = system.db.runPrepQuery(sql, [value], self.dbConnection)
		else:
			result = system.db.runPrepQuery(sql, [value])

		ids = []
		if result and result.getRowCount() > 0:
			for row in range(result.getRowCount()):
				ids.append(result.getValueAt(row, 0))

		return {
			'exists': len(ids) > 0,
			'ids': ids
		}
