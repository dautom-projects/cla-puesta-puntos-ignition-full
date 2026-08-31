def bk():
    """
    Export SQL Server database schema and data to SQL file.
    
    This script reads all tables from a database and generates:
    - CREATE TABLE statements with columns, data types, and constraints
    - INSERT statements for all data
    - Saves result to a .sql file
    
    Tables in excludedTables are skipped entirely (no CREATE TABLE, no data),
    so restore() never touches whatever already exists for them in the
    destination database.
    
    Version: 1.1.0
    
    Returns:
        str: Path to the generated SQL file
    
    Changelog:
        2026-07-30 | William M. | v1.1.0 - excludedTables now fully skips
            schema (DROP/CREATE) too, not just data - previously the table
            was still recreated empty on restore(), wiping any existing
            destination data for it
        2026-07-06 | - | v1.0.0 - Original version
    """
    
    logger = system.util.getLogger("scriptConsole/schemaExport")
    
    try:
        # ==========================================
        # CONFIGURATION - MODIFY THESE VARIABLES
        # ==========================================
        
        # Database connection name (configured in Ignition Gateway)
        dbConnection = "papo_db"
        
        # Tables to exclude completely (no schema, no data) from the export
        # Example: excludedTables = ["registerhistory", "audit_log"]
        #excludedTables = []
        excludedTables = ["registerhistory", "roles", "scada_roles", "scada_user_ci", "scada_user_ex", "scada_user_rl", "scada_user_sa", "scada_users", "sysdiagrams","user_roles", "users"]
        #Output file path - CHANGE THIS to your preferred location
        #outputFilePath = "C:/Users/A1000625/Downloads/database_{}_export.sql".format(dbConnection)
        #outputFilePath = "C:/Users/gerso/Downloads/database_{}_export.sql".format(dbConnection)
        
        outputFilePath = "G:/Shared drives/CLA/Proyectos/2026-05-21 - CLA - Puesta a Puntos/04 - Software/08 - Database\database_{}_export_dev.sql".format(dbConnection)
		
        # ==========================================
        # SCRIPT EXECUTION - DO NOT MODIFY
        # ==========================================
        
        # Output script storage
        sqlScript = []
        sqlScript.append("-- =====================================================")
        sqlScript.append("-- SQL Server Schema Export")
        sqlScript.append("-- Source Database: " + dbConnection)
        sqlScript.append("-- Generated: " + str(system.date.now()))
        sqlScript.append("-- =====================================================")
        sqlScript.append("")
        
        print "Starting database export..."
        print "Source database: " + dbConnection
        print "Output file: " + outputFilePath
        print ""
        
        # Get all tables in schema
        tableQuery = """
            SELECT 
                TABLE_NAME
            FROM 
                INFORMATION_SCHEMA.TABLES
            WHERE 
                TABLE_TYPE = 'BASE TABLE'
                AND TABLE_SCHEMA = 'dbo'
            ORDER BY 
                TABLE_NAME
        """
        
        tables = system.db.runQuery(tableQuery, database=dbConnection)
        
        logger.info("Found " + str(len(tables)) + " tables to export")
        print "Found " + str(len(tables)) + " tables to export"
        print ""
        
        # Process each table
        tableCount = 0
        totalRows = 0
        excludedLower = [t.lower() for t in excludedTables]
        
        for tableRow in tables:
            tableCount += 1
            tableName = tableRow['TABLE_NAME']
            
            logger.info("Processing table " + str(tableCount) + "/" + str(len(tables)) + ": " + tableName)
            print "Processing table " + str(tableCount) + "/" + str(len(tables)) + ": " + tableName
            
            # Skip excluded tables entirely - no schema, no data - so restore()
            # never drops/recreates them and whatever exists in the destination survives
            if tableName.lower() in excludedLower:
                logger.info("Table " + tableName + " fully excluded (schema and data)")
                print "  - Table fully excluded (schema and data)"
                sqlScript.append("")
                sqlScript.append("-- Table " + tableName + " fully excluded (schema and data)")
                sqlScript.append("")
                continue
            
            # Get table structure
            columnQuery = """
                SELECT 
                    COLUMN_NAME,
                    DATA_TYPE,
                    CHARACTER_MAXIMUM_LENGTH,
                    NUMERIC_PRECISION,
                    NUMERIC_SCALE,
                    IS_NULLABLE,
                    COLUMN_DEFAULT
                FROM 
                    INFORMATION_SCHEMA.COLUMNS
                WHERE 
                    TABLE_NAME = ?
                    AND TABLE_SCHEMA = 'dbo'
                ORDER BY 
                    ORDINAL_POSITION
            """
            
            columns = system.db.runPrepQuery(columnQuery, [tableName], database=dbConnection)
            
            # Get primary key
            pkQuery = """
                SELECT 
                    COLUMN_NAME
                FROM 
                    INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                WHERE 
                    OBJECTPROPERTY(OBJECT_ID(CONSTRAINT_SCHEMA + '.' + CONSTRAINT_NAME), 'IsPrimaryKey') = 1
                    AND TABLE_NAME = ?
                    AND TABLE_SCHEMA = 'dbo'
                ORDER BY 
                    ORDINAL_POSITION
            """
            
            primaryKeys = system.db.runPrepQuery(pkQuery, [tableName], database=dbConnection)
            pkColumns = [row['COLUMN_NAME'] for row in primaryKeys]
            
            # Check for IDENTITY columns
            identityQuery = """
                SELECT 
                    COLUMN_NAME,
                    IDENT_SEED(TABLE_SCHEMA + '.' + TABLE_NAME) AS seed_value,
                    IDENT_INCR(TABLE_SCHEMA + '.' + TABLE_NAME) AS increment_value
                FROM 
                    INFORMATION_SCHEMA.COLUMNS
                WHERE 
                    TABLE_NAME = ?
                    AND TABLE_SCHEMA = 'dbo'
                    AND COLUMNPROPERTY(OBJECT_ID(TABLE_SCHEMA + '.' + TABLE_NAME), COLUMN_NAME, 'IsIdentity') = 1
            """
            
            identityColumns = system.db.runPrepQuery(identityQuery, [tableName], database=dbConnection)
            identityColumnNames = [row['COLUMN_NAME'] for row in identityColumns]
            
            # Build CREATE TABLE statement
            sqlScript.append("")
            sqlScript.append("-- =====================================================")
            sqlScript.append("-- Table: " + tableName)
            sqlScript.append("-- =====================================================")
            sqlScript.append("IF OBJECT_ID('dbo." + tableName + "', 'U') IS NOT NULL")
            sqlScript.append("\tDROP TABLE dbo." + tableName + ";")
            sqlScript.append("GO")
            sqlScript.append("")
            sqlScript.append("CREATE TABLE dbo." + tableName + " (")
            
            # Build column definitions
            columnDefs = []
            for col in columns:
                colName = col['COLUMN_NAME']
                dataType = col['DATA_TYPE'].upper()
                isNullable = col['IS_NULLABLE']
                colDefault = col['COLUMN_DEFAULT']
                
                # Build data type with precision/scale
                if dataType in ['VARCHAR', 'NVARCHAR', 'CHAR', 'NCHAR']:
                    maxLength = col['CHARACTER_MAXIMUM_LENGTH']
                    if maxLength == -1:
                        dataType += "(MAX)"
                    else:
                        dataType += "(" + str(maxLength) + ")"
                
                elif dataType in ['DECIMAL', 'NUMERIC']:
                    precision = col['NUMERIC_PRECISION']
                    scale = col['NUMERIC_SCALE']
                    if precision is not None and scale is not None:
                        dataType += "(" + str(precision) + "," + str(scale) + ")"
                
                # Build full column definition
                colDef = "\t[" + colName + "] " + dataType
                
                # Add IDENTITY if applicable
                if colName in identityColumnNames and len(identityColumns) > 0:
                    seedValue = identityColumns[0]['seed_value']
                    incrementValue = identityColumns[0]['increment_value']
                    if seedValue is not None and incrementValue is not None:
                        colDef += " IDENTITY(" + str(int(seedValue)) + "," + str(int(incrementValue)) + ")"
                
                # Add NULL/NOT NULL
                if isNullable == 'NO':
                    colDef += " NOT NULL"
                else:
                    colDef += " NULL"
                
                # Add DEFAULT constraint
                if colDefault is not None:
                    cleanDefault = str(colDefault).strip()
                    colDef += " DEFAULT " + cleanDefault
                
                columnDefs.append(colDef)
            
            # Add primary key constraint
            if len(pkColumns) > 0:
                pkConstraint = "\tCONSTRAINT [PK_" + tableName + "] PRIMARY KEY ("
                pkConstraint += ", ".join(["[" + pk + "]" for pk in pkColumns])
                pkConstraint += ")"
                columnDefs.append(pkConstraint)
            
            # Join all column definitions
            sqlScript.append(",\n".join(columnDefs))
            sqlScript.append(");")
            sqlScript.append("GO")
            sqlScript.append("")
            
            # Export data
            # Get row count
            countQuery = "SELECT COUNT(*) AS [totalRows] FROM [dbo].[" + tableName + "]"
            countResult = system.db.runQuery(countQuery, database=dbConnection)
            rowCount = countResult[0]['totalRows']
            
            if rowCount > 0:
                logger.info("Exporting " + str(rowCount) + " rows from " + tableName)
                print "  - Exporting " + str(rowCount) + " rows"
                
                totalRows += rowCount
                
                sqlScript.append("-- Data for table: " + tableName)
                sqlScript.append("-- Total rows: " + str(rowCount))
                sqlScript.append("")
                
                # Only use IDENTITY_INSERT if table has IDENTITY columns
                hasIdentity = len(identityColumnNames) > 0
                
                if hasIdentity:
                    sqlScript.append("SET IDENTITY_INSERT [dbo].[" + tableName + "] ON;")
                    sqlScript.append("GO")
                    sqlScript.append("")
                
                # Get all data
                dataQuery = "SELECT * FROM [dbo].[" + tableName + "]"
                data = system.db.runQuery(dataQuery, database=dbConnection)
                
                # Build INSERT statements
                columnNames = [col['COLUMN_NAME'] for col in columns]
                columnList = ", ".join(["[" + col + "]" for col in columnNames])
                
                # Process in batches of 100 rows
                batchSize = 100
                for i in range(0, len(data), batchSize):
                    batch = data[i:i+batchSize]
                    
                    sqlScript.append("INSERT INTO [dbo].[" + tableName + "] (" + columnList + ")")
                    sqlScript.append("VALUES")
                    
                    valueSets = []
                    for row in batch:
                        values = []
                        for colName in columnNames:
                            value = row[colName]
                            
                            # Handle NULL
                            if value is None:
                                values.append("NULL")
                            
                            # Handle strings (escape single quotes)
                            elif isinstance(value, (str, unicode)):
                                escapedValue = value.replace("'", "''")
                                escapedValue = escapedValue.replace('\r', '').replace('\n', ' ')
                                values.append("N'" + escapedValue + "'")
                            
                            # Handle dates
                            elif hasattr(value, 'getTime'):
                                dateStr = system.date.format(value, "yyyy-MM-dd HH:mm:ss.SSS")
                                values.append("'" + dateStr + "'")
                            
                            # Handle booleans
                            elif isinstance(value, bool):
                                values.append("1" if value else "0")
                            
                            # Handle numbers
                            else:
                                values.append(str(value))
                        
                        valueSets.append("\t(" + ", ".join(values) + ")")
                    
                    # Join with comma and add semicolon
                    sqlScript.append(",\n".join(valueSets) + ";")
                    sqlScript.append("GO")
                    sqlScript.append("")
                
                if hasIdentity:
                    sqlScript.append("SET IDENTITY_INSERT [dbo].[" + tableName + "] OFF;")
                    sqlScript.append("GO")
                    sqlScript.append("")
            
            else:
                logger.info("Table " + tableName + " is empty")
                print "  - Table is empty (0 rows)"
                sqlScript.append("-- Table " + tableName + " is empty")
                sqlScript.append("")
        
        # Save to file
        sqlScript.append("")
        sqlScript.append("-- =====================================================")
        sqlScript.append("-- Export completed successfully")
        sqlScript.append("-- Total tables: " + str(len(tables)))
        sqlScript.append("-- Total rows exported: " + str(totalRows))
        sqlScript.append("-- =====================================================")
        
        completeScript = "\n".join(sqlScript)
        
        # Write to file
        print ""
        print "Writing to file..."
        
        fileHandle = open(outputFilePath, 'w')
        fileHandle.write(completeScript)
        fileHandle.close()
        
        logger.info("Export completed - Tables: " + str(len(tables)) + " - Rows: " + str(totalRows))
        
        print ""
        print "=========================================="
        print "EXPORT COMPLETED SUCCESSFULLY!"
        print "=========================================="
        print "Database: " + dbConnection
        print "Total tables: " + str(len(tables))
        print "Total rows exported: " + str(totalRows)
        print "File saved to: " + outputFilePath
        print "=========================================="
        
        return outputFilePath
    
    except Exception as e:
        errorMsg = "Error exporting database: " + str(e)
        logger.error(errorMsg)
        print errorMsg
        return None

