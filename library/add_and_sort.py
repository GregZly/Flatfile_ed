from flask import Flask, render_template, request
import csv

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def add_row():
    if request.method == 'GET':
        return render_template('forms/append_row.html')
    elif request.method == 'POST':
        csv.register_dialect('mydia', delimiter=',', quoting=csv.QUOTE_ALL, doublequote=True)    
        csv_path = "C:\\Users\\grzes\\Desktop\\python_dev\\pet_projects\\flatfile_ed\\test.csv"
        csv_file = open(csv_path, 'r', newline='')
        csv_reader = csv.reader(csv_file, delimiter=',', doublequote=True)
        csv_data = []
        for row in csv_reader:
            csv_data.append(row)

        csv_file.close()

        #read data to new row
        new_row =[request.form['col1'],request.form['col2'],request.form['col3']]
        csv_data.append(new_row)
        
        #sort when check box marked
        if request.form.get('sort') == 'on':
            csv_data.sort()

        csv_file = open(csv_path, 'w', newline='')
        csv_writer = csv.writer(csv_file, 'mydia')
        csv_writer.writerows(csv_data)
        csv_file.close()
        
        return render_template('forms/append_row.html')