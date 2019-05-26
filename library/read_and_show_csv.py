from flask import Flask, render_template
import csv

app = Flask(__name__)

@app.route('/')
def get_and_show_csv():
    #get csv
    csv_path = "C:\\Users\\grzes\\Desktop\\python_dev\\pet_projects\\flatfile_ed\\test.csv"
    csv_file = open(csv_path)
    csv_data = csv.reader(csv_file, delimiter=',', doublequote=True)

    return render_template('sample_csv.html',csv_data=csv_data)