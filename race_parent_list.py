"""
Scrape the parent list of races
This will give links to the home page for each race
From the home page for each race, it will be necessary to then select a list of potential races
eg 2008, 2009, 2010...
"""

from bs4 import BeautifulSoup
import requests

parent_page = "http://eu.ironman.com/triathlon/coverage/past.aspx#axzz59wPZrEd1"
races_output_file = "./page_contents/race_home_pages.txt"

def return_soup(page):
    """
    return the contents of a web page given the link
    """
    data = requests.get(page).content
    soup = BeautifulSoup(data, "lxml")
    return(soup)

# One article per race
def get_race_links(conts):
    """
    find all the links on a given page
    return a list
    """
    articles = conts.find_all('article')
    links = []
    for article in articles:
        link = article.find("a", {"class" : "titleLink"}).get("href")
        links.append(link)
    return(links)

def append_to_file(file_path, list_to_file):
    f = open(file_path, 'a')
    for line in list_to_file:
        f.write(line + '\n')

def process_page(page_link):
    """
    Process each page, grab the relevant links
    write links to txt file
    if no 'Next' button exists, then the end we have finished
    """
    page_conts = return_soup(page_link)
    race_links = get_race_links(page_conts)
    append_to_file(races_output_file, race_links)

    next_button_link = page_conts.find("a", {"class" : "nextPage"}).get("href")

    print(next_button_link)

    if next_button_link is not None:
        process_page(next_button_link)


process_page(parent_page)

