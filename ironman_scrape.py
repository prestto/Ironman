"""
This script will scrape the web page for Ironman Nice
"""

from bs4 import BeautifulSoup
import requests
import re
import string
import random
import time
import numpy as np
import csv

def return_soup(page):
    data = requests.get(page).content
    soup = BeautifulSoup(data, "lxml")
    return(soup)

def get_page_results(soup):
    event_results_page = soup.find_all('table', id = "eventResults")
    rows = event_results_page[0].find_all("tr")

    page_results = []

    for tr in rows[1:]:
    
        td = tr.find_all("td")
    
        partial_link = td[0].find_all("a")[0].get("href")
        name = td[0].text
        results_partial_link = td[0]
        country = td[1].text
        div_rank = td[2].text
        gen_rank = td[3].text
        ovr_rank = td[4].text
        swim = td[5].text
        bike = td[6].text
        run = td[7].text
        total = td[8].text
        points = td[9].text
    
        page_results.append([name, country, div_rank, gen_rank, ovr_rank, swim, bike, run, total, points, partial_link])
    
    return(page_results)

def get_random_uid():

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

def get_page_url(pg_no, user):
    
    base_page = "http://eu.ironman.com/triathlon/events/emea/ironman/france/results.aspx?p="

    race_specifics = "&rd=20170723&ps=20"
    
    full_url = base_page + pg_no + race_specifics + user

    return(full_url)

def application_wait():
    seconds = random.randint(1, 10)
    time.sleep(seconds)

def results_to_csv(results_list, file_name):
    with open(file_name, 'w') as csvfile:
    wrtr = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for table in file_name:
        for line in table:
            wrtr.writerow(line)

ovr_list = []
pg_no = 1

while True:

    application_wait()

    user = get_random_uid()

    url = get_page_url(str(pg_no), user)

    soup = return_soup(url)

    try:
        page_list = get_page_results(soup)
    except IndexError:
        break
    
    ovr_list.append(page_list)

    print(pg_no)
    pg_no += 1

results_to_csv(ovr_list, 'results.csv')

    


