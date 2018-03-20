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

class gen_parser:
    """
    Parent class with functions common to the classes used to 
    get information from race and results pages
    """

    web_url = ""
    body = ""
    next_page_link = ""

    def __init__(self, web_url):
        self.web_url = web_url
        self.body = self.return_soup()
        self.next_page_link = self.get_next_page_link()

    def return_soup(self):
        try:
            req = requests.get(self.web_url).content
        except:
            logging.debug("Could not retreive page: {}".format(self.web_url))
        else:
            return(BeautifulSoup(req, "lxml"))

    def get_next_page_link(self):
        try:
            next_page_link = self.body.find("a", {"class" : "nextPage"}).get("href")
        except:
            next_page_link = None
        return(next_page_link)

class results_parser(gen_parser):
    """
    Parser specifically for the results pages
    """
    file_name = ""
    file_path = ""
    output_folder = ""

    def __init__(self, web_url, output_folder):
        super().__init__(web_url, output_folder)
        self.file_name = self.get_file_name()
        self.file_path = self.get_full_path()
        self.output_folder = output_folder

    def get_file_name(self):
        try:
            file_name = re.match("(?:.+aspx\?)(.+)(?:#.+)", self.web_url).group(1)
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
            logging.debug("Could not print to file: {} error: {}".format(self.file_path, e))
        else:
            logging.debug("Results written succesfully to: {}".format(self.file_path))



class single_race:

    atricle = ""
    link = ""
    title = ""
    datetime = ""
    location = []
    city = ""
    country = ""
    year_link = ""
    database_path = ""

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

    output_file = ""
    articles = []

    def __init__(self, web_url, db_path):
        super().__init__(web_url)
        self.articles = self.get_atricles()

    def get_atricles(self):
        """
        find all the links on a given page
        return a list
        """
        return(self.body.find_all('article'))
        
    # def append_to_file(self, file_path, list_to_file):
    #     f = open(file_path, 'a')
    #     for line in list_to_file:
    #         f.write(line + '\n')

# Insert all races to the db -------------------------------------   
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

# Page one of the race list from the ironman page
parent_page = "http://eu.ironman.com/triathlon/coverage/past.aspx#axzz59wPZrEd1"
# The base to which we will write races
db_path = "./database/ironbase.db"
# Launch
process_race_pages(parent_page, db_path)

# Save all results pages to the specified folder -------------------
def process_results_pages(web_url, output_folder):
    """
    Loop recursively through all results pages, starting from the top page
    this top page is found in the database ironbase.db
    """
    results_page = results_parser(web_url, output_folder)
    results_page.write_to_file()
    print(results_page.next_page_link)
    if results_page.next_page_link is not None:
        process_results_pages(results_page.next_page_link, output_folder)

# start_page_races = "http://eu.ironman.com/triathlon/events/emea/ironman/uk/results.aspx?p=101&ps=20#axzz59wPZrEd1"
# results_output_folder = "./page_contents"
# process_pages(addy, results_output_folder)



















