from flask import Flask, render_template, request, redirect
import csv


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
    csv_data[int(request.form['mod_index'])] =[request.form['col1'],request.form['col2'],request.form['col3']]
    
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

