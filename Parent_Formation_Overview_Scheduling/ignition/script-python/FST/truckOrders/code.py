#Shared paths/constants/etc
TRUCK_PATH = "[default]Formation/Tables/Schedule/currentTruckOrders"
SCHEDULE_PATH = "[default]Formation/Tables/Schedule/currentScheduleFromExcel"


def getMatching(truckCol,item):
	colCount = truckCol.getColumnCount()
	selCol = "Received"
	if colCount == 2:
		for row in range(truckCol.getRowCount()):
			if item in str(truckCol.getValueAt(row,0)):
				try:
					newValues = [item,truckCol.getValueAt(row,selCol)]
				except:
					newValues = [item,0]
				break
	else:
		newValues = [item,0]
	return newValues

def getTruckData(data):
		#show only unique TruckOrder values
	ds = system.tag.read(SCHEDULE_PATH)
	data = ds.value
	dsTagPath = TRUCK_PATH
	#show only unique TruckOrder values
	nameTruckOrder = "TruckOrder"
	nameSetAuto = "SetAuto"
	headers = ["TruckOrder"]
	headersDS = ["TruckOrder","Received"]
	colTruck = data.getColumnIndex(nameTruckOrder)
	used = set()
	truckCol = []
	currentOrders = set()
	currentTruckVals = system.tag.readBlocking([dsTagPath])
	truckDS = currentTruckVals[0].value
	for row in range(truckDS.getRowCount()):
		valTruck = str(truckDS.getValueAt(row,0))
		truckCol.append(valTruck)
	columnData = []
	for row in range(data.getRowCount()):
		colVal = str(data.getValueAt(row,colTruck))
		if len(colVal)>0:
			columnData.append(colVal)
	unique = list(dict.fromkeys(columnData))
	colData = []
	for x in unique:
		colData.append([x])
	truckData = []
	for y in colData:
		item = y[0]
		if not item in truckCol:
			newValues =[item,0]
			truckData.append(newValues)
		else:
			newValues = getMatching(truckDS,item)
			truckData.append(newValues)
	dataNew = system.dataset.toDataSet(headers,colData)
	truckNewDS = system.dataset.toDataSet(headersDS, truckData)
	system.tag.writeBlocking([dsTagPath],[truckNewDS])
	dataSort = system.dataset.sort(truckNewDS,"TruckOrder",1)
	#dataSort = system.dataset.sort(dataNew,"TruckOrder",1)
	return dataSort

def updateRow(ds, selRow, selCol, newVal):
		if selRow != -1 and selCol != -1:
	   		newData = system.dataset.setValue(ds, selRow, selCol, newVal)
	  		return newData

def updateSetAuto():
	try:
		dsPath = SCHEDULE_PATH
		truckPath = TRUCK_PATH
		truckData = system.tag.readBlocking([truckPath])
		truckDS = truckData[0].value
		readData = system.tag.readBlocking([dsPath])
		excelDS = readData[0].value
		newDS = excelDS
		#excelDS = event.source.excelData
		nameTruckOrder = "TruckOrder"
		selCol = "SetAuto"
		newDS = excelDS
		for row in range(excelDS.getRowCount()):
			strTruckOrder = str(excelDS.getValueAt(row,nameTruckOrder))
			if len(strTruckOrder)>0:
				newValues = getMatching(truckDS,strTruckOrder)
				setAutoVal = newValues[1]
				tempDS = updateRow(newDS,row,selCol,setAutoVal)
				newDS = tempDS
		system.tag.writeBlocking([dsPath],[newDS])
		return True
	except:
		return False
