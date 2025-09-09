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