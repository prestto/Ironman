"""
We are only interested in pages that have a results set
This should be in the recognised table format

Some pages have results in a pdf, or no results at all
Some pages show results for the incorrect year, ie, link says 2006
but results table is for 2017
"""


def return_soup(web_url):
    try:
        req = requests.get(web_url).content
    except:
        logging.debug("Could not retreive page: {}".format(web_url))
    else:
        return(BeautifulSoup(req, "lxml"))


