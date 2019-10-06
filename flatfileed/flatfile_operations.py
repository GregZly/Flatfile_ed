from flask import Flask, render_template, request, redirect, url_for, Blueprint
from flask import current_app as app
import csv
import datetime
import glob

from pathlib import Path

bp = Blueprint('flatfile_operations', __name__)

#import custom csv function - temporary flask hack to use custom module 
from .csv_interface import get_csv, save_csv


@bp.route('/')
@bp.route('/index')
def show_csv_data():
    try:
        #get csv
        csv_data = get_csv(app.config['CSV_PATH'],app.config['CSV_DIALECT'])
        return render_template('modifiable_list.html',csv_data=csv_data)
    except PermissionError:
        return "ERROR! Configured file unreadable!"
    except csv.Error:
        return 'Internal structure of CSV different than configured! Check Config!'

@bp.route('/add_row',methods=['GET','POST'])
def add_row():
    if request.method == 'GET':
        return render_template('forms/append_row.html',config=app.config['CSV_DIALECT'])
    elif request.method == 'POST':
        #get csv
        csv_data = get_csv(app.config['CSV_PATH'],app.config['CSV_DIALECT'])
        try:
            #read data to new row
            csv_row = {k: v for k, v in request.form.items() if k.startswith('col')} 
            csv_data.append(list(csv_row.values()))

            #sort when check box marked
            if request.form.get('sort') == 'on':
                csv_data.sort()

            #save data
            save_csv(csv_data, app.config['CSV_PATH'],app.config['CSV_DIALECT'])

            return redirect("/", code=301)
        except PermissionError:
            return "ERROR! Cannot write to file!"


@bp.route('/modify_row', methods=['POST'])
def modify_row():
    #get csv
    csv_data = get_csv(app.config['CSV_PATH'],app.config['CSV_DIALECT'])
    
    #read data of selected row
    print(request.form['row_index'])
    mod_row = csv_data[int(request.form['row_index'])]

    return render_template('forms/mod_row.html', mod_index=request.form['row_index'], mod_row=mod_row)

@bp.route('/save_mod', methods=['POST'])
def save_modification():
    #get csv
    csv_data = get_csv(app.config['CSV_PATH'],app.config['CSV_DIALECT'])
    
    try:
        #read data to new row
        if request.form.get('submit') == 'modify':
            csv_row = {k: v for k, v in request.form.items() if k.startswith('col')}
            csv_data[int(request.form['mod_index'])] = csv_row.values()

        elif request.form.get('submit') == 'save_as_new':
            csv_row = {k: v for k, v in request.form.items() if k.startswith('col')}
            csv_data.append(csv_row.values())

        #save data
        save_csv(csv_data, app.config['CSV_PATH'],app.config['CSV_DIALECT'])

        return redirect("/", code=301)
    except IndexError:
        return 'Error! There is no entry with provided index'
    except PermissionError:
        return 'ERROR! Cannot write to file!'

@bp.route('/remove_row', methods=['POST'])
def remove_row():
    #get csv
    csv_data = get_csv(app.config['CSV_PATH'],app.config['CSV_DIALECT'])

    try:
        #read data to new row
        csv_data.remove(csv_data[int(request.form['row_index'])])  

        #save data
        save_csv(csv_data, app.config['CSV_PATH'],app.config['CSV_DIALECT'])
    
        return redirect("/", code=301)
    except PermissionError:
        return 'ERROR! Cannot write to file!'