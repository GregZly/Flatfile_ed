import csv

def main():
    csv_path = "C:\\Users\\grzes\\Desktop\\python_dev\\pet_projects\\flatfile_ed\\test.csv"
    csv_file = open(csv_path)

    csv_reader = csv.reader(csv_file, delimiter=',', doublequote=True)
    #show all data
    for row in csv_reader:
        print(row)
if __name__ == "__main__":
    main()