from bs4 import BeautifulSoup
import requests
import logging

logging.basicConfig(filename = "./logs/snoop_logg.log", level = logging.DEBUG, 
  format = "%(asctime)s:%(levelname)s:%(message)s")

class gen_parser:
    """Contains the methods for a generic parser"""
    def return_soup(page_link):
      try:
          req = requests.get(page_link).content
      except error:
          logging.error("Could not retreive page: {}".format(page_link))
      else:
          soup = BeautifulSoup(req, "lxml")
          return(soup)

    def append_to_file(file_path, list_to_file):
        try:
            f = open(file_path, 'a')
            for line in list_to_file:
                f.write(line + '\n')
        except:
            logging.error("Could not print to file: {}".format(file_path))
        else:
            logging.debug("Results written succesfully to: {}".format(file_path))

class specific_race_results(gen_parser):

    def __init__(self, base_page):

        self.base_page = base_page

    def get_results_table(self, soup):
        """
        given the http for a page this function returns
        a list of 
        """

        # Add a try here

        event_results_page = soup.find_all('table', id = "eventResults")
        rows = event_results_page[0].find_all("tr")

        page_results = []

        for tr in rows[1:]:
        
            td = tr.find_all("td")

            athlete = single_result(name = td[0].text,
                                    country = td[1].text,
                                    div_rank = td[2].text,
                                    gen_rank = td[3].text,
                                    ovr_rank = td[4].text,
                                    swim = td[5].text,
                                    bike = td[6].text,
                                    run = td[7].text,
                                    total = td[8].text,
                                    points = td[9].text
                                   )

        
            page_results.append([athlete.name, athlete.country, athlete.div_rank, athlete.gen_rank, athlete.ovr_rank, 
                                athlete.swim, athlete.bike, athlete.run, athlete.total, athlete.points])
        
            del athlete
            
        return(page_results)

    def process_page(self, parent_page):
        """
        Process each page, grab the relevant links
        if no 'Next' button exists, then the end we have finished, so return the list
        """
        output_file = "'./page_contents/race.txt'"

        page_conts = return_soup(parent_page)
        race_times = get_page_results(page_conts)
        append_to_file(output_file, race_times)

        # Move on to next file or exit sub
        next_button_link = page_conts.find("a", {"class" : "nextPage"}).get("href")
        if next_button_link is not None:
            process_page(next_button_link)
        else:
            return(race_links)

    def results_to_file(self):
        process_page(base_page)

wisconsin = "http://eu.ironman.com/triathlon/coverage/athlete-tracker.aspx?race=wisconsin&y=2003#axzz59wPZrEd1"
b = specific_race_results(wisconsin)
b.results_to_file










