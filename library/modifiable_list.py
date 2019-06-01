from flask import Flask, render_template, request, redirect
import csv
import datetime


app = Flask(__name__)

@app.route('/')
def show_csv_data():
    #get csv
    csv_path = "C:\\Users\\grzes\\Desktop\\python_dev\\pet_projects\\flatfile_ed\\test.csv"
    csv_file = open(csv_path)
    csv_data = csv.reader(csv_file, delimiter=',', doublequote=True)

    return render_template('modifiable_list.html',csv_data=csv_data)

@app.route('/modify_row', methods=['POST'])
def modify_row():
    #get csv
    csv_path = "C:\\Users\\grzes\\Desktop\\python_dev\\pet_projects\\flatfile_ed\\test.csv"
    csv_file = open(csv_path, 'r')
    csv_reader = csv.reader(csv_file, delimiter=',', doublequote=True)
    csv_data = []
    for row in csv_reader:
        csv_data.append(row)

    #read data of selected row
    print(request.form['row_index'])
    mod_row = csv_data[int(request.form['row_index'])]

    #close file at the end
    csv_file.close()
    return render_template('forms/mod_row.html', mod_index=request.form['row_index'], mod_row=mod_row)

@app.route('/save_mod', methods=['POST'])
def save_modification():
    #Add custom dialect to read and write CSV file correct
    csv.register_dialect('mydia', delimiter=',', quoting=csv.QUOTE_ALL, doublequote=True)    
    csv_path = "C:\\Users\\grzes\\Desktop\\python_dev\\pet_projects\\flatfile_ed\\test.csv"
    csv_file = open(csv_path, 'r', newline='')
    csv_reader = csv.reader(csv_file, delimiter=',', doublequote=True)
    csv_data = []
    for row in csv_reader:
        csv_data.append(row)

    csv_file.close()

    #read data to new row
    print(request.form)
    if request.form.get('submit') == 'modify':
        csv_row = {k: v for k, v in request.form.items() if k.startswith('col')}
        csv_data[int(request.form['mod_index'])] = csv_row.values()

    elif request.form.get('submit') == 'save_as_new':
        csv_row = {k: v for k, v in request.form.items() if k.startswith('col')}
        #csv_data.append([request.form['col1'],request.form['col2'],request.form['col3']])
        csv_data.append(csv_row.values())
    csv_file = open(csv_path, 'w', newline='')
    csv_writer = csv.writer(csv_file, 'mydia')
    csv_writer.writerows(csv_data)
    csv_file.close()
    
    return show_csv_data()

@app.route('/remove_row', methods=['POST'])
def remove_row():
    #Add custom dialect to read and write CSV file correct
    csv.register_dialect('mydia', delimiter=',', quoting=csv.QUOTE_ALL, doublequote=True)    
    csv_path = "C:\\Users\\grzes\\Desktop\\python_dev\\pet_projects\\flatfile_ed\\test.csv"
    csv_file = open(csv_path, 'r', newline='')
    csv_reader = csv.reader(csv_file, delimiter=',', doublequote=True)
    csv_data = []
    for row in csv_reader:
        csv_data.append(row)

    csv_file.close()

    #read data to new row
    print(request.form)
    csv_data.remove(csv_data[int(request.form['row_index'])])   
    
    csv_file = open(csv_path, 'w', newline='')
    csv_writer = csv.writer(csv_file, 'mydia')
    csv_writer.writerows(csv_data)
    csv_file.close()
    
    return show_csv_data()

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

    return show_csv_data()


    