
from mes_core.sql import SQLTableBase
import system

class workOrderTable(SQLTableBase):
	def __init__(self, dbConnection=None):
		columns = {
			'ID': 'int',
			'ScheduleID': 'int',
			'RunStartDateTime': 'datetime',
			'RunStopDateTime': 'datetime',
			'Closed': 'tinyint',
			'Hide': 'tinyint',
			'TimeStamp': 'datetime',
			'ProductCodeID': 'int',
		}
		SQLTableBase.__init__(self, 'workorder', columns, dbConnection)

	def insert(self, workorder, quantity, productcodeid, closed=0, hide=0, timestamp=None):
		if timestamp is None:
			timestamp = system.date.now()
		values = {
			'WorkOrder': workorder,
			'Quantity': quantity,
			'ProductCodeID': productcodeid,
			'Closed': closed,
			'Hide': hide,
			'TimeStamp': timestamp,
		}
		SQLTableBase.insert(self, values)

	def selectID(self, workorder_id, columns=None):
		"""
		Select a work order by its ID.
		columns: list, optional list of specific columns to select
		"""
		return self.select('ID = ?', [workorder_id], columns)

	def updateID(self, workorder_id, set_values):
		self.update(set_values, 'ID = ?', [workorder_id])

	def deleteID(self, workorder_id):
		self.delete('ID = ?', [workorder_id])
		
	def show(self):
		"""
		Print columns and types for the workorder table.
		"""
		print("Tabla: workorder")
		print("-" * 50)
		for col_name, col_type in self.columns.items():
			print("{}: {}".format(col_name, col_type))
		print("-" * 50)
	  
	def selectAll(self, columns=None):
		"""
		Select all work orders with optional columns.
		columns: list, optional list of specific columns to select
		"""
		return self.select(columns=columns)
		
	def selectCustom(self, columns=None, where_clause=None, where_args=None):
		"""
		Custom SELECT on workorder table.
		columns: list of columns or None
		where_clause: SQL where clause (without WHERE)
		where_args: list of args for placeholders
		"""
		return SQLTableBase.select(self, where_clause, where_args, columns)


