import logging
import importlib
from site_scraping_classes import results_parser
import sqlite3 as sql
import re

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler('snoop.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

db_path = "./database/ironbase.db"


def pages_from_base(db_path):
    """
    Grab all the links from the base from the link_page table
    Exclude results that are already in the results_table
    These have already been scraped
    """
    conn = sql.connect(db_path)
    c = conn.cursor()
    c.execute("""
                select link 
                from link_page 
                where link not in (
                    select link 
                    from results_page)
                """)
    all_links = c.fetchall()
    conn.commit()
    conn.close()

    return(all_links)

page_tuples = pages_from_base(db_path)
first_results_pages = [x[0] for x in page_tuples]

# # Save all results pages to the specified folder -------------------
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
        process_results_pages(results_page.next_page_link, output_folder, database_path)


results_output_folder = "./page_contents"
for first_page_url in reversed(first_results_pages):
    process_results_pages(first_page_url, results_output_folder, db_path)













