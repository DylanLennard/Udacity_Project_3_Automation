# DAND Project 3 Automation 
## Purpose  
The purpose of this project was to attempt to automate the process of auditing, cleaning, and loading data from the web as XML, to CSV, and then to a relational DB for the Data Wrangling Project of the Data Analyst Nanodegree.  

## Background  
The project involves auditing OSM data from a given location of choice and loading it into a DB. The point of the project is to practice auditing data in a complex data format (XML), making the changes in python, formatting the data into an object that can be stored in SQL, and then uploading that data into SQL. While students are expected to focus highly on the auditing portion, I wanted to take the time to practice automating the process from end to end to set up a sort of automated ETL process using solely python.  

## Steps Taken  
1) Read in data of concern from http request  
2) Read this data onto local machine  
3) Run auditing functions to get high level information on file  
4) Simultaneously clean and export the data into a csv format  
5) Use DB-API and pre-defined schema to upload the data into SQL db   

## Potential Future Improvements  
A major improvement to the project in terms of automating this process would be unit tests to ensure the integrity of the functions themselves. These would also be good for future edge case testing.  


## Files   
Some files were setup by Udacity and then further modified/completed by myself, others were made by me for the purpose of completing the automation process.  

* request_data.py (custom): get's data from http request  
* mapparser.py: gets a count of each tag type in OSM file     
* tags.py: investigates the k attributes of each tag to look into addresses   
* users.py: gets count of unique users that contributed to data   
* audit.py: cleans up the street names and looks for more names to fix  
* data.py: takes final cleaned up data and reads it into csv files for import  
* schema.py: used for validation purposes   

* main.py(custom): will be the place we call all functions to run simultaneously
* insert_data.py (custom): inserts csv data directly into db via sqlite3
* check_files.py (custom): makes sure csv data comes out how we wanted 

* sample.py: Creates a smaller sample of your data for testing code correctness
