import csv

def get_csv(csv_path):
    """
    Returns csv_data array for provided csv_path 
    """
    csv_file = open(csv_path)
    csv_reader = csv.reader(csv_file, delimiter=',', doublequote=True)
    
    csv_data = []
    for row in csv_reader:
        csv_data.append(row)
    csv_file.close()

    return csv_data

def save_csv(csv_data, csv_path):
    """
    Saves csv_data array into provided csv_path
    """
    csv.register_dialect('mydia', delimiter=',', quoting=csv.QUOTE_ALL, doublequote=True) 
    csv_file = open(csv_path, 'w', newline='')
    csv_writer = csv.writer(csv_file, 'mydia')
    csv_writer.writerows(csv_data)
    csv_file.close()