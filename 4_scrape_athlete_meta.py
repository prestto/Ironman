"""
Scrapes metadata and detailed race times about athlete

links from the race results pages were inserted into the race_times table
a link to the athlete's personal page is included in this information
the personal page contains the following useful variables:

 - bib_id (unique to the race)
 - division
 - age
 - state
 - country
 - profession

+ detailed race times incl transition

***This is a long process, for the 14676 results for ironman nice alone, this script will take 10
10 days to run, based on a 6 second lag to ease server load***

"""
from site_scraping_classes import results_parser
import re
import os
import sqlite3 as sql
import logging

# Set up standard logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('snoop.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Params
db_path = "./database/ironbase.db"
pages_dir = "./page_contents/meta"

def athlete_metas_to_process(db_path):
    # Grab all the athlete meta links in the base from the race_times table
    # Exclude results that are already in the meta_url: no need to scrape twice
    conn = sql.connect(db_path)
    c = conn.cursor()
    c.execute("""
            SELECT meta_link 
            FROM race_times
            WHERE meta_link not in (
                SELECT meta_url
                FROM athlete_meta)
                and parent_url like '%france%';
            """)
    all_links = c.fetchall()
    conn.commit()
    conn.close()

    return(all_links)

# Get then clean list of metas to process
db_response = athlete_metas_to_process(db_path)
links_to_process = [x[0] for x in db_response]

def process_meta_page(url, pages_dir, db_path):
    # write the html of the meta file ready for site_parsing_classes
    logger.info("Processing page: {}".format(url))
    results_page = results_parser(url, pages_dir, db_path)

    logger.info("Writing to file: {}".format(results_page.file_name))
    results_page.write_to_file()


for meta_link in links_to_process:
    # Loop through all files returned from list to be processed
    process_meta_page(meta_link, pages_dir, db_path)



