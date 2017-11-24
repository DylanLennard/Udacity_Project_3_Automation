# -*- coding: utf-8 -*-
# insert_data.py (custom: inserts csv data directly into sql)

import sqlite3 
from sqlite3 import Error 
import csv 
import sys

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        # if db_file doesn't exist, this command creates it
        conn = sqlite3.connect(db_file) 
        
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
    fields = tuple([row[key].replace("'", "''") for key in row]) 
    
    # unpacks tuple into format, should work like a dream 
    query = query.format(*fields)
     
    return query

        
def get_data(FILENAME, DB_FILE):      
    
    # TODO: enter connection in here and then set up try/except blocks
    # this will cut down on connection time  
    
    # iterate through csv file and read it into sql 
    with open(FILENAME, 'r') as f: 
        r = csv.DictReader(f)
        
        try: 
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            for row in get_row(r):
                
                # TODO: get table name read in from filename  
                query = construct_insert(row, 'nodes_tags')
                # update_db(query, DB_FILE)
                
                try: 
                    c.execute(query)
                    conn.commit() 
            
                except Exception as e:
                    print (e, query)
                
        except Error as e:
            print(e)
        
        finally:
            conn.close()
            print("connection closed")
            

        
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