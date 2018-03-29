"""
Parse athlete meta pages stored in ./page_contents/meta to database_path athlete_meta

Athlete meta containd data to be used as explanatory variables:
 - bib_id (unique to the race)
 - division
 - age
 - state
 - country
 - profession

Only race pages that have not been processes will be processed.
"""
from site_parsing_classes import single_results_page, gen_html_parser, athlete_meta
import os
import sqlite3 as sql
import re

database_path = "./database/ironbase.db"
pages_dir = "./page_contents/meta"
pages_to_parse = ["{}/{}".format(pages_dir, x) for x in os.listdir(pages_dir)]

# # Grab all pages not already parsed
# db_response = pages_from_base(database_path)
# pages_to_parse = [x[0] for x in db_response]

def update_athlete_info(pages_to_parse):
    # process the athletes meta page
    # only insert to base if not already present
    for html_page in pages_to_parse:
        results_page = single_results_page(html_page)

        for table_row in results_page.page_results:
            athlete_results = personal_result(table_row, results_page.url, database_path)
            athlete_results.extract_values()

            if athlete_results.in_base == False:
                athlete_results.insert_to_base()

update_athlete_info(pages_to_parse)

# # Test single page:
# test_page = "/Users/tompreston/program/Ironman/page_contents/?p=69&race=california70.3&y=2005&ps=20.html"
# results_page = single_results_page(test_page)
# for table_row in results_page.page_results:
#     athlete_results = personal_result(table_row, results_page.url, database_path)
#     athlete_results.extract_values()
#     if athlete_results.in_base == False:
#         athlete_results.insert_to_base()


