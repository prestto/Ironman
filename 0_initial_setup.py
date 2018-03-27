"""
This file checks tat the following exist, and are correctly configured:
 - Folder structure
 - Database
 - 
 Folder structure
	./database
	./documentation
	./page_contents

Database
add db schema for clarity
"""
import os
import sqlite3 as sql

print("This file is being run from: {}\nChecking directory and database structure...".format({}))

# Check folder structure
def check_folder_existance(folder_path, create_if_absent):
	if os.path.isdir(folder_path):
		print("Good news: Folder {} is present".format(folder_path))
	elif os.path.isdir(folder_path) & create_if_absent = True:
		print("Folder {} not present, creating...")
		try:
			os.mkdir(folder_path)
		except Exception as e:
			print("Failed to create folder {}\n Exception: {}".format(folder_path, e))
	else:
		print("Folder {} not present")

check_folder_existance('./database', True)
check_folder_existance('./documentation', False)
check_folder_existance('./database', True)

# Check database existance
# If does not exit, create the tables one by one
if os.path.exists(full_path):
	print("Good news: {} is present".format(full_path))
else:
	print("Database {} not found".format(full_path))
	input("Do you want to create a new database {} ? This will be necessary to continue.")


def query_base(query_string):
	"""
	Execute query in ./database/ironbase.db
	No response is to be sent
	"""
	db_path = "./database/ironbase.db"
	conn = sql.connect(db_path)
	print("Connected to base {}".format(db_path))
	c = conn.cursor()
	print("Executing query: {}".format(query_string))
	try:
		req = c.execute(query_string)
		conn.commit()
	except Exception as e:
		print("Query not executed!\n{}".format(e))

	finally:
		conn.close()

query_base() # link_page
query_base() # race_times
query_base() # results_page

# print(os.path.isdir("/home/el"))
# print(os.path.exists("/home/el/myfile.txt"))