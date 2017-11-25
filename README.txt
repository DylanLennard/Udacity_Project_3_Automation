The files together are created to acquire, audit, clean, and ultimately insert 
data into a SQL database. 

* request_data.py (custom): get's data from http request)
* mapparser.py: gets a count of each tag tpe 
* tags.py: investigates the k attributes of each tag to look into addresses 
* users.py: get's count of unique users that contributed to data  
* audit.py: cleans up the street names and looks for more names to fix
* data.py: takes final cleaned up data and reads it into csv files for import
* schema.py: used for validation purposes 

* main.py(custom): will be the place we call all functions to run simultaneously
* sql.py(custom): creates the sql statements needed for a .sql file to make db
* insert_data.py (custom): inserts csv data directly into db via sqlite3
* check_files.py (custom): makes sure csv data comes out how we wanted 

* sample.py: Creates a sample of your data for practice and code is below