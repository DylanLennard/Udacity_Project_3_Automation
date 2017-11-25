# DAND Project 3 Automation 
## Purpose  
The purpose of this project was to attempt to automate the process of auditing,
cleaning, and loading the data from web as XML, to CSV, to DB. 


## Files   
Some files were pre-written by Udacity and then further modified/completed by
myself, others were made by me for the purpose of completing the automation
process.  

* request_data.py (custom): get's data from http request)
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
