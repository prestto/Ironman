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
    - scrape_page
    - athlete_meta
"""
import os
import sqlite3 as sql

print("This file is being run from: {}\nChecking directory and database structure...".format({}))


def check_folder_existance(folder_path, create_if_absent):
    # Check folder structure
    # Option to create a folder if needed
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
check_folder_existance('./page_contents', True)
check_folder_existance('./page_contents/meta', True)


# Check database existance
# If does not exit, create the tables one by one
full_path = './database/ironbase.db'

if os.path.exists(full_path):
    print("Good news: {} is present".format(full_path))

else:
    print("Database {} not found".format(full_path))
    input("Do you want to create a new database {} ? This will be necessary to continue.")

def query_base(query_string):
    # Execute query in ./database/ironbase.db
    # No response is to be sent
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

create_scrape_details = """CREATE TABLE IF NOT EXISTS scrape_page (
                id integer primary key,
                link NVARCHAR(200),
                datetime text,
                page_type NVARCHAR(50)
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
              parent_url NVARCHAR(200),
              meta_link NVARCHAR(200)
              );"""

create_athlete_meta = """CREATE TABLE IF NOT EXISTS athlete_meta (
              id integer primary key,
              bib_id NVARCHAR(100),
              name NVARCHAR(100), 
              country NVARCHAR(100), 
              state NVARCHAR(100), 
              division NVARCHAR(100), 
              age NVARCHAR(100),
              profession NVARCHAR(100), 
              meta_url NVARCHAR(200),
              scrape_date NVARCHAR(100)
              );"""

query_base(create_links_qry)    # link_page
query_base(create_scrape_details) # scrape_page
query_base(create_race_times)   # race_times
query_base(create_athlete_meta)   # athlete_meta




