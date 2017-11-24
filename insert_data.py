# -*- coding: utf-8 -*-
# insert_data.py (custom: inserts csv data directly into sql)

import sqlite3 
from sqlite3 import Error 
import csv 
import sys

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file) # if db_file doesn't exist, this command creates it
        
    except Error as e:
        print(e)
        
    finally:
        conn.close()
    

# step 2  
def update_db(query, db_file):
    try: 
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        
        try: 
            c.execute(query)
            conn.commit()
            
        except Exception as e:
            print (e)
        
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
    
    setup = ["'{}'"]* len(row)
    query_inserts = ', '.join(setup)
    query = """insert into {} values ({})""".format(table_name, query_inserts)
    
    # because this is an ordered dict we can unpack correct order!  
    fields = tuple([row[key] for key in row]) 
    
    # unpacks tuple into format, should work like a dream 
    query = query.format(*fields)
     
    return query

        
def get_data(FILENAME, DB_FILE):      

    # iterate through csv file and read it into sql 
    with open(FILENAME, 'r') as f: 
        r = csv.DictReader(f)
        count = 0
        for row in get_row(r):
            query = construct_insert(row, 'ways')
            update_db(query, DB_FILE)
            

        
def results_query(query, db_file="test.db"):
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