"""
4 classes to process html pages stored locally.

  - gen_html_parser : parent class for single_results_page and athlete_meta
    - single_results_page : fed a html page, this will extract the 
      body and create a list of athlete time details in html format.
    - athlete_meta : extracts pertinent information from the meta type pages
  - personal_result : fed a single html table row by single_results_page, this 
  class handles the extraction and insertion to base of the data
"""

from bs4 import BeautifulSoup
from time import gmtime, strftime
import sqlite3 as sql
import logging
import os
import re

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('snoop.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class gen_html_parser():
    # Parent class of single_results_page and athlete_meta
    body = ""
    file_path = ""
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.body = self.get_body()

    def get_body(self):
        f = open(self.file_path, 'r')

        return(BeautifulSoup(f.read(), "lxml"))


class single_results_page(gen_html_parser):
    # processes both race times and meta pages 
    page_results = ""
    url = ""

    def __init__(self, file_path):
        logger.info('Initialising single_results_page with {}'.format(file_path))
        super().__init__(file_path)
        self.page_results = self.get_page_results()
        self.url = self.get_url()

    def get_page_results(self):
        event_results_page = self.body.find_all('table', id = "eventResults")
        rows = event_results_page[0].find_all("tr")
        results = [r for r in rows if r.find("th") is None]

        return(results)

    def get_url(self):
        base_url = self.body.find("meta", {"property" : "og:url"}).get("content")
        full_name = os.path.basename(self.file_path)
        clean_name = os.path.splitext(full_name)[0]

        return("{}/{}".format(base_url, clean_name))

class athlete_meta(gen_html_parser):
    # Specifically for meta type pages
    # Given a file path this extracts useful metadata
    bib_id = ""
    division = ""
    age = ""
    state = ""
    country = ""
    profession = ""
    meta_table = ""

    def __init__(self, file_path):
        super().__init__(file_path)

    def get_meta_info(self):
        main_table = self.body.find("div", {"class" : "moduleWrap eventResults resultsListing resultsListingDetails"})
        general_table = main_table.find("table", {"id" : "general-info"})

        return(general_table)

    def get_bib_id(self):
        label = general_table.find('td',text='BIB')

        return(label.nextSibling.nextSibling.text)

    def get_division(self):
        label = general_table.find('td',text='Division')

        return(label.nextSibling.nextSibling.text)

    def get_age(self):
        label = general_table.find('td',text='Age')

        return(label.nextSibling.nextSibling.text)

    def get_state(self):
        label = general_table.find('td',text='State')

        return(label.nextSibling.nextSibling.text)

    def get_country(self):
        label = general_table.find('td',text='Country')

        return(label.nextSibling.nextSibling.text)

    def get_profession(self):
        label = general_table.find('td',text='Profession')
        
        return(label.nextSibling.nextSibling.text)

    # def insert_to_base(self):
    #     # Insert the values to the base
    #     # Normal to check if the values are already in the base
    #     # Key autoincrementing on race_times so no PK conflicts possible,
    #     # but risk of duplication
    #     try:
    #         conn = sql.connect(self.db_path)
    #         c = conn.cursor()
    #         c.execute("""insert into athlete_meta ('name', 'bib_id', 'country', 'state', 'division', 
    #                   'age', 'profession', 'meta_url', 'scrape_date') values
    #                   (:name, :bib_id, :country, :state, :division, :age, 
    #                   :profession, :meta_url, :scrape_date);
    #                   """,
    #                   {"name" : self.name, "bib_id" : self.bib_id, "country" : self.country, "datetime" : strftime("%Y-%m-%d %H:%M:%S", gmtime()),
    #                   , "bike" : self.bike, "run" : self.run, 
    #                   "gen_rank" : self.gen_rank, "ovr_rank" : self.ovr_rank, "div_rank" : self.div_rank, 
    #                   "total" : self.total, "points" : self.points, "parent_url" : self.url,
    #                   "bib_id" : self.bib_id, "meta_link" : self.meta_link})
    #         conn.commit()
    #         logger.info("SUCCESS: For url {} inserted {} to base".format(self.url, self.name))
    #     except Exception as e:
    #         logger.error("FAILIURE: For url {} Failed to insert {}".format(self.url, self.name))
    #         print(e)
    #     finally:
    #         conn.close()

    # def is_in_base(self):
    #     # Check if a result is already in the base based on bib_id and url
    #     # returns a bool
    #     conn = sql.connect(self.db_path)
    #     c = conn.cursor()
    #     c.execute("""SELECT bib_id FROM race_times WHERE bib_id = :bib_id and parent_url = :parent_url;""",
    #               {"parent_url" : self.url, "bib_id" : self.bib_id})
    #     conn.commit()
    #     logger.info("SUCCESS: ".format(self.url, self.bib_id))
    #     if c.fetchone() is None:
    #         logger.info("Not in base bib: {} url: {}".format(self.bib_id, self.url))
    #         qry_result = False
    #     else:
    #         logger.info("In base bib: {} url: {}".format(self.bib_id, self.url))
    #         qry_result = True
    #     conn.close()
    #     return(qry_result)

class personal_result:
    # Specifically for summary results pages, this class is fed by 
    # single_results_page and will insert values to base..race_times
    results_raw = ""
    athlete_info = ""
    name = ""
    meta_link = ""
    country = ""
    div_rank = ""
    gen_rank = ""
    ovr_rank = ""
    swim = ""
    bike = ""
    run = ""
    total = ""
    points = ""
    db_path = ""
    url = ""
    bib_id = ""
    in_base = ""

    def __init__(self, results_table_html, url, db_path):
        # log start and ser options
        logger.info('Initialising personal_result with results_table_html: {}, url: {}, db: {}'.format(results_table_html, url, db_path))
        self.results_raw = results_table_html
        self.db_path = db_path
        self.url = url

    def extract_values(self):
        # Extract all useful values from the page 
        self.athlete_info = self.get_athlete_info()
        self.name = self.get_name()
        self.meta_link = self.get_meta_link()
        self.country = self.get_country()
        self.div_rank = self.get_div_rank()
        self.gen_rank = self.get_gen_rank()
        self.ovr_rank = self.get_ovr_rank()
        self.swim = self.get_swim()
        self.bike = self.get_bike()
        self.run = self.get_run()
        self.total = self.get_total()
        self.points = self.get_points()
        self.bib_id = self.get_bib_id()
        self.in_base = self.is_in_base()

    def get_athlete_info(self):
        return(self.results_raw.find_all("td"))

    def get_name(self):
        try:
            odd_name = self.athlete_info[0].text
            nm_ls = odd_name.split(',')
            proper_name = "{} {}".format(nm_ls[1].strip(), nm_ls[0].strip())
        except:
            proper_name = self.name
        return(proper_name)

    def get_meta_link(self):
        return(self.athlete_info[0].find_all("a")[0].get("href"))

    def get_country(self):
        return(self.athlete_info[1].text)

    def get_div_rank(self):
        return(self.athlete_info[2].text)

    def get_gen_rank(self):
        return(self.athlete_info[3].text)

    def get_ovr_rank(self):
        return(self.athlete_info[4].text)

    def get_swim(self):
        return(self.athlete_info[5].text)

    def get_bike(self):
        return(self.athlete_info[6].text)

    def get_run(self):
        return(self.athlete_info[7].text)

    def get_total(self):
        return(self.athlete_info[8].text)

    def get_points(self):
        return(self.athlete_info[9].text)

    def get_bib_id(self):
        return(re.search("(bidid=)(\d+)(&amp;|&)", self.meta_link).group(2))

    def insert_to_base(self):
        # Insert the values to the base
        # Normal to check if the values are already in the base
        # Key autoincrementing on race_times so no PK conflicts possible,
        # but risk of duplication
        try:
            conn = sql.connect(self.db_path)
            c = conn.cursor()
            c.execute("""insert into race_times ('name', 'country', 'datetime', 'swim', 'bike', 'run', 
                      'gen_rank', 'ovr_rank', 'div_rank', 'total', 'points', 'parent_url', 'bib_id', 'meta_link') values
                      (:name, :country, :datetime, :swim, :bike, :run, 
                      :gen_rank, :ovr_rank, :div_rank, :total, :points, :parent_url, :bib_id, :meta_link);
                      """,
                      {"name" : self.name, "country" : self.country, "datetime" : strftime("%Y-%m-%d %H:%M:%S", gmtime()),
                      "swim" : self.swim, "bike" : self.bike, "run" : self.run, 
                      "gen_rank" : self.gen_rank, "ovr_rank" : self.ovr_rank, "div_rank" : self.div_rank, 
                      "total" : self.total, "points" : self.points, "parent_url" : self.url,
                      "bib_id" : self.bib_id, "meta_link" : self.meta_link})
            conn.commit()
            logger.info("SUCCESS: For url {} inserted {} to base".format(self.url, self.name))
        except Exception as e:
            logger.error("FAILIURE: For url {} Failed to insert {}".format(self.url, self.name))
            print(e)
        finally:
            conn.close()

    def is_in_base(self):
        # Check if a result is already in the base based on bib_id and url
        # returns a bool
        conn = sql.connect(self.db_path)
        c = conn.cursor()
        c.execute("""SELECT bib_id FROM race_times WHERE bib_id = :bib_id and parent_url = :parent_url;""",
                  {"parent_url" : self.url, "bib_id" : self.bib_id})
        conn.commit()
        logger.info("SUCCESS: ".format(self.url, self.bib_id))
        if c.fetchone() is None:
            logger.info("Not in base bib: {} url: {}".format(self.bib_id, self.url))
            qry_result = False
        else:
            logger.info("In base bib: {} url: {}".format(self.bib_id, self.url))
            qry_result = True
        conn.close()
        return(qry_result)



