from flask import Flask, render_template, request, redirect, url_for
import csv
import datetime
import glob

app = Flask(__name__)

#import custom csv function - temporary flask hack to use custom module 
from library.csv_interface import get_csv, save_csv

csv_path = "C:\\Users\\grzes\\Desktop\\python_dev\\pet_projects\\flatfile_ed\\test.csv"

@app.route('/')
@app.route('/index')
def show_csv_data():
    #get csv
    csv_data = get_csv(csv_path)
    return render_template('modifiable_list.html',csv_data=csv_data)

@app.route('/modify_row', methods=['POST'])
def modify_row():
    #get csv
    csv_data = get_csv(csv_path)
    
    #read data of selected row
    print(request.form['row_index'])
    mod_row = csv_data[int(request.form['row_index'])]

    return render_template('forms/mod_row.html', mod_index=request.form['row_index'], mod_row=mod_row)

@app.route('/save_mod', methods=['POST'])
def save_modification():
    #get csv
    csv_data = get_csv(csv_path)
    
    #read data to new row
    if request.form.get('submit') == 'modify':
        csv_row = {k: v for k, v in request.form.items() if k.startswith('col')}
        csv_data[int(request.form['mod_index'])] = csv_row.values()

    elif request.form.get('submit') == 'save_as_new':
        csv_row = {k: v for k, v in request.form.items() if k.startswith('col')}
        csv_data.append(csv_row.values())

    #save data
    save_csv(csv_data, csv_path)

    return redirect("/", code=301)

@app.route('/remove_row', methods=['POST'])
def remove_row():
    #get csv
    csv_data = get_csv(csv_path)

    #read data to new row
    print(request.form)
    csv_data.remove(csv_data[int(request.form['row_index'])])  

    #save data
    save_csv(csv_data, csv_path)
    
    return redirect("/", code=301)

@app.route('/create_new_backup')
def create_backup():
    #open csv file
    csv_dir = "C:\\Users\\grzes\\Desktop\\python_dev\\pet_projects\\flatfile_ed"
    csv_name = "test.csv"
    csv_path = csv_dir + "\\" + csv_name
    csv_file = open(csv_path, 'r', newline='')

    #init backup copy of csv file
    backup_dir = "C:\\Users\\grzes\\Desktop\\python_dev\\pet_projects\\flatfile_ed\\backup"
    backup_time = datetime.datetime.today().strftime("%Y%m%d_%H_%M_%S")
    backup_file_name = backup_time + csv_name + ".bak"
    backup_path = backup_dir + "\\" + backup_file_name
    backup_file = open(backup_path,'x', newline='')

    #save csv_file to backup
    for line in csv_file:
        backup_file.write(line)

    backup_file.close()

    return redirect("/", code=301)

@app.route('/list_of_backups')
def list_of_backups():
    #generate list of backup files
    backup_dir = "C:\\Users\\grzes\\Desktop\\python_dev\\pet_projects\\flatfile_ed\\backup"
    backup_list = glob.glob(backup_dir + "\\*.bak")

    #backup list for view
    backups = []
    for path in backup_list:
        backups.append([path, path.replace(backup_dir + "\\",'')])
    backups = sorted(backups, key=lambda tup: tup[1],reverse=True)

    return render_template('backups.html',backups=backups)

@app.route('/show_backup', methods=['POST'])
def show_backup():
    #get backup csv
    backup_path = request.form.get('backup_path') 
    backup_file = open(backup_path)
    backup_data = csv.reader(backup_file, delimiter=',', doublequote=True)

    return render_template('show_backup.html',backup_data=backup_data, backup_path=backup_path)

@app.route('/return_from_backup', methods=['POST'])
def return_from_backup():
    #get backup csv path
    backup_path = request.form.get('backup_path') 
    
    #get backup data
    backup_data = get_csv(backup_path)

    #save data
    save_csv(backup_data, csv_path)

    return redirect("/", code=301)