def pulling_excel_variables(nodeid,
                            dbConnection,
                            filePath =  "C:/Program Files/Inductive Automation/Ignition/Programa_de_inyeccion_Poly.xlsx",
                            sheetName = "CAJAS-CUB"):
    import re
    import mes_core
    from org.apache.poi.xssf.usermodel import XSSFWorkbook
    from java.io import FileInputStream
    from org.apache.poi.ss.usermodel import CellType, DateUtil, DataFormatter

    # -------------------------------------------------------
    # 1) Resolver linename (15) a partir del nodeid en la BD
    # -------------------------------------------------------
    nodeTable = mes_core.model.nodeTable(dbConnection)

    #  columna DisplayName'IMM 15'
    dsValue = nodeTable.selectID(nodeid, ["DisplayName"])

    if dsValue is None or dsValue.getRowCount() == 0:
        raise Exception("No se encontró el nodeID %s en la tabla node" % nodeid)

    displayName = dsValue.getValueAt(0, 0)
    if displayName is None:
        raise Exception("DisplayName nulo para nodeID %s" % nodeid)

    displayName = str(displayName).strip()

    # Extraer dígitos al final: 'IMM 15' -> '15'
    m = re.search(r'(\d+)\s*$', displayName)
    if m:
        linename = m.group(1)  # '15'
    else:
        # Fallback: si no hay número, usamos el texto completo
        linename = displayName

    # -------------------------------------------------------
    # 2) Abrir archivo Excel
    # -------------------------------------------------------
    file_in = FileInputStream(filePath)
    workbook = XSSFWorkbook(file_in)
    file_in.close()

    sheet = workbook.getSheet(sheetName)
    headerRow = sheet.getRow(5)  # Fila 6 (índice 5), donde están las INYECTORAS
    indexInyectora = -1

    # -------------------------------------------------------
    # 3) Helper para leer celdas sin evaluar fórmulas
    # -------------------------------------------------------
    df = DataFormatter()

    def cell_to_str(cell):
        if cell is None:
            return ""

        try:
            ct = cell.getCellType()
        except:
            ct = cell.getCellTypeEnum()

        def _format_date_if_needed():
            if DateUtil.isCellDateFormatted(cell):
                try:
                    return str(cell.getLocalDateTimeCellValue().toLocalDate())
                except:
                    return df.formatCellValue(cell).strip()
            return None

        if ct == CellType.FORMULA:
            try:
                rt = cell.getCachedFormulaResultType()
            except:
                rt = cell.getCachedFormulaResultTypeEnum()

            if rt == CellType.NUMERIC:
                date_s = _format_date_if_needed()
                if date_s is not None:
                    return date_s
                try:
                    return str(cell.getNumericCellValue())
                except:
                    return df.formatCellValue(cell).strip()

            elif rt == CellType.STRING:
                try:
                    return cell.getStringCellValue().strip()
                except:
                    return df.formatCellValue(cell).strip()

            elif rt == CellType.BOOLEAN:
                try:
                    return "TRUE" if cell.getBooleanCellValue() else "FALSE"
                except:
                    return df.formatCellValue(cell).strip()

            else:
                return df.formatCellValue(cell).strip()

        elif ct == CellType.NUMERIC:
            date_s = _format_date_if_needed()
            if date_s is not None:
                return date_s
            try:
                return str(cell.getNumericCellValue())
            except:
                return df.formatCellValue(cell).strip()

        elif ct == CellType.STRING:
            return cell.getStringCellValue().strip()

        elif ct == CellType.BOOLEAN:
            return "TRUE" if cell.getBooleanCellValue() else "FALSE"

        else:
            return df.formatCellValue(cell).strip()

    # -------------------------------------------------------
    # 4) Buscar la columna "INYECTORA {linename}"
    # -------------------------------------------------------
    if headerRow is not None:
        lastCol = headerRow.getLastCellNum()
        for columnIndex in range(0, lastCol):
            cell = headerRow.getCell(columnIndex)
            line = cell_to_str(cell)
            if not line:
                continue

            if line == ("INYECTORA " + str(linename)):
                indexInyectora = columnIndex
                break

    headers = ["Turno","Dia", "Code", "Horas Programadas", "Horas Acumuladas",
               "Cantidad Programada", "Programa Acumulado"]

    # Si no encontramos la columna de la inyectora, devolvemos dataset vacío
    if indexInyectora < 0:
        return system.dataset.toDataSet(headers, [])

    # Índices relativos a la inyectora encontrada
    COL_TURNO      = 3
    COL_DIA        = 4
    COL_COD        = indexInyectora - 1
    COL_HORAS_PROG = indexInyectora + 2
    COL_HORAS_ACUM = indexInyectora + 3
    COL_CANT_PROG  = indexInyectora + 4
    COL_PROG_ACUM  = indexInyectora + 5

    rows = []

    # -------------------------------------------------------
    # 5) Recorrer filas de datos
    # -------------------------------------------------------
    for rowIndex in range(8, 386):  # Fila 9 a 386
        r = sheet.getRow(rowIndex)
        if not r:
            continue

        def getCellStr(colIndex):
            return cell_to_str(r.getCell(colIndex))

        turno      = getCellStr(COL_TURNO)
        dia        = getCellStr(COL_DIA)
        cod        = getCellStr(COL_COD)
        horas_prog = getCellStr(COL_HORAS_PROG)
        horas_acum = getCellStr(COL_HORAS_ACUM)
        cant_prog  = getCellStr(COL_CANT_PROG)
        prog_acum  = getCellStr(COL_PROG_ACUM)

        if cod:  # Sólo guardar si hay SKU
            rows.append([turno, dia, cod, horas_prog, horas_acum, cant_prog, prog_acum])

    dataset = system.dataset.toDataSet(headers, rows)
    return dataset
