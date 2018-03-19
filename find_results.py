"""
This file assumes that you have succesfully run the file race_parent_list.py
Thus you have already created ./page_contents/race_home_pages.txt

From here we need to check the metadata about the race (distance location etc)

We also need to establish how the race results are stored, and if they are infact available at all
"""

from bs4 import BeautifulSoup
import requests

class single_result:
    name = ""
    results_partial_link = ""
    country = ""
    div_rank = ""
    gen_rank = ""
    ovr_rank = ""
    swim = ""
    bike = ""
    run = ""
    total = ""
    points = ""
    
    def __init__(self, name, country, div_rank, gen_rank, ovr_rank, swim, bike, run, total, points):
        self.name = process_name(name)
        self.country = country
        self.div_rank = div_rank
        self.gen_rank = gen_rank
        self.ovr_rank = ovr_rank
        self.swim = swim
        self.bike = bike
        self.run = run
        self.total = total
        self.points = points
        
    def process_name(orig_name):
        first_last = orig_name.strip().split(", ")
        name = first_last[1] + " " + first_last[0]
        return(name)

def return_soup(page_link):
    req = requests.get(page_link).content
    soup = BeautifulSoup(req, "lxml")
    return(soup)

def append_to_file(file_path, list_to_file):
    f = open(file_path, 'a')
    for line in list_to_file:
        f.write(line + '\n')

print(return_soup("http://eu.ironman.com/triathlon/coverage/athlete-tracker.aspx?race=wisconsin&y=2003#axzz59wPZrEd1"))

def get_page_results(soup):
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

def process_page(parent_page):
    """
    Process each page, grab the relevant links
    if no 'Next' button exists, then the end we have finished, so return the list
    """
    page_conts = return_soup(parent_page)
    race_times = get_page_results(page_conts)
    append_to_file('./page_contents/race.txt', race_times)

    next_button_link = page_conts.find("a", {"class" : "nextPage"}).get("href")
    
    if next_button_link is not None:
        process_page(next_button_link)
    else:
        return(race_links)