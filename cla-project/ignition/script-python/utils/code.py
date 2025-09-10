def printDataset(dataset):
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
        
def minutesformat(minutes):
	"""Convert minutes to time format HH:mm:ss.

	Args:
		minutes (int or float): Time in minutes.

	Returns:
		str: Time formatted as 'HH:mm:ss'.
	"""
	total_seconds = int(minutes * 60)
	hours, remainder = divmod(total_seconds, 3600)
	mins, secs = divmod(remainder, 60)
	return "{hours:02}h {mins:02}m".format(hours=hours, mins=mins)