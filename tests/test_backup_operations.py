import os
from flatfileed import flatfile_operations
from flatfileed.csv_interface import get_csv, save_csv
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR
import glob
from pathlib import Path

#Path to folder
local_path = Path.cwd() / "tests"

CSV_NAME = "test_test.csv"
CSV_PATH = local_path / CSV_NAME
BACKUP_DIR = local_path / "backup"
csv_path = CSV_PATH
backup_directory = BACKUP_DIR

def test_create_backup_successful(client):

    #get current state of csv
    csv_data = get_csv(csv_path)

    #do backup
    response = client.post('/do_bak',follow_redirects=True)

    #get list of backups to find path to the latest created backup
    backup_dir = backup_directory
    backup_list = list(backup_dir.glob("*.bak"))
    
    backups = []
    for path in backup_list:
        backups.append([str(path), path.name])
    backups = sorted(backups, key=lambda tup: tup[1],reverse=True)

    bak_path = backups[0][0]

    #check if created backup trully exist
    assert os.path.exists(bak_path)

    #load backup to memory
    backup_data = get_csv(bak_path)

    #compare staged state and last backup to confirm that backup is correct
    assert csv_data == backup_data

    #check if response returned code 200
    assert response.status_code == 200 

def test_list_of_backups(client):
    #get list of .bak files in backup folder
    backup_dir = backup_directory
    backup_list = list(backup_dir.glob("*.bak"))
    
    #show backup list
    response = client.get('/list_of_backups')

    #check if all elements of backup dir are in response data
    for backup_file in backup_list:
        assert backup_file.name.encode() in response.data
    
    #check if response returned code 200
    assert response.status_code == 200 


def test_return_backup_success(client):
    #remove all backups
    backup_dir = backup_directory
    filelist = list(backup_dir.glob("*.bak"))
    if len(filelist) > 0:
        for f in filelist:
            os.remove(f)

    #do backup
    resp1 = client.post('/do_bak',follow_redirects=True)
    assert resp1.status_code == 200 

    #get list of .bak files in backup folder
    backup_list = list(backup_dir.glob("*.bak"))
    backup_path = backup_list[0]

    #data to write
    new_row = ['AAAWrite1','AAAWrite2','AAAkWrite3']

    #apply change to csv file
    resp2 = client.post('/add_row',
                           data=dict(col1=new_row[0],col2=new_row[1],col3=new_row[2],sort='on'),
                           follow_redirects=True)
    assert resp2.status_code == 200 

	#retrun from backup
    resp3 = client.post('/return_from_backup',
                        data=dict(backup_path=backup_path),
                        follow_redirects=True)
    assert resp3.status_code == 200 

    #get data from csv and check if new row exist
    csv_data = get_csv(csv_path)

    assert new_row[0] != csv_data[0][0]
    assert new_row[1] != csv_data[0][1]
    assert new_row[2] != csv_data[0][2]

def test_return_backup_failure(client):
    #remove all backups
    backup_dir = backup_directory
    filelist = list(backup_dir.glob("*.bak"))
    if len(filelist) > 0:
        for f in filelist:
            os.remove(f)
    
    #do backup
    resp1 = client.post('/do_bak',follow_redirects=True)
    assert resp1.status_code == 200 

    #get list of .bak files in backup folder
    backup_list = list(backup_dir.glob("*.bak"))
    
    backup_path = backup_list[0]

    #data to write
    new_row = ['AAAWrite1','AAAWrite2','AAAkWrite3']

    #apply change to csv file
    resp2 = client.post('/add_row',
                           data=dict(col1=new_row[0],col2=new_row[1],col3=new_row[2],sort='on'),
                           follow_redirects=True)
    assert resp2.status_code == 200 

    #block file to prevent write
    os.chmod(csv_path, S_IREAD|S_IRGRP|S_IROTH)

    #retrun from backup
    resp3 = client.post('/return_from_backup',
                        data=dict(backup_path=backup_path),
                        follow_redirects=True)
    assert resp3.status_code == 200 

    #check if error message has appeared
    assert b'ERROR! Cannot write to file!' in resp3.data

    #get data from csv and check if new row exist
    csv_data = get_csv(csv_path)

    assert new_row[0] == csv_data[0][0]
    assert new_row[1] == csv_data[0][1]
    assert new_row[2] == csv_data[0][2]

    #unlock file at the end of test
    os.chmod(csv_path, S_IWUSR|S_IREAD)