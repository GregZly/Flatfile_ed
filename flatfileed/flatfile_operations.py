from flask import Flask, render_template, request, redirect, url_for, Blueprint
from flask import current_app as app
#from flask_assets import Environment
import csv
import datetime
import glob

bp = Blueprint('flatfile_operations', __name__)


#import custom csv function - temporary flask hack to use custom module 
from .csv_interface import get_csv, save_csv

csv_path = "C:\\Users\\grzes\\Desktop\\python_dev\\pet_projects\\flatfile_ed\\test.csv"
csv_name = "test.csv"

@bp.route('/')
@bp.route('/index')
def show_csv_data():
    #get csv
    csv_data = get_csv(app.config['CSV_PATH'])
    return render_template('modifiable_list.html',csv_data=csv_data)


@bp.route('/add_row',methods=['GET','POST'])
def add_row():
    if request.method == 'GET':
        return render_template('forms/append_row.html')
    elif request.method == 'POST':
        #get csv
        csv_data = get_csv(app.config['CSV_PATH'])

        #read data to new row
        csv_row = {k: v for k, v in request.form.items() if k.startswith('col')}
        csv_data.append([csv_row.values()])
        
        #debug
        print(csv_data)

        #sort when check box marked
        if request.form.get('sort') == 'on':
            csv_data.sort()

        #save data
        save_csv(csv_data, app.config['CSV_PATH'])

        return redirect("/", code=301)


@bp.route('/modify_row', methods=['POST'])
def modify_row():
    #get csv
    csv_data = get_csv(app.config['CSV_PATH'])
    
    #read data of selected row
    print(request.form['row_index'])
    mod_row = csv_data[int(request.form['row_index'])]

    return render_template('forms/mod_row.html', mod_index=request.form['row_index'], mod_row=mod_row)

@bp.route('/save_mod', methods=['POST'])
def save_modification():
    #get csv
    csv_data = get_csv(app.config['CSV_PATH'])
    
    #read data to new row
    if request.form.get('submit') == 'modify':
        csv_row = {k: v for k, v in request.form.items() if k.startswith('col')}
        csv_data[int(request.form['mod_index'])] = csv_row.values()

    elif request.form.get('submit') == 'save_as_new':
        csv_row = {k: v for k, v in request.form.items() if k.startswith('col')}
        csv_data.append(csv_row.values())

    #save data
    save_csv(csv_data, app.config['CSV_PATH'])

    return redirect("/", code=301)

@bp.route('/remove_row', methods=['POST'])
def remove_row():
    #get csv
    csv_data = get_csv(app.config['CSV_PATH'])

    #read data to new row
    print(request.form)
    csv_data.remove(csv_data[int(request.form['row_index'])])  

    #save data
    save_csv(csv_data, app.config['CSV_PATH'])
    
    return redirect("/", code=301)

@bp.route('/do_bak', methods=['POST'])
def create_backup():
    #get csv
    csv_data = get_csv(app.config['CSV_PATH'])

    #init backup copy of csv file
    backup_dir = "C:\\Users\\grzes\\Desktop\\python_dev\\pet_projects\\flatfile_ed\\backup"
    backup_time = datetime.datetime.today().strftime("%Y%m%d_%H_%M_%S")
    backup_file_name = backup_time + app.config['CSV_NAME'] + ".bak"
    backup_path = backup_dir + "\\" + backup_file_name
    backup_file = open(backup_path,'x', newline='')
    backup_file.close()

    #save data to backup
    save_csv(csv_data, backup_path)
    
    return redirect("/", code=301)

@bp.route('/list_of_backups')
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

@bp.route('/show_backup', methods=['POST'])
def show_backup():
    #get backup csv
    backup_path = request.form.get('backup_path') 
    backup_data = get_csv(backup_path)

    return render_template('show_backup.html',backup_data=backup_data, backup_path=backup_path)

@bp.route('/return_from_backup', methods=['POST'])
def return_from_backup():
    #get backup csv path
    backup_path = request.form.get('backup_path') 
    
    #get backup data
    backup_data = get_csv(backup_path)

    #save data
    save_csv(backup_data, app.config['CSV_PATH'])

    return redirect("/", code=301)