def restore():
	"""
	Import a SQL Server schema+data backup produced by bk() into a database,
	replacing every table the backup file contains.

	Drops all existing foreign keys on the target database first (the bk()
	export never captures them, so the restored schema won't have any
	either), then splits the backup file on standalone "GO" lines and
	executes each resulting batch (DROP TABLE / CREATE TABLE / INSERT)
	against the target connection. Shows a confirm dialog before touching
	anything, since this is destructive and cannot be undone.

	Returns:
		bool: True if every batch executed without error, False otherwise.
	"""

	logger = system.util.getLogger("scriptConsole/schemaImport")

	try:
		# ==========================================
		# CONFIGURATION - MODIFY THESE VARIABLES
		# ==========================================

		dbConnection = "papo_db"
		inputFilePath = "C:/Users/A1000625/Downloads/database_papo_db_export.sql"

		# ==========================================
		# SCRIPT EXECUTION - DO NOT MODIFY
		# ==========================================

		confirmed = system.gui.confirm(
			"Esto va a BORRAR y reemplazar TODAS las tablas de '" + dbConnection + "' " +
			"con el contenido de:\n" + inputFilePath + "\n\n" +
			"Tambien se eliminaran todas las foreign keys existentes " +
			"(el backup no las incluye). Esta accion NO se puede deshacer.\n\n" +
			"Continuar?",
			"Confirmar restauracion de base de datos"
		)
		if not confirmed:
			print "Import cancelled by user"
			return False

		print "Reading backup file..."
		print "Source file: " + inputFilePath
		print "Target database: " + dbConnection
		print ""

		fileHandle = open(inputFilePath, 'r')
		fileContent = fileHandle.read()
		fileHandle.close()

		# Drop existing foreign keys so DROP TABLE order doesn't matter
		print "Dropping existing foreign keys on " + dbConnection + "..."
		fkQuery = """
			SELECT
				fk.name AS constraintName,
				OBJECT_NAME(fk.parent_object_id) AS tableName
			FROM sys.foreign_keys fk
		"""
		foreignKeys = system.db.runQuery(fkQuery, database=dbConnection)

		for fk in foreignKeys:
			dropFkSql = "ALTER TABLE [dbo].[" + fk['tableName'] + "] DROP CONSTRAINT [" + fk['constraintName'] + "];"
			system.db.runUpdateQuery(dropFkSql, database=dbConnection)

		print "Dropped " + str(len(foreignKeys)) + " foreign key(s)"
		print ""

		# Split file into batches on standalone "GO" lines
		rawLines = fileContent.split("\n")
		batches = []
		currentBatch = []

		for line in rawLines:
			if line.strip().upper() == "GO":
				if currentBatch:
					batches.append("\n".join(currentBatch))
					currentBatch = []
			else:
				currentBatch.append(line)

		if currentBatch:
			batches.append("\n".join(currentBatch))

		print "Executing " + str(len(batches)) + " batches..."
		print ""

		executedCount = 0
		errorCount = 0

		for i in range(len(batches)):
			batch = batches[i]

			# Skip batches with no real SQL (blank lines / comments only)
			hasContent = False
			for line in batch.split("\n"):
				stripped = line.strip()
				if stripped and not stripped.startswith("--"):
					hasContent = True
					break

			if not hasContent:
				continue

			try:
				system.db.runUpdateQuery(batch, database=dbConnection)
				executedCount += 1
			except Exception as batchError:
				errorCount += 1
				logger.error("Batch " + str(i) + " failed: " + str(batchError))
				print "  ERROR in batch " + str(i) + ": " + str(batchError)

			if (i + 1) % 200 == 0:
				print "  ... " + str(i + 1) + "/" + str(len(batches)) + " batches processed"

		logger.info("Import completed - Executed: " + str(executedCount) + " - Errors: " + str(errorCount))

		print ""
		print "=========================================="
		print "IMPORT COMPLETED"
		print "=========================================="
		print "Database: " + dbConnection
		print "Batches executed: " + str(executedCount)
		print "Batches with errors: " + str(errorCount)
		print "=========================================="

		return errorCount == 0

	except Exception as e:
		errorMsg = "Error importing database: " + str(e)
		logger.error(errorMsg)
		print errorMsg
		return False
		
