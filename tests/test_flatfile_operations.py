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
    #ensure that file is readble
    os.chmod(csv_path, S_IWUSR|S_IREAD)

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

def test_add_row_get(client):
    response = client.get('/add_row')
    assert response.status_code == 200
    assert b'Add new row to csv file' in response.data
    assert b'Column 1' in response.data

def test_add_row_post_not_sort(client):
    #ensure that file is readble
    os.chmod(csv_path, S_IWUSR|S_IREAD)

    #post new row into file
    response = client.post('/add_row',
                           data=dict(col1='TestWrite1',col2='TestWrite2',col3='TestWrite3'),
                           follow_redirects=True)
    
    #check if new row appeared in csv file
    csv_data = get_csv(csv_path)
    assert  any("TestWrite1" in s for s in csv_data)
    
    #check if response returned code 200
    assert response.status_code == 200

def test_add_row_post_sort(client):
    #ensure that file is readble
    os.chmod(csv_path, S_IWUSR|S_IREAD)
    
    #post new row into file
    response = client.post('/add_row',
                           data=dict(col1='AAA_1',col2='TestWrite2',col3='TestWrite3',sort='on'),
                           follow_redirects=True)

    #check if new row appeared in csv file
    csv_data = get_csv(csv_path)
    assert  any("AAA_1" in s for s in csv_data)

    #check if new row is first row in csv file
    assert csv_data[0][0] == "AAA_1"

    #check if response returned code 200
    assert response.status_code == 200

def test_add_row_post_not_sort_failed(client):
    #block file to prevent write
    os.chmod(csv_path, S_IREAD|S_IRGRP|S_IROTH)

    #perform write to capture error
    response = client.post('/add_row',
                           data=dict(col1='ErrorWrite1',col2='ErrorWrite2',col3='ErrorWrite3'),
                           follow_redirects=True)
    
    #check if error message has appeared
    assert b'ERROR! Cannot write to file!' in response.data

    #confirm that entered row does not exist
    csv_data = get_csv(csv_path)
    assert  not(any("ErrorWrite1" in s for s in csv_data))

    #check if response returned code 200
    assert response.status_code == 200

    #unlock file at the end of test
    os.chmod(csv_path, S_IWUSR|S_IREAD)

def test_mod_row(client):
    #get first row from CSV
    csv_data = get_csv(csv_path)
    row_data = csv_data[0]

    response = client.post('/modify_row',
                          data=dict(row_index=0), follow_redirects=True)
    
    #check if modify row form has loaded
    assert b'Modify row of csv file' in response.data
    
    #check if requested value of CSV file has been loaded correctly
    for cell in row_data:
        assert cell.encode() in response.data
    
    #check if response returned code 200
    assert response.status_code == 200

def test_save_as_mod_success(client):
    #Send row to modify
    response = client.post('/save_mod',
                           data=dict(submit='modify',mod_index='0',
                                     col1='ModWrite1',col2='ModWrite2',col3='ModWrite3'), 
                           follow_redirects=True)
    
    #check if modifcation have completed successful
    #get modified CSV row
    csv_data = get_csv(csv_path)
    row_data = csv_data[0]

    assert row_data[0] == 'ModWrite1'
    assert row_data[1] == 'ModWrite2'
    assert row_data[2] == 'ModWrite3'

    #check if response returned code 200
    assert response.status_code == 200

def test_save_as_mod_failure(client):
    #Send row to modify to notexisting index
    response = client.post('/save_mod',
                           data=dict(submit='modify',mod_index='9999',
                                     col1='ModWrite1',col2='ModWrite2',col3='ModWrite3'), 
                           follow_redirects=True)

    assert b'Error! There is no entry with provided index' in response.data

    #check if response returned code 200
    assert response.status_code == 200

def test_as_new_success(client):
    #Send row to modify
    response = client.post('/save_mod',
                           data=dict(submit='save_as_new',
                                     col1='NewWrite1',col2='NewWrite2',col3='NewWrite3'), 
                           follow_redirects=True)
    
    #check if modifcation have completed successful
    #get modified CSV row
    csv_data = get_csv(csv_path)
    row_data = csv_data[-1]

    assert row_data[0] == 'NewWrite1'
    assert row_data[1] == 'NewWrite2'
    assert row_data[2] == 'NewWrite3'

    #check if response returned code 200
    assert response.status_code == 200

def test_as_new_failure(client):
    #block file to prevent write
    os.chmod(csv_path, S_IREAD|S_IRGRP|S_IROTH)

    #Send row to modify
    response = client.post('/save_mod',
                           data=dict(submit='save_as_new',
                                     col1='ErrorWrite1',col2='ErrorWrite2',col3='ErrorWrite3'), 
                           follow_redirects=True)

    #check if error message has appeared
    assert b'ERROR! Cannot write to file!' in response.data

    #confirm that entered row does not exist
    csv_data = get_csv(csv_path)
    assert  not(any("ErrorWrite1" in s for s in csv_data))

    #check if response returned code 200
    assert response.status_code == 200

    #unlock file at the end of test
    os.chmod(csv_path, S_IWUSR|S_IREAD)
    
def test_remove_row_success(client):
    #get data of row to remove
    csv_data = get_csv(csv_path)
    row_data = csv_data[0]

    #invoke removation of row
    response = client.post('/remove_row',
                            data=dict(row_index='0'),
                            follow_redirects=True)
    
    #confirm that removed row doesnt exist
    csv_data_after_remove  = get_csv(csv_path)
    assert row_data[0] != csv_data_after_remove[0][0]
    assert row_data[1] != csv_data_after_remove[0][1]
    assert row_data[2] != csv_data_after_remove[0][2]      

    #check if response returned code 200
    assert response.status_code == 200

def test_remove_row_failure(client):
    #get data of row to remove
    csv_data = get_csv(csv_path)
    row_data = csv_data[0]

    #block file to prevent write
    os.chmod(csv_path, S_IREAD|S_IRGRP|S_IROTH)

    #invoke removation of row
    response = client.post('/remove_row',
                            data=dict(row_index='0'),
                            follow_redirects=True)
    
    #check if error message has appeared
    assert b'ERROR! Cannot write to file!' in response.data

    #confirm that row to remove still exist
    csv_data_after_remove = get_csv(csv_path)
    
    assert row_data[0] == csv_data_after_remove[0][0]
    assert row_data[1] == csv_data_after_remove[0][1]
    assert row_data[2] == csv_data_after_remove[0][2] 

    #check if response returned code 200
    assert response.status_code == 200  