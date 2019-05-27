import csv

def main():
    #Add custom dialect to read and write CSV file correct
    csv.register_dialect('mydia', delimiter=',', quoting=csv.QUOTE_ALL, doublequote=True)    
    csv_path = "C:\\Users\\grzes\\Desktop\\python_dev\\pet_projects\\flatfile_ed\\test.csv"
    csv_file = open(csv_path, 'r')

    csv_reader = csv.reader(csv_file, 'mydia')
    
    #show all data
    for row in csv_reader:
        print(row)
    #close file to read
    csv_file.close()

    #add new row and write file
    csv_file = open(csv_path, 'a')
    row = ['Sample4','40.20','N']
    csv_writer = csv.writer(csv_file, 'mydia')
    csv_writer.writerow(row)

    #close file at the end
    csv_file.close()


if __name__ == "__main__":
    main()