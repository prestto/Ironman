from bs4 import BeautifulSoup
import requests
import logging
import re

logging.basicConfig(filename = "./logs/snoop_logg.log", level = logging.DEBUG, 
  format = "%(asctime)s:%(levelname)s:%(message)s")

class gen_parser:
    """
    Generic class with methods to save web pages to file
    Loops from first page until the loop button is no longer active
    """
    web_url = ""
    output_folder = ""
    file_name = ""
    file_path = ""
    body = ""
    next_page_link = ""

    def __init__(self, web_url, output_folder):
        self.web_url = web_url
        self.output_folder = output_folder
        self.file_name = self.get_file_name()
        self.file_path = self.get_full_path()
        self.body = self.return_soup()
        self.next_page_link = self.get_next_page_link()


    def get_file_name(self):
        try:
            file_name = re.match("(?:.+aspx\?)(.+)(?:#.+)", self.web_url).group(1)
        except:
            file_name = re.sub("/", "-", self.web_url)
        finally:
            return(file_name)


    def get_full_path(self):
        return("{}/{}.html".format(self.output_folder, self.file_name))


    def return_soup(self):
        try:
            req = requests.get(self.web_url).content
        except:
            logging.debug("Could not retreive page: {}".format(self.web_url))
        else:
            return(BeautifulSoup(req, "lxml"))


    def write_to_file(self):
        try:
            f = open(self.file_path, "w")
            f.write(str(self.body))
        except Exception as e:
            logging.debug("Could not print to file: {} error: {}".format(self.file_path, e))
        else:
            logging.debug("Results written succesfully to: {}".format(self.file_path))


    def get_next_page_link(self):
        try:
            next_page_link = self.body.find("a", {"class" : "nextPage"}).get("href")
        except:
            next_page_link = None
        return(next_page_link)



def process_pages(web_url, output_folder):

    results_page = gen_parser(web_url, output_folder)
    results_page.write_to_file()
    print(results_page.next_page_link)
    if results_page.next_page_link is not None:
        process_pages(results_page.next_page_link, output_folder)


addy = "http://eu.ironman.com/triathlon/events/emea/ironman/uk/results.aspx?p=101&ps=20#axzz59wPZrEd1"
output_folder = "./page_contents"

process_pages(addy, output_folder)






















