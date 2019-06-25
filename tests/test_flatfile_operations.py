import os
from flatfileed import flatfile_operations
from flatfileed.csv_interface import get_csv, save_csv
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR

csv_path = "C:\\Users\\grzes\\Desktop\\python_dev\\pet_projects\\flatfile_ed\\tests\\test_test.csv"

def test_index(client):
    response = client.get('/index')
    assert response.status_code == 200
    assert b'Modifiable CSV' in response.data

def test_read_csv_successful(client):
    #prepare test csv_data
    csv_data = [['Row1Col1','Row1Col2','Row1Col3'],
                ['Row2Col1','Row2Col2','Row2Col3']]
    #save data into test csv file
    save_csv(csv_data,csv_path)

    #check if file has been read succssefully
    response = client.get('/index')
    for row in csv_data:
        for cell in row:
            assert cell.encode() in response.data
    