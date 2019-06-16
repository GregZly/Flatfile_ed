import pytest
import os
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR

from flatfileed.csv_interface import get_csv
from flatfileed.csv_interface import save_csv

test_path_correct = "C:\\Users\\grzes\\Desktop\\python_dev\\pet_projects\\flatfile_ed\\test.csv"
#test_path_correct = "save_test.csv"
test_path_wrong = "unk.csv"

def test_get_csv():
    assert get_csv(test_path_correct) is not None 

def test_get_csv_exception():
    with pytest.raises(FileNotFoundError) as err_info:
        get_csv(test_path_wrong)
    
    assert 'CSV File not provided!' in str(err_info.value)

def test_save_csv_correct():
    save_path_correct = "C:\\Users\\grzes\\Desktop\\python_dev\\pet_projects\\flatfile_ed\\tests\\save_test.csv"
    save_data_set =["Column1","Column2","Column3"]
    
    assert save_csv(save_data_set,save_path_correct) == 'CSV Saved successful'

def test_save_csv_no_privileges():
    save_path = "C:\\Users\\grzes\\Desktop\\python_dev\\pet_projects\\flatfile_ed\\tests\\save_test.csv"
    save_data_set =["Column1","Column2","Column3"]
    
    #change target file to read-only 
    os.chmod(save_path, S_IREAD|S_IRGRP|S_IROTH)

    with pytest.raises(PermissionError) as err_info:
        save_csv(save_data_set,save_path)
    assert 'No permission to file or directory' in str(err_info.value)

    #when test completed make file writable again
    os.chmod(save_path, S_IWUSR|S_IREAD)