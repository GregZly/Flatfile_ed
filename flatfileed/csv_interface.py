import csv

def get_csv(csv_path):
    """
    Returns csv_data array for provided csv_path 
    """
    try:

        csv_file = open(csv_path)
        csv_reader = csv.reader(csv_file, delimiter=',', doublequote=True)
        
        csv_data = []
        for row in csv_reader:
            csv_data.append(row)
        csv_file.close()

        return csv_data
    except FileNotFoundError:
        raise FileNotFoundError('CSV File not provided!')

    
def save_csv(csv_data, csv_path):
    """
    Saves csv_data array into provided csv_path
    """
    try:    
        csv.register_dialect('mydia', delimiter=',', quoting=csv.QUOTE_ALL, doublequote=True) 
        csv_file = open(csv_path, 'w', newline='')
        csv_writer = csv.writer(csv_file, 'mydia')
        csv_writer.writerows(csv_data)
        csv_file.close()
        return 'CSV Saved successful'
    except PermissionError:
        raise PermissionError('No permission to file or directory')