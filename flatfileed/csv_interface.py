import csv

def validate_csv(csv_data,dialect):
    """
    Validates csv_data against declared configuration in dialect
    """
    #check number of columns
    if len(csv_data[1]) == dialect['CSV_COLUMNS']:
        return True
    else:
        return False


def get_csv(csv_path,dialect):
    """
    Returns csv_data array for provided csv_path 
    """
    try:
        #register dialect provided as parameter
        csv.register_dialect('flatfileed', delimiter=dialect['CSV_DELIMITER'],
                             quoting=dialect['CSV_QUOTING'], doublequote=dialect['CSV_DOUBLEQUOTE'],
                             strict=True)

        csv_file = open(csv_path)
        #csv_reader = csv.reader(csv_file, delimiter=',', doublequote=True)
        csv_reader = csv.reader(csv_file, 'flatfileed')
        csv_data = []
        for row in csv_reader:
            csv_data.append(row)
        csv_file.close()

        if validate_csv(csv_data,dialect) == True:
            return csv_data
        else:
            raise csv.Error
    except FileNotFoundError:
        raise FileNotFoundError('CSV File not provided!')
    except csv.Error:
        raise csv.Error('Wrong format of provied CSV! Check file or review configuration')

    
def save_csv(csv_data, csv_path, dialect):
    """
    Saves csv_data array into provided csv_path
    """
    try:    
        #csv.register_dialect('mydia', delimiter=',', quoting=csv.QUOTE_ALL, doublequote=True) 
        #register dialect provided as parameter
        csv.register_dialect('flatfileed', delimiter=dialect['CSV_DELIMITER'],
                             quoting=dialect['CSV_QUOTING'], doublequote=dialect['CSV_DOUBLEQUOTE'],
                             strict=True)
        csv_file = open(csv_path, 'w', newline='')
        #csv_writer = csv.writer(csv_file, 'mydia')
        csv_writer = csv.writer(csv_file, 'flatfileed')
        csv_writer.writerows(csv_data)
        csv_file.close()
        return 'CSV Saved successful'
    except PermissionError:
        raise PermissionError('No permission to file or directory')