'''  
##### ORIGINAL #####
def pulling_excel_variables(nodeid):
	from org.apache.poi.xssf.usermodel import XSSFWorkbook
	from java.io import FileInputStream
	from org.apache.poi.ss.usermodel import CellType, DateUtil, DataFormatter

	# Ruta del archivo
	original_path = "C:/Program Files/Inductive Automation/Ignition/Programa_de_inyeccion_Poly.xlsx"

	# Abrir archivo
	file_in = FileInputStream(original_path)
	workbook = XSSFWorkbook(file_in)
	file_in.close()

	# Hoja deseada
	sheet = workbook.getSheet("CAJAS-CUB")
	row = sheet.getRow(5)  # Fila 6 (índice 5)
	indexInyectora = -1

	# From id to inyectora's number
	if nodeid == 4:
		linename = "15"
	else:
		# Ajusta si usarás otros nodeid
		linename = "15"

	# ---- NUEVO: lector seguro de celdas SIN evaluar fórmulas ----
	df = DataFormatter()  # respeta el formato de la celda cuando apliquemos fallback

	def cell_to_str(cell):
		"""
		Convierte una celda a string SIN evaluar fórmulas:
		- Para FORMULA, usa el tipo de resultado en caché (cached result).
		- Para NUMERIC con formato fecha, devuelve yyyy-MM-dd.
		- Para el resto, usa DataFormatter como fallback.
		"""
		if cell is None:
			return ""

		try:
			ct = cell.getCellType()  # Enum CellType
		except:
			# Compatibilidad con versiones antiguas de POI:
			ct = cell.getCellTypeEnum()

		# Helper interno para fechas
		def _format_date_if_needed():
			if DateUtil.isCellDateFormatted(cell):
				# usa el valor de fecha basado en cache / numérico
				try:
					return str(cell.getLocalDateTimeCellValue().toLocalDate())  # yyyy-MM-dd
				except:
					# fallback al formateador
					return df.formatCellValue(cell).strip()
			return None

		if ct == CellType.FORMULA:
			# NO evaluar: usar el tipo de resultado en caché
			try:
				rt = cell.getCachedFormulaResultType()  # algunas versiones devuelven int
			except:
				rt = cell.getCachedFormulaResultTypeEnum()

			# Trata como si fuera ese tipo
			if rt == CellType.NUMERIC:
				# ¿Es fecha?
				date_s = _format_date_if_needed()
				if date_s is not None:
					return date_s
				# numérico estándar
				try:
					return str(cell.getNumericCellValue())
				except:
					return df.formatCellValue(cell).strip()

			elif rt == CellType.STRING:
				try:
					return cell.getStringCellValue().strip()
				except:
					return df.formatCellValue(cell).strip()

			elif rt == CellType.BOOLEAN:
				try:
					return "TRUE" if cell.getBooleanCellValue() else "FALSE"
				except:
					return df.formatCellValue(cell).strip()

			else:
				# BLANK, ERROR u otros -> usa formatter
				return df.formatCellValue(cell).strip()

		elif ct == CellType.NUMERIC:
			date_s = _format_date_if_needed()
			if date_s is not None:
				return date_s
			# numérico normal
			try:
				return str(cell.getNumericCellValue())
			except:
				return df.formatCellValue(cell).strip()

		elif ct == CellType.STRING:
			return cell.getStringCellValue().strip()

		elif ct == CellType.BOOLEAN:
			return "TRUE" if cell.getBooleanCellValue() else "FALSE"

		else:
			# BLANK, ERROR, etc.
			return df.formatCellValue(cell).strip()

	# ---- Buscar el índice de la INYECTORA en la fila 6 sin evaluar fórmulas ----
	for columnIndex in range(0, 100):
		cell = row.getCell(columnIndex)
		line = cell_to_str(cell)
		if not line:
			continue

		# Debug opcional
		# print("Col %d: %s" % (columnIndex, line))

		if line == ("INYECTORA " + linename):
			indexInyectora = columnIndex
			break

	# Validación básica
	if indexInyectora < 0:
		# Evita índices negativos y explica el problema
		headers = ["Turno","Dia", "Code", "Horas Programadas", "Horas Acumuladas", "Cantidad Programada", "Programa Acumulado"]
		return system.dataset.toDataSet(headers, [])  # o lanza una excepción controlada

	# Índices de columnas relativos a la inyectora encontrada
	COL_TURNO = 3
	COL_DIA = 4
	COL_COD = indexInyectora - 1
	COL_HORAS_PROG = indexInyectora + 2
	COL_HORAS_ACUM = indexInyectora + 3
	COL_CANT_PROG = indexInyectora + 4
	COL_PROG_ACUM = indexInyectora + 5

	headers = ["Turno","Dia", "Code", "Horas Programadas", "Horas Acumuladas", "Cantidad Programada", "Programa Acumulado"]
	rows = []

	for rowIndex in range(8, 386):  # Fila 9 a 386
		r = sheet.getRow(rowIndex)
		if not r:
			continue

		def getCellStr(colIndex):
			return cell_to_str(r.getCell(colIndex))

		# Obtener valores SIN evaluar fórmulas
		turno      = getCellStr(COL_TURNO)
		dia        = getCellStr(COL_DIA)
		cod        = getCellStr(COL_COD)
		horas_prog = getCellStr(COL_HORAS_PROG)
		horas_acum = getCellStr(COL_HORAS_ACUM)
		cant_prog  = getCellStr(COL_CANT_PROG)
		prog_acum  = getCellStr(COL_PROG_ACUM)

		if cod:  # Solo guardar si hay SKU
			rows.append([turno, dia, cod, horas_prog, horas_acum, cant_prog, prog_acum])

	dataset = system.dataset.toDataSet(headers, rows)
	# system.tag.writeBlocking(["[default]Ds_Inyectora_15"], [dataset])
	return dataset
'''

