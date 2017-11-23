# -*- coding: utf-8 -*-

# sql.py 
# (this is one you'll make to create the sql statements needed)
# -*- coding: utf-8 -*-
# insert_data.py (custom: inserts csv data directly into sql)

import sqlite3 
from sqlite3 import Error 
import csv
import os

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        # if db_file doesn't exist, this command creates it
        conn = sqlite3.connect(db_file) 
        
    except Error as e:
        print(e)
        
    finally:
        conn.close()
    

# step 3
def get_row(dictReader):
    for row in dictReader: 
        yield row
        
# step 4
def construct_insert(row, table_name):
    colnames = []
    values = []
    for key in row:
        colnames.append(key)
        values.append(row[key])
        
    insert_cols = ", ".join(colnames)
    insert_vals = "'"+ "', '".join(values) + "'"
    query = "insert into {} ({}) values ({});\n".\
                                  format(table_name ,insert_cols, insert_vals)

    return query  

def file_read(file, wf):
    '''Iterates through file using generator, writes each row to file'''
    with open(file, 'r') as rf:
        r = csv.DictReader(rf)
        
        # construct table_name from file
        table_name = file.replace("./CSV_files/","").\
                                 replace(".csv","").upper()
                                 
                                 
        for row in get_row(r):
            query = construct_insert(row, table_name)
            wf.write(query)
        # add newline just for some space in the sql files
        wf.write("\n")

        
def get_data(file_path, sql_file, create=None, drop=None):  
    
    # open write file  
    with open(sql_file, 'w') as wf:
        
        # check if drop or create queries passed, execute if so 
        if drop:
            wf.write(drop)
        if create: 
            wf.write(create)
            
        # open read files and call file_read
        for file in os.listdir(file_path):
            path = file_path+file
            print("Looking at", path)
            file_read(path, wf)
        
        
def results_query(query, db_file):
    try: 
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        results = None
        try: 
            c.execute(query)
            results = c.fetchall()
            
        except Exception as e:
            print (e)
        
    except Error as e:
        print(e)
        
    finally:
        conn.close()
    
    if results:
        return results