##Biblioteca de querys
"""
INSERT INTO [dbo].[papo] (Description, Reference)
VALUES ('Mi descripción', 'MI-REF-001');
----------------------------------------------------------------------------
INSERT INTO [dbo].[papoitem] (AnswerType, Description, PapoID, RegisterTypeID)
VALUES 
    ('BOOL', 'Penetracion bandera hombro',1067, 7);
    
----------------------------------------------------------------------------
INSERT INTO [dbo].[papoitem_registertype] (PapoItemID, RegisterTypeID)
VALUES 
    (11011, 7);
 ----------------------------------------------------------------------------   
INSERT INTO [dbo].[node] (DisplayName, Name, ParentNodeID, Selectable, Topic, Type)
VALUES ('Mi Nodo', 'MI_NODO', NULL, 1, 'topic/ruta', 'LINE');
----------------------------------------------------------------------------
INSERT INTO [dbo].[nodepapo] (NodeID, PapoID)
VALUES (1, 1067);
----------------------------------------------------------------------------
INSERT INTO [dbo].[workstation] (Description, Hostname, IpAddress)
VALUES ('Mi Estacion', 'PC-PLANTA-01', '192.168.1.100');
----------------------------------------------------------------------------
INSERT INTO [dbo].[workstationnode] (NodeID, WorkstationID)
VALUES (1, 1);
----------------------------------------------------------------------------
INSERT INTO registerhistory (
	[Timestamp], DataAnswer, Status, PapoID, RegisterTypeID,
	[User], WorkstationNodeID, NodeID, WorkstationID, RegisterCode
)
SELECT
	GETDATE(), '{}', 'Sin Iniciar', np.PapoID, 12,
	'SYSTEM', wsn.ID, wsn.NodeID, wsn.WorkstationID, 0
FROM nodepapo np
JOIN workstationnode wsn ON wsn.NodeID = np.NodeID
WHERE NOT EXISTS (
	SELECT 1 FROM registerhistory rh
	WHERE rh.PapoID = np.PapoID AND rh.WorkstationNodeID = wsn.ID
);