def ordering_dataset(nodeid,dbConnection,for_schedule=False):
	# Leer dataset
	datasetOriginal = mes_core.workOrder.pulling_excel_variables(int(nodeid),dbConnection)
	logger = system.util.getLogger("dau_ordering_dataset")
	# Columnas a excluir del nuevo dataset
	excluded_columns = ["Programa Acumulado", "Horas Acumuladas", "Cantidad", "Cantidad Programada"]
	columnNames = [col for col in datasetOriginal.getColumnNames() if col not in excluded_columns]
	columnTypes = [datasetOriginal.getColumnType(datasetOriginal.getColumnIndex(col)) for col in columnNames]

	# Agregar columnas nuevas
	columnNames.append("Cantidad")

	# Lista final
	nuevaLista = []

	# Variables de estado para la acumulación
	code_actual = None
	fila_acumulada = None
	acumulando = False  # Para controlar si estamos acumulando

	for fila in range(datasetOriginal.getRowCount()):
		code_val = datasetOriginal.getValueAt(fila, "Code")

		if for_schedule == False:
			# Validar si es numérico
			try:
				code_num = str(int(float(code_val)))
				es_numerico = True
			except:
				es_numerico = False

			if not es_numerico:
				# Fila no válida para acumulación → guardar acumulado anterior (si existe) y reiniciar
				if fila_acumulada is not None:
					nuevaLista.append(fila_acumulada)
					fila_acumulada = None
					code_actual = None
					acumulando = False
				continue
		else:
			# Validación personalizada para programación
			if code_val == "NP-8":
				if fila_acumulada is not None:
					nuevaLista.append(fila_acumulada)
					fila_acumulada = None
					code_actual = None
					acumulando = False
				continue
			else:
				code_num = code_val
				try:
					code_num = str(int(float(code_val)))
					
				except:
					code_num = code_val

		# Leer y convertir cantidad programada
		try:
			cant_prog = float(datasetOriginal.getValueAt(fila, "Cantidad Programada"))
		except:
			cant_prog = 0.0

		# Leer y convertir horas programadas
		try:
			horas_prog = float(datasetOriginal.getValueAt(fila, "Horas Programadas"))
		except:
			horas_prog = 0.0

		if code_actual is not None and code_num == code_actual and acumulando:
			# Mismo código consecutivo → acumular
			fila_acumulada[-2] += horas_prog
			fila_acumulada[-1] += cant_prog
		else:
			# Código nuevo o fin de secuencia → guardar lo acumulado
			if fila_acumulada is not None:
				nuevaLista.append(fila_acumulada)

			# Crear nueva fila
			fila_acumulada = []
			for col_name in columnNames[:-2]:  # Excluye "Horas Programadas" y "Cantidad"
				val = datasetOriginal.getValueAt(fila, col_name)
				if col_name == "Code":
					val = code_num  # aquí forzamos a que sea string sin .0
				fila_acumulada.append(val)

			fila_acumulada.append(horas_prog)
			fila_acumulada.append(cant_prog)

		# Actualizar el estado
		code_actual = code_num
		acumulando = True

	# Agregar última fila pendiente
	if fila_acumulada is not None:
		nuevaLista.append(fila_acumulada)

	# Crear el nuevo dataset
	datasetOrdenado = system.dataset.toDataSet(columnNames, nuevaLista)

	#system.tag.writeBlocking("[default]Ds_WorkOrder_15", datasetOrdenado)

	return datasetOrdenado

