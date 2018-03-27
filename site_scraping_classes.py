"""

This module is designed to scrape results from the iroman website
It contains 1 parent class and 2 sub classes for parsing web pages:

- ger_parser <- parent

- race_parser <- inherits from class gen_parser, used to scrape links to results pages
then store results in the ironbase.db sqlite3 database

- results_parser <- inherits from class gen_parser, used to scrape and store in .http 
file each results page (race times)

There are also the 1 class for parsing the results from each type of page
- single_race <- used in conjunction with the class race_parser
contains functions to strip information from each article in the http

Why not store all http information from the race pages?
There are only 63 race pages, this will be efficient, and not add too much to stress on the ironman server
to reprocess.
it would not be great to scrape every race if a single detail was missed on each page.

"""

from bs4 import BeautifulSoup
import requests
import logging
import re
import sqlite3 as sql
import random
import string
from time import sleep
from time import gmtime, strftime


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler('snoop.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

"""

"""
# def logit(my_function):
#     def wrapper_function(*args, **kwargs):
#         logger.info(locals())
#         return(my_function(*args, **kwargs))
#     return(wrapper_function)


class gen_parser:
    """
    Parent class with functions common to the classes used to 
    get information from race and results pages
    """

    web_url = ""
    uid = ""
    augmanted_url = ""
    body = ""
    next_page_link = ""
    database_path = ""

    def __init__(self, web_url, database_path):
        self.database_path = database_path
        self.web_url = web_url
        self.uid = self.get_random_uid()
        self.augmanted_url = "{}#{}".format(self.web_url, self.uid)
        self.body = self.return_soup()
        self.next_page_link = self.get_next_page_link()
        self.be_responsible()
    
    def return_soup(self):
        try:
            req = requests.get(self.augmanted_url).content
        except:
            logging.debug("Could not retreive page: {}".format(self.augmanted_url))
        else:
            return(BeautifulSoup(req, "lxml"))

    def be_responsible(self):
        nap_time = random.uniform(3, 6)
        sleep(nap_time)

    def get_next_page_link(self):
        try:
            next_page_link = self.body.find("a", {"class" : "nextPage"}).get("href")
        except:
            next_page_link = None
        return(next_page_link)

    def get_random_uid(self):

        """
        uid should be:
        4 lower case
        2 numbers
        2 upper case
        1 lower
        1 upper
        2 numbers
        1 lower
        """

        user = [''.join(random.choices(string.ascii_lowercase, k=4)),
        ''.join(random.choices(string.digits, k=2)),
        ''.join(random.choices(string.ascii_uppercase, k=2)),
        ''.join(random.choices(string.ascii_lowercase + string.digits, k=1)),
        ''.join(random.choices(string.ascii_uppercase, k=1)),
        ''.join(random.choices(string.digits, k=2)),
        ''.join(random.choices(string.ascii_lowercase, k=1))]
        
        return(''.join(user))

class results_parser(gen_parser):
    """
    Parser specifically for the results pages
    """
    file_name = ""
    file_path = ""
    output_folder = ""
    page_type = ""

    def __init__(self, web_url, output_folder, database_path):
        super().__init__(web_url, database_path)
        self.output_folder = output_folder
        self.file_name = self.get_file_name()
        self.file_path = self.get_full_path()
        self.insert_to_base()
        self.page_type = self.check_page_type()

    def check_page_type(self):
        if self.body.find("div", {"class" : "moduleWrap liveStream"}):
            return("LIVE STREAM")
        elif self.body.find("table", id = "eventResults"):
            return("RESULTS")
        else:
            return("different...")

    def get_file_name(self):
        try:
            file_name = re.match("(?:.+aspx?)(.+)", self.web_url).group(1)
        except:
            file_name = re.sub("/", "-", self.web_url)
        finally:
            return(file_name)

    def get_full_path(self):
        return("{}/{}.html".format(self.output_folder, self.file_name))
    
    def write_to_file(self):
        try:
            f = open(self.file_path, "w")
            f.write(str(self.body))
        except Exception as e:
            logging.info("Could not print to file: {} error: {}".format(self.file_path, e))
        else:
            logging.info("Results written succesfully to: {}".format(self.file_path))

    def insert_to_base(self):
        conn = sql.connect(self.database_path)
        c = conn.cursor()
        c.execute("""insert into results_page ('link', 'datetime') values
                  (:link, :datetime);
                  """,
                  {"link" : self.web_url, "datetime" : strftime("%Y-%m-%d %H:%M:%S", gmtime())})
        conn.commit()
        conn.close()




class single_race:

    atricle = ""
    link = ""
    title = ""
    datetime = ""
    location = []
    city = ""
    country = ""
    year_link = ""


    def __init__(self, article, db_path):
        self.article = article
        self.database_path = db_path
        self.link = self.get_link()
        self.title = self.get_title()
        self.datetime = self.get_datetime()
        self.location = self.get_location()
        self.city = self.get_city()
        self.country = self.get_country()
        self.year_link = self.extract_link_year()

    def get_link(self):
        return(self.article.find("a", {"class" : "titleLink"}).get("href"))

    def get_title(self):
        return(self.article.find("h3").contents[0])

    def get_datetime(self):
        return(self.article.find("time").get("datetime"))

    def get_location(self):
        return(self.article.find("li", {"class" : "last"}).find("p").contents[1])

    def get_city(self):
        return(self.location.split(",")[0].strip())

    def get_country(self):
        try:
            country = self.location.split(",")[1].strip()
        except:
            country = ""
        return(country)

    def extract_link_year(self):
        return(re.search("(?:.+y=)(.+)", self.link)[1])

    def insert_to_base(self):
        conn = sql.connect(self.database_path)
        c = conn.cursor()
        c.execute("""insert into link_page ('link', 'event_name', 'datetime', 'city', 
                  'country') values
                  (:link, :event_name, :datetime, :city, :country);
                  """,
                  {"link" : self.link, "event_name" : self.title, "datetime" : self.datetime, 
                  "city" : self.city, "country" : self.country})
        conn.commit()
        conn.close()

    def link_in_base(self):
        conn = sql.connect(self.database_path)
        c = conn.cursor()
        c.execute("""
                  select count(link)
                  from link_page
                  where link = :link
                  """,
                  {"link" : self.link})
        if c.fetchone()[0] > 0:
            response = True
        else:
            response = False
        conn.commit()
        conn.close()
        return(response)

class race_parser(gen_parser):

    # output_folder = ""
    articles = []

    def __init__(self, web_url, database_path):
        super().__init__(web_url, database_path)
        self.articles = self.get_atricles()

    def get_atricles(self):
        """
        find all the links on a given page
        return a list
        """
        return(self.body.find_all('article'))
        





















