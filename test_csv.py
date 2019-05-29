import csv

def main():
    #Add custom dialect to read and write CSV file correct
    csv.register_dialect('mydia', delimiter=',', quoting=csv.QUOTE_ALL, doublequote=True)    
    csv_path = "C:\\Users\\grzes\\Desktop\\python_dev\\pet_projects\\flatfile_ed\\test.csv"
    csv_file = open(csv_path, 'r')

    csv_reader = csv.reader(csv_file, 'mydia')
    
    #copy all data to collection
    csv_data = []
    for row in csv_reader:
        csv_data.append(row)
    #close file to read
    print(csv_data)
    csv_file.close()

    #add new row and write file
    row = ['Sample6','44.22','Y']
    csv_data.append(row)

    #change current row to other
    csv_data[2] = ['Change Sample2','20.00','NN']

    csv_file = open(csv_path, 'w', newline='')
    csv_writer = csv.writer(csv_file, 'mydia')
    csv_writer.writerows(csv_data)

    #close file at the end
    csv_file.close()


if __name__ == "__main__":
    main()