def calcular_fechas(nodeid,dbConnection):
	import java.text.SimpleDateFormat as SimpleDateFormat
	import java.util.Calendar as Calendar
	import java.util.Date as Date
	
	dataset=mes_core.workOrder.ordering_dataset(nodeid = nodeid, dbConnection = dbConnection, for_schedule=True)
	logger = system.util.getLogger("dau_calcular_fechas")
	# Paso 1: Calcular fechas inicio y fin
	horarios_turno = {
		1.0: (22, 0),
		2.0: (6, 0),
		3.0: (14, 0)
	}
	formato_fecha = SimpleDateFormat("yyyy-MM-dd")
	fechas_resultado = []

	fecha_fin_anterior = None
	turno_anterior = None

	for fila in range(dataset.getRowCount()):
		raw_dia = dataset.getValueAt(fila, "Dia")
		turno = float(dataset.getValueAt(fila, "Turno"))
		horas_prog = float(dataset.getValueAt(fila, "Horas Programadas"))

		# Convertir a tipo Date si es necesario
		if isinstance(raw_dia, Date):
			dia = raw_dia
		else:
			try:
				dia = formato_fecha.parse(str(raw_dia))
			except:
				# Si falla la conversión, omitir
				continue

		# Calcular fecha de inicio
		if fila == 0 or turno != turno_anterior:
			hora, minuto = horarios_turno.get(turno, (6, 0))
			c = Calendar.getInstance()
			c.setTime(dia)
			c.set(Calendar.HOUR_OF_DAY, hora)
			c.set(Calendar.MINUTE, minuto)
			c.set(Calendar.SECOND, 0)
			fecha_inicio = c.getTime()
		else:
			fecha_inicio = fecha_fin_anterior

		# Calcular fecha de fin
		millis_duracion = int(horas_prog * 3600 * 1000)
		c = Calendar.getInstance()
		c.setTime(fecha_inicio)
		c.add(Calendar.MILLISECOND, millis_duracion)
		fecha_fin = c.getTime()

		fechas_resultado.append([fecha_inicio, fecha_fin])
		fecha_fin_anterior = fecha_fin
		turno_anterior = turno

	# Paso 2: Extraer columnas Code y Cantidad
	col_code = dataset.getColumnIndex("Code")
	col_cantidad = dataset.getColumnIndex("Cantidad")

	datos_finales = []

	for i in range(dataset.getRowCount()):
		code = dataset.getValueAt(i, col_code)
		cant = dataset.getValueAt(i, col_cantidad)
		fecha_inicio, fecha_fin = fechas_resultado[i]
		datos_finales.append([code, cant, fecha_inicio, fecha_fin])

	# Paso 3: Crear dataset resultante
	columnas = ["Code", "Cantidad", "Fecha Inicio", "Fecha Fin"]
	return system.dataset.toDataSet(columnas, datos_finales)


	def es_duplicado(excel_order, existing_orders, tolerance_ms=5000):
	    """Compara la orden de Excel con las órdenes existentes y verifica duplicados con tolerancia."""
	    for order in existing_orders:
	        if excel_order['Code'] == order['Code'] and excel_order['Cantidad Programada'] == order['Cantidad Programada']:
	            # Convertir fechas a timestamps
	            fecha_inicio_excel = pd.to_datetime(excel_order['Dia'])
	            fecha_inicio_existing = pd.to_datetime(order['ScheduleStartDateTime'])
	            delta_inicio = abs((fecha_inicio_excel - fecha_inicio_existing).total_seconds() * 1000)  # en milisegundos
	            
	            fecha_fin_excel = fecha_inicio_excel + pd.Timedelta(hours=excel_order['Horas Programadas'])
	            fecha_fin_existing = pd.to_datetime(order['ScheduleFinishDateTime'])
	            delta_fin = abs((fecha_fin_excel - fecha_fin_existing).total_seconds() * 1000)  # en milisegundos
	
	            if delta_inicio <= tolerance_ms and delta_fin <= tolerance_ms:
	                return True  # Es un duplicado
	    return False  # No es un duplicado

	

