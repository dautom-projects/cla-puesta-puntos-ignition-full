#* DAUTOM SAS CONFIDENTIAL
#*_________________________
#*
#* [2013] - [2025] DAUTOM SAS
#* All Rights Reserved.
#*
#* NOTICE: All information contained herein is, and remains the property
#* of DAUTOM SAS and its suppliers, if any. The intellectual and 
#* technical concepts contained herein are proprietary to DAUTOM SAS
#* and its suppliers and may be covered by U.S and Foreign Patents, 
#* patents in process, and are protected by trade secret or copyright law. 
#* Dissemination of this information or reproduction of this material
#* is strictly forbidden unless prior written permission is obtained
#* from DAUTOM SAS.

def printDatasetresultado(dataset):
	"""
	Prints the dataset in a structured format with column names and rows.
	:param dataset: Ignition dataset (BasicDataset, PyDataSet)
	"""
	if dataset is None:
		print("Dataset is None")
		return
	# Get column names
	columnNames = dataset.getColumnNames()
	# Print header
	header = " | ".join(columnNames)
	print(header)
	print("-" * len(header))
	# Print each row
	for row in range(dataset.getRowCount()):
		values = [str(dataset.getValueAt(row, col)) for col in range(dataset.getColumnCount())]
		print(" | ".join(values))
		
def secondsToMinutes(seconds):
    minutes = round(seconds / 60)
    return minutes
    
def format_datetime(date, format):
	"""Formatea un objeto Date en formato 'yyyy-MM-dd HH:mm' para Ignition."""	
	if date is None:
		return None
		
	return system.date.format(date, format)
	
	
	
def generate_tree_for_administration(db):
	true = True
	false = False

	# 1. Consultar todos los nodos excepto enterprise
	query = """
		SELECT ID, Name, Type, ParentNodeID
		FROM node
		WHERE Type != 'ENTERPRISE'
	"""
	results = system.db.runQuery(query, db)

	# 2. Construir mapa de nodos
	nodes = {}
	for row in results:
		nodes[row["ID"]] = {
			"id": row["ID"],
			"label": row["Name"],
			"type": row["Type"],
			"parent": row["ParentNodeID"],
			"children": []
		}

	# 3. Armar relaciones padre-hijo
	rootSites = []
	for node in nodes.values():
		if node["parent"] not in nodes:  # si su padre no está (era enterprise), es raíz
			rootSites.append(node)
		else:
			nodes[node["parent"]]["children"].append(node)

	# 4. Convertir a formato Tree Navigator
	def toTreeNode(node):
		return {
			"label": node["label"],
			"expanded": true,
			"icon": {
				"path": "material/brightness_5" if node["type"] == "LINE" else "",
				"color": "--cla-text-data",
				"style": {}
			},
			"data": {
				"nodeID": node["id"],
				"nodeType": node["type"],
				"nodeName": node["label"]
			},
			"items": [toTreeNode(child) for child in node["children"]]
		}

	# 5. Raíz Enterprise fijo
	root = {
		"label": "Clarios",
		"expanded": true,
		"items": [toTreeNode(site) for site in rootSites]
	}

	# 6. Retornar JSON listo
	return system.util.jsonEncode(root)

# seconds to minutes
def secondsToMinutes(seconds):
    minutes = round(seconds / 60)
    return minutes


from java.util import Date
from java.text import SimpleDateFormat

def makeDateTime(dateTime=None, YYYY=None, MM=None, DD=None, hh=None, mm=None, ss=None, ms=None, output='datetime', pattern='yyyy-MM-dd HH:mm:ss.SSS'):
	"""
	Builds a datetime from a base date and selective overrides (including milliseconds),
	returning a datetime, a formatted string, or both. No 'system' dependency (safe if 'system' is shadowed).

	Behavior:
		- Uses 'dateTime' as base. If None, uses Date() (now).
		- Replaces provided components (YYYY, MM, DD, hh, mm, ss, ms).
		- 'MM' accepts 1–12 (human) or 0–11 (Java index pass-through).
		- Constructs the result via java.util.Date epoch arithmetic.

	Parameters:
		dateTime (Date, optional): Base datetime. Default: None (current time).
		YYYY (int, optional): Year override (e.g., 2025). Default: None (keep base).
		MM (int, optional): Month override; 1–12 or 0–11. Default: None (keep base).
		DD (int, optional): Day of month (1–31). Default: None (keep base).
		hh (int, optional): Hour 0–23. Default: None (keep base).
		mm (int, optional): Minute 0–59. Default: None (keep base).
		ss (int, optional): Second 0–59. Default: None (keep base).
		ms (int, optional): Millisecond 0–999. Default: None (keep base).
		output (str, optional): 'datetime' | 'string' | 'both'. Default: 'datetime'.
		pattern (str, optional): SimpleDateFormat for string. Default: 'yyyy-MM-dd HH:mm:ss.SSS'.

	Returns:
		java.util.Date | str | dict:
			- 'datetime' -> java.util.Date
			- 'string'   -> formatted str with 'pattern'
			- 'both'     -> {'datetime': Date, 'string': str}

	Examples:
		# Get "2025-10-02 00:00:00.000" as string (month preserved if MM not passed)
		# makeDateTime(dateTime=Date(), YYYY=2025, DD=2, hh=0, mm=0, ss=0, ms=0, output='string')

		# Both outputs, fixing only time:
		# makeDateTime(dateTime=value, hh=7, mm=0, ss=0, ms=0, output='both')
	"""
	try:
		# Base datetime
		baseDt = dateTime if dateTime is not None else Date()

		# Current components from baseDt (deprecated getters but reliable in Jython)
		curY = baseDt.getYear() + 1900
		curM0 = baseDt.getMonth()          # 0-11
		curD = baseDt.getDate()
		curH = baseDt.getHours()
		curMin = baseDt.getMinutes()
		curSec = baseDt.getSeconds()
		curMs = int(baseDt.getTime() % 1000)

		# Overrides
		newY = curY if YYYY is None else int(YYYY)
		if MM is None:
			newM0 = curM0
		else:
			m = int(MM)
			newM0 = (m - 1) if m >= 1 else m  # accept 1–12, pass-through 0–11
		newD = curD if DD is None else int(DD)
		newH = curH if hh is None else int(hh)
		newMin = curMin if mm is None else int(mm)
		newSec = curSec if ss is None else int(ss)
		newMs = curMs if ms is None else int(ms)

		# Build date at local midnight for Y-M-D, then add time + ms
		dtMidnight = Date(newY - 1900, newM0, newD)  # 00:00:00.000 local
		epoch = dtMidnight.getTime() + (newH * 3600000) + (newMin * 60000) + (newSec * 1000) + newMs
		dtFull = Date(epoch)

		if output == 'string':
			return SimpleDateFormat(pattern).format(dtFull)
		elif output == 'both':
			return {'datetime': dtFull, 'string': SimpleDateFormat(pattern).format(dtFull)}
		return dtFull

	except:
		# Fallback: now()
		nowDt = Date()
		if output == 'string':
			return SimpleDateFormat(pattern).format(nowDt)
		elif output == 'both':
			return {'datetime': nowDt, 'string': SimpleDateFormat(pattern).format(nowDt)}
		return nowDt

