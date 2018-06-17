"""
Cycle through the results for races not yet scraped, store html

link_page contains a list of all first results pages
scrape_page contains a list of all scrapes

pages_from_base returns a list of first resuts pages which have not already been scraped

these are then cleaned and passed to process_results_pages, which loops pqges until no next button
is found.

all html is stored in the specified output folder results_output_folder
"""
import logging
import importlib
from site_scraping_classes import results_parser
import sqlite3 as sql
import re

# Set up standard logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('snoop.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Set up params
db_path = "./database/ironbase.db"
results_output_folder = "./page_contents"

def pages_from_base(db_path):
    # Grab all the links from the base from the link_page table
    # Exclude results that are already in the scrape_page:
    #   these have already been scraped
    conn = sql.connect(db_path)
    c = conn.cursor()
    c.execute("""
                select link 
                from link_page 
                where link not in (
                    select link 
                    from scrape_page)
                """)
    all_links = c.fetchall()
    conn.commit()
    conn.close()

    return(all_links)

page_tuples = pages_from_base(db_path)
first_results_pages = [x[0] for x in page_tuples]


def process_results_pages(web_url, output_folder, database_path):
    # Loop recursively through all results pages, starting from the top page
    # this top page is found in the database ironbase.db
    logger.info("Processing page: {}".format(web_url))
    results_page = results_parser(web_url, output_folder, database_path)

    logger.info("Writing to file: {}".format(results_page.file_name))
    results_page.write_to_file()

    if results_page.next_page_link is not None:
        process_results_pages(results_page.next_page_link, output_folder, database_path)

"""
This currently overwrites the first_results_pages from the database
Scraping takes a long time, Nice is the chosen piority race for analysis
Comment this section once Nice has been scraped, and the other races will be processed
"""
first_results_pages = ["http://eu.ironman.com/triathlon/events/emea/ironman/france/results.aspx",
"http://eu.ironman.com/triathlon/events/emea/ironman/france/results.aspx?rd=20160605",
"http://eu.ironman.com/triathlon/events/emea/ironman/france/results.aspx?rd=20150628",
"http://eu.ironman.com/triathlon/events/emea/ironman/france/results.aspx?rd=20140629",
"http://eu.ironman.com/triathlon/events/emea/ironman/france/results.aspx?rd=20130623"]

for first_page_url in reversed(first_results_pages):
    process_results_pages(first_page_url, results_output_folder, db_path)
