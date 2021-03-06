"""
Process race home pages 

Loop recursively through all pages containing races.

Details of each race are scraped then parsed immediately
html not stored as:
- there are only 70 pages of races, this can be scraped again quickly
- the races per page will change as new races are added
"""

import logging
from site_scraping_classes import race_parser, single_race

# Set up standard logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('snoop.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def process_race_pages(web_url, db_path):
    # loop recursively through all race pages
    # initial race page is taken as an argument
    race_page = race_parser(web_url, db_path)
    logger.info("Processing: {}".format(web_url))

    for article in race_page.articles:
        summary_race_info = single_race(article, db_path)
        logger.info("race: {}".format(summary_race_info.title))

        if not summary_race_info.link_in_base():
            logger.info("inserting: {}".format(summary_race_info.title))
            print("inserting: {}".format(summary_race_info.title))
            summary_race_info.insert_to_base()

        else:
            logger.info("Already present in base {}".format(summary_race_info.title))
            print("Already present in base {}".format(summary_race_info.title))

    if race_page.get_next_page_link is not None:
        process_race_pages(race_page.next_page_link, db_path)

# parent_page is page one of the race list from the ironman page
parent_page = "http://eu.ironman.com/triathlon/coverage/past.aspx#axzz59wPZrEd1"
db_path = "./database/ironbase.db"

process_race_pages(parent_page, db_path) 
web_url, output_folder, database_path
