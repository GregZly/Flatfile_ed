from flask import Flask, render_template, request
import csv

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def add_row():
    if request.method == 'GET':
        return render_template('forms/append_row.html')
    elif request.method == 'POST':
        #Add custom dialect to read and write CSV file correct
        csv.register_dialect('mydia', delimiter=',', quoting=csv.QUOTE_ALL, doublequote=True)    
        csv_path = "C:\\Users\\grzes\\Desktop\\python_dev\\pet_projects\\flatfile_ed\\test.csv"
        csv_file = open(csv_path, 'a', newline='')

        #read data to new row
        new_row = [request.form['col1'],request.form['col2'],request.form['col3']]
        csv_writer = csv.writer(csv_file, 'mydia')
        csv_writer.writerow(new_row)
        
        #close file at the end
        csv_file.close()
        return render_template('forms/append_row.html')