"""
Parse html pages stored in pages_dir to database_path inserting into race_times

Using the classes found in the site_parsing_classes module, this module 
launches a script to process each file in the page_contents directory inserting 
results to database_path, table: race_times

Race pages to be processed are found by listing all files in directory,
then filtering results already in the table race_times
"""
from site_parsing_classes import single_results_page, personal_result
import os
import sqlite3 as sql
import re

database_path = "./database/ironbase.db"
pages_dir = "./page_contents"

all_results_files = ["{}/{}".format(pages_dir, x) for x in os.listdir(pages_dir)]

def race_times_already_processed(db_path):
    # Return lines that are already processed
    conn = sql.connect(db_path)
    c = conn.cursor()
    c.execute("""SELECT parent_url 
            FROM race_times 
            GROUP BY parent_url;
            """)
    all_links = c.fetchall()
    conn.commit()
    conn.close()

    return(all_links)

# Call and clean race_times_already_processed
db_response = race_times_already_processed(database_path)
already_processed = [x[0] for x in db_response]

# pages_to_parse = all_results_files - already_processed
pages_to_parse = [x for x in all_results_files if x not in already_processed]

def update_athlete_info(pages_to_parse):
    # One page_to_parse contains details for many athletes
    # for each athlete on each page, if they are not already in 
    # the base, insert them.
    for html_page in pages_to_parse:
        results_page = single_results_page(html_page)

    for table_row in results_page.page_results:
        print("processing {}".format(results_page.url))
        try:
            athlete_results = personal_result(table_row, results_page.url, database_path)
            athlete_results.extract_values()

            if athlete_results.in_base == False:
                athlete_results.insert_to_base()
        except:
            print("unable to parse file: {}".format(results_page.url))

update_athlete_info(pages_to_parse)

# # Test single page:
# test_page = "/Users/tompreston/program/Ironman/page_contents/?p=69&race=california70.3&y=2005&ps=20.html"
# results_page = single_results_page(test_page)
# for table_row in results_page.page_results:
#     athlete_results = personal_result(table_row, results_page.url, database_path)
#     athlete_results.extract_values()
#     if athlete_results.in_base == False:
#         athlete_results.insert_to_base()


