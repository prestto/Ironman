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
 - Check base existance in ./database/ironbase.db
 - Check tables:
    - links_page
    - race_times
    - results_page
"""
import os
import sqlite3 as sql

print("This file is being run from: {}\nChecking directory and database structure...".format({}))

# Check folder structure
def check_folder_existance(folder_path, create_if_absent):
    if os.path.isdir(folder_path):
        print("Good news: Folder {} is present".format(folder_path))
    elif os.path.isdir(folder_path) & create_if_absent == True:
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
full_path = './database/ironbase.db'
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

create_links_qry = """CREATE TABLE IF NOT EXISTS link_page (
                id integer primary key,
                link NVARCHAR(200),
                event_name nvarchar(100),
                datetime text,
                city NVARCHAR(100),
                country NVARCHAR(100),
                year_table int,
                location_table NVARCHAR(100),
                distance NVARCHAR(50),
                format NVARCHAR(50)
                );"""

create_results_page = """CREATE TABLE IF NOT EXISTS results_page (
                id integer primary key,
                link NVARCHAR(200),
                datetime text
                );"""

create_race_times = """CREATE TABLE IF NOT EXISTS race_times (
              id integer primary key,
              name NVARCHAR(100), 
              bib_id NVARCHAR(100),
              country NVARCHAR(100), 
              datetime TEXT, 
              swim TEXT, 
              bike TEXT, 
              run TEXT, 
              gen_rank NVARCHAR(10), 
              ovr_rank NVARCHAR(10), 
              div_rank NVARCHAR(10), 
              total NVARCHAR(10), 
              points NVARCHAR(10),
              parent_url NVARCHAR(200)
              );"""

query_base(create_links_qry)    # link_page
query_base(create_results_page) # results_page
query_base(create_race_times)   # race_times



