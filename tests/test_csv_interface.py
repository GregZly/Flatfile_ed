import pytest
import os
import csv
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR

from flatfileed.csv_interface import get_csv
from flatfileed.csv_interface import save_csv

test_path_correct = "C:\\Users\\grzes\\Desktop\\python_dev\\pet_projects\\flatfile_ed\\test.csv"
#test_path_correct = "save_test.csv"
test_path_wrong = "unk.csv"
test_dialect = {'CSV_DELIMITER' : ',',
               'CSV_QUOTING' : csv.QUOTE_ALL,
               'CSV_DOUBLEQUOTE' : True,
               'CSV_COLUMNS' : 3}

#def get_columns_number(csv_path, csv_dialect):
#    csv.register_dialect('getcols', delimiter=csv_dialect['CSV_DELIMITER'],
#                             quoting=csv_dialect['CSV_QUOTING'], doublequote=csv_dialect['CSV_DOUBLEQUOTE'],
#                             strict=True)
#    csv_file = open(csv_path, 'r')
#    csv_reader = csv.reader(csv_file, 'getcols')
#    csv_data = []
#    for row in csv_reader:
#            csv_data.append(row)
#    csv_file.close()
#    return(len(csv_data[1]))


def test_get_csv():
    assert get_csv(test_path_correct, test_dialect) is not None 

def test_get_csv_exception():
    with pytest.raises(FileNotFoundError) as err_info:
        get_csv(test_path_wrong,test_dialect)
    
    assert 'CSV File not provided!' in str(err_info.value)

def test_save_csv_correct():
    save_path_correct = "C:\\Users\\grzes\\Desktop\\python_dev\\pet_projects\\flatfile_ed\\tests\\save_test.csv"
    save_data_set =["Column1","Column2","Column3"]
    
    assert save_csv(save_data_set,save_path_correct,test_dialect) == 'CSV Saved successful'

def test_save_csv_no_privileges():
    save_path = "C:\\Users\\grzes\\Desktop\\python_dev\\pet_projects\\flatfile_ed\\tests\\save_test.csv"
    save_data_set =["Column1","Column2","Column3"]
    
    #change target file to read-only 
    os.chmod(save_path, S_IREAD|S_IRGRP|S_IROTH)

    with pytest.raises(PermissionError) as err_info:
        save_csv(save_data_set,save_path,test_dialect)
    assert 'No permission to file or directory' in str(err_info.value)

    #when test completed make file writable again
    os.chmod(save_path, S_IWUSR|S_IREAD)


def test_columns_mismatch():
    #prepare other dialect and file
    other_dialect = {'CSV_DELIMITER' : '\t',
                     'CSV_QUOTING' : csv.QUOTE_NONE,
                     'CSV_DOUBLEQUOTE' : False }
    other_file_path = "C:\\Users\\grzes\\Desktop\\python_dev\\pet_projects\\flatfile_ed\\tests\\other_format.csv"
    save_data_set =[["Row1Column1","Row1Column2","Row1Column3"],
                    ["Row2Column1","Row2Column2","Row2Column3"]]

    save_csv(save_data_set,other_file_path,other_dialect)
    #assert get_columns_number(other_file_path,test_dialect) != 3       
    with pytest.raises(csv.Error) as err_info:
        get_csv(other_file_path,test_dialect)
    assert 'Wrong format of provied CSV! Check file or review configuration' in str(err_info.value)  