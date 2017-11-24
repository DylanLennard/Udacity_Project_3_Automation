# -*- coding: utf-8 -*-

import os 
from pprint import pprint

import request_data
import sample
import mapparser
import tags
import users
import audit
import data
import check_files 
import insert_data 


URL = "http://overpass-api.de/api/map?bbox=-87.5322,36.4246,-87.19,36.64"
FILENAME = "./OSM_files/Clarksville.OSM" 
SAMPLE_NAME = "./OSM_files/Clarksville_Sample.OSM"
DB_FILE = "./DB/Clarksville.DB"
SQL_FILE = "./SQL_files/populate_db.sql"
CSV_PATH = "./CSV_files/"

CREATE_QUERY = """
CREATE TABLE nodes (
    id INTEGER PRIMARY KEY NOT NULL,
    lat REAL,
    lon REAL,
    user TEXT,
    uid INTEGER,
    version INTEGER,
    changeset INTEGER,
    timestamp TEXT
);

CREATE TABLE nodes_tags (
    id INTEGER,
    key TEXT,
    value TEXT,
    type TEXT,
    FOREIGN KEY (id) REFERENCES nodes(id)
);

CREATE TABLE ways (
    id INTEGER PRIMARY KEY NOT NULL,
    user TEXT,
    uid INTEGER,
    version TEXT,
    changeset INTEGER,
    timestamp TEXT
);

CREATE TABLE ways_tags (
    id INTEGER NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    type TEXT,
    FOREIGN KEY (id) REFERENCES ways(id)
);

CREATE TABLE ways_nodes (
    id INTEGER NOT NULL,
    node_id INTEGER NOT NULL,
    position INTEGER NOT NULL,
    FOREIGN KEY (id) REFERENCES ways(id),
    FOREIGN KEY (node_id) REFERENCES nodes(id)
);

"""

DROP_QUERY = """
DROP TABLE IF EXISTS WAYS;
DROP TABLE IF EXISTS WAYS_NODES;
DROP TABLE IF EXISTS WAYS_TAGS;
DROP TABLE IF EXISTS NODES;
DROP TABLE IF EXISTS NODES_TAGS; 
"""



if __name__ == "__main__":

    # get the data (optional)
    request_data.get_XML_data(URL, FILENAME)
    
    # get a sample of the data first (this is optional once we're done) 
    sample.sample_data(FILENAME, SAMPLE_NAME, k=10)
    
    # count how many tags we have 
    pprint(mapparser.count_tags(FILENAME))
    
    # get idea of what kind of fixes we should make  
    pprint(tags.process_map(FILENAME))
    
    # get idea of unique users in dataset 
    # possibly use this to make another table called users. we'll see 
    print(users.process_map(FILENAME)) 
    
    # audit the data to see lastly what changes need be made
    pprint(audit.audit(FILENAME))
    
    # lastly, after examining the data, call data.py. 
    # one change ou need to make: include audit in data.py somehow 
    data.process_map(FILENAME, validate=False)
    
    
    # from here, put everything into your sqlite3 database  
    # or....try to load everything through python  




'''   
sql.create_connection(DB_FILE)
sql.get_data(CSV_PATH, SQL_FILE, create=CREATE_QUERY, drop=DROP_QUERY)'''