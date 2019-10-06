from flask import Flask, render_template, request, redirect, url_for, Blueprint
from flask import current_app as app
import csv
import datetime
import glob

from pathlib import Path

bp = Blueprint('backup_operations', __name__)

#import custom csv function - temporary flask hack to use custom module 
from .csv_interface import get_csv, save_csv

@bp.route('/do_bak', methods=['POST'])
def create_backup():
    #get csv
    csv_data = get_csv(app.config['CSV_PATH'],app.config['CSV_DIALECT'])

    #init backup copy of csv file
    backup_dir = Path(app.config['BACKUP_DIR'])
    backup_time = datetime.datetime.today().strftime("%Y%m%d_%H_%M_%S")
    backup_file_name = backup_time + app.config['CSV_NAME'] + ".bak"
    backup_path = backup_dir / backup_file_name
    backup_file = open(backup_path,'x', newline='')
    backup_file.close()

    #save data to backup
    save_csv(csv_data, backup_path,app.config['CSV_DIALECT'])
    
    app.logger.info('Backup created as ' + str(backup_path))

    return redirect("/", code=301)

@bp.route('/list_of_backups')
def list_of_backups():
    #generate list of backup files
    backup_dir = Path(app.config['BACKUP_DIR'])
    backup_list = list(backup_dir.glob("*.bak"))

    #backup list for view
    backups = []
    for path in backup_list:
        backups.append([str(path), path.name])
    backups = sorted(backups, key=lambda tup: tup[1],reverse=True)
    app.logger.info('Backups listed')
    return render_template('backups.html',backups=backups)

@bp.route('/show_backup', methods=['POST'])
def show_backup():
    #get backup csv
    backup_name = request.form.get('backup_name')
    backup_path = app.config['BACKUP_DIR'] / backup_name
    backup_data = get_csv(backup_path,app.config['CSV_DIALECT'])

    app.logger.info('Backup ' + str(backup_path) + ' displayed on screen')

    return render_template('show_backup.html',backup_data=backup_data, backup_path=backup_path)

@bp.route('/return_from_backup', methods=['POST'])
def return_from_backup():
    try:
        #get backup csv path
        backup_path = request.form.get('backup_path') 
    
        #get backup data
        backup_data = get_csv(backup_path,app.config['CSV_DIALECT'])

        #save data
        save_csv(backup_data, app.config['CSV_PATH'],app.config['CSV_DIALECT'])

        app.logger.info('CSV file returned from backup ' + str(backup_path))

        return redirect("/", code=301)
    except PermissionError:
        return 'ERROR! Cannot write to file!'