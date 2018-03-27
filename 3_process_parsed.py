"""
Using the modules found in the site_parsing_classes module
This module launches a script to process each file in the page_contents directory
It then inserts results to the base

Only race pages that have not been processes will be processed.
"""

from site_parsing_classes import single_results_page, personal_result
import os
# import re

database_path = "./database/ironbase.db"
pages_dir = "./page_contents"
pages_to_parse = ["{}/{}".format(pages_dir, x) for x in os.listdir(pages_dir)]

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


for html_page in pages_to_parse:
    results_page = single_results_page(html_page)

    for table_row in results_page.page_results:
        athlete_results = personal_result(table_row, results_page.url, database_path)
        athlete_results.extract_values()

        if athlete_results.in_base == False:
            athlete_results.insert_to_base()


# # Test single page:
# test_page = "/Users/tompreston/program/Ironman/page_contents/?p=69&race=california70.3&y=2005&ps=20.html"
# results_page = single_results_page(test_page)
# for table_row in results_page.page_results:
#     athlete_results = personal_result(table_row, results_page.url, database_path)
#     athlete_results.extract_values()
#     if athlete_results.in_base == False:
#         athlete_results.insert_to_base()


