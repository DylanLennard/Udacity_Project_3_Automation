# -*- coding: utf-8 -*-

import pandas as pd
import csv


# this is how I'd do it with csv
def check_file_w_csv(file, fields):
    with open(file) as f: 
        r = csv.DictReader(f)
        
        # if data is large, should create generator to iterate through  
        r = list(r)
        
        # add some checks here. 
        print("Filename:", NODES_PATH)
        print("Number of Rows:", len(r))
        print("Column Names:", r[0].keys()) # create check agains our fields list 
        print("First Rows: ", r[0:4])
        print("\n")

# However the output from here is a little cleaner and easier to understand since we know pandas already
def check_file(file, fields):
    
    """
    Runs a quick check on a given output file to make sure the file is formatted properly
    Reports shape of file, column names, missing columns, extra columns,
    and shows the head of the DF. 
    
    NOTE: Should only use this if your data size is small enough to read into memory effectively  
    
    Args: 
        file: filename to read in and check for  
        field: corresponding field which was defined in our above program. 
                - This is used to check our column names with 
                - If used separately, make sure you redefine those fields from our above cell
    """
    DF = pd.read_csv(file)
    columns = DF.columns.values.tolist() 
    missing_cols = list(set(fields) - set(columns)) 
    extra_cols = list(list(set(columns) - set(fields))) 
    
    print("Filename:", file)
    print("Shape: ", DF.shape)
    print("Column Names:", columns)
    
    # the following two checks should simply report empty lists
    # if they don't, go figure out what missing or extra columns you have!  
    print("Column Names Missing From DF:", missing_cols) 
    print("Extra Columns in DF:", extra_cols) 
    
    
    print("Head:\n", DF.head(n=3))
    print("\n\n")
