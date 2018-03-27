import logging
import importlib
from site_scraping_classes import race_parser, single_race, results_parser
import sqlite3 as sql
import re

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler('snoop.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# Insert all races to the db ------------ 
def process_race_pages(web_url, db_path):
    """
    loop recursively through all race pages
    initial race page is taken as an argument
    """
    race_page = race_parser(web_url, db_path)
    print("processing: {}".format(web_url))
    for article in race_page.articles:
        summary_race_info = single_race(article, db_path)
        print("race: {}".format(summary_race_info.title))
        if not summary_race_info.link_in_base():
            print("inserting: {}".format(summary_race_info.title))
            summary_race_info.insert_to_base()
    if race_page.get_next_page_link is not None:
        process_race_pages(race_page.next_page_link, db_path)

# # Page one of the race list from the ironman page
# parent_page = "http://eu.ironman.com/triathlon/coverage/past.aspx#axzz59wPZrEd1"
# # The base to which we will write races
db_path = "./database/ironbase.db"

# Grab all the links from the base
def pages_from_base(db_path):
    conn = sql.connect(db_path)
    c = conn.cursor()
    c.execute("select link from link_page")
    all_links = c.fetchall()
    conn.commit()
    conn.close()
    return(all_links)

page_tuples = pages_from_base(db_path)
first_results_pages = [x[0] for x in page_tuples]

# Save all results pages to the specified folder -------------------
def process_results_pages(web_url, output_folder, database_path):
    """
    Loop recursively through all results pages, starting from the top page
    this top page is found in the database ironbase.db
    """
    logger.info("Processing page: {}".format(web_url))
    results_page = results_parser(web_url, output_folder, database_path)
    
    print(results_page.page_type)

    logger.info("Writing to file: {}".format(results_page.file_name))
    results_page.write_to_file()

    if results_page.next_page_link is not None:
        process_results_pages(results_page.next_page_link, output_folder)


results_output_folder = "./page_contents"
for first_page_url in first_results_pages:
    process_results_pages(first_page_url, results_output_folder, db_path)













