from custom_sql import CustomSQL
import os
import csv

"""
    take a csv file +
    file exists check +
    and check it is csv + 

    connect to the db
    override the entire table 
    and insert into the cleared table with queries built out of csv
    build a procedure i.e. dot sql file to help with debugging
    figure out how to run it 
    build as transaction with rollback functionality 
"""

def cvs_reader(filename):
    """ Function to read contents of menu csv file"""
    try:
        with open(filename, 'r') as csvfile:
            _arr = []
            _spamreader = csv.reader(csvfile, delimiter=',')
            for row in _spamreader:
                _arr.append(row[0])
            del(_arr[0])
            return _arr
    except:
        print("File does not exist")

def main():
    # connection to database
    db = CustomSQL()
    pathname = os.path.join("scripts", "menu.csv")
    
    if pathname.endswith('.csv'):
        cvs_reader(pathname)
    else:
        print("This is not a csv file")

if __name__ == "__main__":
    main()
