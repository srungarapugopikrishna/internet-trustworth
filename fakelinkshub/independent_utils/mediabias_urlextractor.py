

from urllib.request import urlopen
from bs4 import BeautifulSoup


# scrape_link = 'https://mediabiasfactcheck.com/free-thought-project/'


def extract_url(scrape_link):
    page = urlopen(scrape_link)
    source = BeautifulSoup(page, 'html.parser')
    links = source.find_all('p')
    for ahref in links:
        if 'Source:' in ahref.text:
            link_text = ahref.find_all('a', href=True)
            return link_text[0]['href']
