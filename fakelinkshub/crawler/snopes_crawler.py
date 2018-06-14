
from urllib.request import urlopen
from bs4 import BeautifulSoup

import urllib.request

source_resource = []


def get_snopes_page_links(scrape_link):
    page = urlopen(scrape_link)
    source = BeautifulSoup(page, 'html.parser')
    link_elements = source.find_all('meta', attrs={'itemprop': 'mainEntityOfPage'})
    for link in link_elements:
        scrape_snopes_page(link['content'])


def scrape_snopes_page(scrape_link):
    page = urlopen(scrape_link)
    source = BeautifulSoup(page, 'html.parser')
    link_elements = source.find_all('meta', attrs={'itemprop': 'sameAs'})
    print(scrape_link, ':', link_elements)
    if link_elements:
        print(scrape_link, ':', link_elements)
        # print(scrape_link, ':', link_elements[0]['content'])
        source_resource.append({scrape_link: link_elements[0]['content']})
        # if 'http://archive.is' in link_elements[0]['content']:
        #     # print(scrape_link, ':', link_elements[0]['content'])
        #     archiveis_bot(link_elements[0]['content'])


def archiveis_bot(scrape_link):
    # scrape_link = 'http://archive.is/3UZiI'
    print('--------')
    page = urlopen(scrape_link)
    source = BeautifulSoup(page, 'html.parser')
    print(source)
    link_elements = source.find_all('input', attrs={'name': 'q'})
    print(link_elements)


def snopes_bot():
    scrape_snopes = True
    page_num = 1
    while scrape_snopes:
        try:
            get_snopes_page_links('https://www.snopes.com/tag/fake-news/page/{}/'.format(str(page_num)))
            page_num += 1
            print(page_num)
        except urllib.error.HTTPError as e:
            scrape_snopes = False
            print(e.code)
            return source_resource


if __name__ == "__main__":
    result = snopes_bot()
    # print(result)
    # scrape_snopes_page('https://www.snopes.com/fact-check/amy-schumer-female-remake-saving-private-ryan/')
    # print(source_resource)
    # archiveis_bot('http://archive.is/3UZiI')