def writeData2Database(nodeid, prevDataset, db='mes_core'):
	"""
	Genera un dataset de órdenes a partir de calcular_fechas(),
	lo filtra para evitar duplicados en Schedule y SKU no creados,
	y opcionalmente inserta las órdenes nuevas a la base de datos.
	"""
	
	logger = system.util.getLogger("dau_writeData2Database")
	logger.info("=== writeData2Database iniciado ===")
	logger.info("Parámetros -> nodeid: %s | db: %s" % (str(nodeid), str(db)))
	
	try:
		# --- Función auxiliar: Filtrar 'Code' numérico ---
		def filtrar_numericos(dataset):
			colNames = list(dataset.getColumnNames())
			newRows = []
			for row in range(dataset.getRowCount()):
				code = str(dataset.getValueAt(row, "Code"))
				try:
					float(code)
					newRows.append([dataset.getValueAt(row, col) for col in colNames])
				except:
					pass
			return system.dataset.toDataSet(colNames, newRows)

		# --- 1) Dataset inicial desde calcular_fechas() ---
		logger.info("Paso 1 - Ejecutando mes_core.workOrder.calcular_fechas() ...")
		scheduleDataset = mes_core.workOrder.calcular_fechas(nodeid = nodeid, dbConnection = db)
		logger.info("Dataset inicial recibido: %d filas" % scheduleDataset.getRowCount())

		filteredDataset = filtrar_numericos(scheduleDataset)
		logger.info("Filtrado numérico aplicado: %d filas válidas" % filteredDataset.getRowCount())

		# --- Tablas necesarias ---
		tableProduct = mes_core.model.productcodeTable(db)
		tablePCL = mes_core.model.productcodelineTable(db)
		tableSR = mes_core.model.standardrateTable(db)
		tableSCH = mes_core.schedule.scheduleTable(db)
		table = mes_core.workOrder.workOrderTable(db)

		# --- 2) Obtener Schedule actual de la línea ---
		logger.info("Paso 2 - Consultando Schedule actual para NodeID=%s ..." % str(nodeid))
		currentScheduleDS = tableSCH.selectCustom(
			["WorkOrderID", "ScheduleStartDateTime", "ScheduleFinishDateTime"],
			where_clause="NodeID = ?",
			where_args=[nodeid]
		)
		startDatesSch = [currentScheduleDS.getValueAt(r, "ScheduleStartDateTime")
						 for r in range(currentScheduleDS.getRowCount())]
		logger.info("Fechas en Schedule actual: %d registros" % len(startDatesSch))

		# --- 3) Filtro 1: Remover duplicados por fecha/hora ---
		TOLERANCE_MS = 1000
		logger.info("Paso 3 - Aplicando filtro de duplicados con tolerancia ±%dms" % TOLERANCE_MS)

		startDatesSch_ms = []
		for d in startDatesSch:
			try:
				startDatesSch_ms.append(long(d.getTime()))
			except:
				startDatesSch_ms.append(long(d))

		def es_duplicado_con_tolerancia(fecha_nueva, fechas_ms, tol_ms):
			try:
				t_new = long(fecha_nueva.getTime())
			except:
				t_new = long(fecha_nueva)
			for t_exist in fechas_ms:
				diff = t_new - t_exist
				if abs(diff) <= tol_ms:
					return True, diff
			return False, 0

		dataForWriting = []
		headers = list(filteredDataset.getColumnNames())

		try:
			colIdxFecha = filteredDataset.getColumnIndex("ScheduleStartDateTime")
		except:
			colIdxFecha = 2  # fallback

		for r in range(filteredDataset.getRowCount()):
			fecha_inicio = filteredDataset.getValueAt(r, colIdxFecha)
			duplicado, delta_ms = es_duplicado_con_tolerancia(fecha_inicio, startDatesSch_ms, TOLERANCE_MS)
			if duplicado:
				logger.debug("Fila %d omitida por duplicado (Δ=%d ms)" % (r, delta_ms))
				continue
			else:
				fila_completa = [filteredDataset.getValueAt(r, c) for c in range(filteredDataset.getColumnCount())]
				dataForWriting.append(fila_completa)

		logger.info("Filas tras filtro de duplicados: %d" % len(dataForWriting))
		if len(dataForWriting) > 0:
			logger.debug("Ejemplo de fila a insertar: %s" % str(dataForWriting[0]))

		# --- 4) Filtro 2: SKU existente y con StandardRate ---
		logger.info("Paso 4 - Verificando existencia de SKU y StandardRate...")
		productCodesIds = []
		notCreated = []
		dataWithoutSKU = []

		for fila in dataForWriting:
			sku = fila[0]
			try:
				result = tableProduct.selectCustom(["ID"], where_clause="ProductCode = ?", where_args=[str(sku)])
				value = result.getValueAt(0, 0)
				resultLine = tablePCL.selectCustom(["ID"], where_clause="ProductCodeID = ?", where_args=[value])
				PCLid = resultLine.getValueAt(0, 0)
				resultSR = tableSR.selectCustom(["ID"], where_clause="ProductCodeID = ?", where_args=[value])
				SRid = resultSR.getValueAt(0, 0)
				productCodesIds.append(value)
			except:
				logger.warn("SKU no encontrado o sin StandardRate: %s" % str(sku))
				productCodesIds.append(None)
				notCreated.append(sku)

		for i in range(len(dataForWriting)):
			if productCodesIds[i] != None:
				dataWithoutSKU.append(dataForWriting[i])

		logger.info("Filas válidas con SKU existente: %d" % len(dataWithoutSKU))
		if len(notCreated) > 0:
			logger.warn("SKU sin crear: %s" % str(notCreated))

		# --- 5) Comparar contra dataset previo ---
		logger.info("Paso 5 - Comparando con dataset previo...")

		def datasets_iguales(ds1, ds2):
			if ds1.getColumnCount() != ds2.getColumnCount() or ds1.getRowCount() != ds2.getRowCount():
				return False
			for r in range(ds1.getRowCount()):
				for c in range(ds1.getColumnCount()):
					if ds1.getValueAt(r, c) != ds2.getValueAt(r, c):
						return False
			return True

		newDataset = system.dataset.toDataSet(headers, dataWithoutSKU)

		if datasets_iguales(prevDataset, newDataset):
			logger.info("Dataset idéntico al previo. No se realizan inserciones.")
			return 0, newDataset
		else:
			logger.info("Dataset nuevo detectado. Insertando en base de datos...")
			for i in range(len(dataForWriting)):
				if productCodesIds[i] != None:
					try:
						table.insert(
							dataForWriting[i][0],
							dataForWriting[i][1],
							productCodesIds[i],
							0, 0, None
						)
					except:
						logger.error("Error insertando fila %d con SKU=%s" % (i, str(dataForWriting[i][0])))

			system.tag.writeBlocking(
				"[UNS]Clarios/Pacifico/Cubiertas/IMM 15/UI/Schedule/Dataset_excel", newDataset
			)
			logger.info("Tag Dataset_excel actualizado correctamente.")
			logger.info("=== writeData2Database finalizado con éxito ===")
			return notCreated, newDataset

	except Exception as e:
		logger.error("Error en writeData2Database: %s" % str(e))
		import traceback
		logger.error(traceback.format_exc())
		return None, None
