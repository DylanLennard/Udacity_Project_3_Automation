# -*- coding: utf-8 -*-
# insert_data.py (custom: inserts csv data directly into sql)

import sqlite3 
from sqlite3 import Error 
import csv 
import sys
import re 

def create_connection(db_file):
    """ 
    create a database connection to a SQLite database 
    """
    
    try:
        # if db_file doesn't exist, this command creates it
        conn = sqlite3.connect(db_file) 
        
    except Error as e:
        print(e)
        
    finally:
        conn.close()
    

# step 2  
def update_db(query, db_file):
    
    """
    Updates the DB query with insert/create statements
    """
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
    """
    Dynamically creates the insert statement needed to insert the data from 
    the CSV file. This query will accomodate all tables.
    """
    
    setup = ["'{}'"] * len(row)
    query_inserts = ', '.join(setup)
    query = """insert into {} values ({})""".format(table_name, query_inserts)
    
    # because this is an ordered dict we can unpack correct order!  
    fields = tuple([row[key].replace("'", "''") if isinstance(row[key], str) \
                        else row[key] for key in row]) 
    
    # unpacks tuple into format, should work like a dream 
    query = query.format(*fields)
     
    return query

        
def get_data(FILENAME, DB_FILE):      
    
    '''
    Opens file, connects to DB, iterates through file, updates data in DB
    '''
    
    # iterate through csv file and read it into sql 
    with open(FILENAME, 'r') as f: 
        r = csv.DictReader(f)
        
        try: 
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            for row in get_row(r):
                
                # get tablename from the filename then construct query 
                table_name = re.sub("./CSV_files/|.csv", "", FILENAME)
                query = construct_insert(row, table_name)
                
                try: 
                    c.execute(query)
            
                except Exception as e:
                    print (e, query)
        
            # once all statements completed, commit changes
            conn.commit()
                
        except Error as e:
            print(e)
        
        finally:
            conn.close()
            print("connection closed")
            

        
def results_query(query, db_file):
    """
    Used for querying the DB to check that changes happened
    """
    
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
