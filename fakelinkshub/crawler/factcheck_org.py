

from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from tld import get_tld

import urllib.request
import re
import os


source_resource = []


def get_factcheckorg_page_links(scrape_link):
    page = urlopen(scrape_link)
    source = BeautifulSoup(page, 'html.parser')
    link_elements = source.find_all('h3')
    for ahref in link_elements:
        link_text = ahref.find_all('a', href=True)
        print(link_text[0].text, ' : ', link_text[0]['href'])
        scrape_factcheckorg_page(link_text[0]['href'])


def scrape_factcheckorg_page(scrape_link):
    page = urlopen(scrape_link)
    source = BeautifulSoup(page, 'html.parser')
    source = str(source)
    source_list = source.split(" ")
    # print(source_list)
    bool = False
    for rec in source_list:
        # print(rec)
        if bool and "</div>" in rec:
            bool = False
        if "Sources" in rec and any(["<h5>" in rec, "<b>" in rec, "<strong>" in rec, "<span>" in rec, 
                                     "<h3>" in rec, "<p><strong><span>" in rec, "</span>" in rec]):
            # print(rec)
            bool = True
        # if bool:
        #     print(rec)
        if bool and "href" in rec:
            # print(rec)
            try:
                if "https" in rec:
                    my_url = re.search("(?P<url>https?://[^\s]+)", rec).group("url")
                elif "http" in rec:
                    my_url = re.search("(?P<url>http?://[^\s]+)", rec).group("url")
                index = my_url.find('"')
                my_url = my_url[:index]
            except:
                pass
            try:
                if "web.archive.org" in my_url:
                    print(my_url[my_url.find("http", my_url.find("http") + 1):])    #Fake Link
                    source_resource.append({scrape_link: my_url[my_url.find("http", my_url.find("http") + 1):]})
                else:
                    filename, file_extension = os.path.splitext(my_url)             #Fake Link
                    if file_extension not in ['.pdf', '.txt', '.csv'] and '.gov' not in get_tld(my_url):
                        print(my_url)
                        source_resource.append({scrape_link: my_url})
            except Exception as e:
                print('Exception : ', e)
        # print(bool)

def factcheck_bot():
    scrape_factcheck = True
    page_num = 1
    while scrape_factcheck:
        try:
            get_factcheckorg_page_links('https://www.factcheck.org/fake-news/page/{}/'.format(str(page_num)))
            page_num += 1
            print(page_num)
        except urllib.error.HTTPError as e:
            print(e.code)
            scrape_factcheck = False
            return source_resource


if __name__ == "__main__":
    print(factcheck_bot())
    # scrape_factcheckorg_page('https://www.factcheck.org/2018/03/no-russian-arrest-warrant-george-soros/')
    # scrape_factcheckorg_page('https://www.factcheck.org/2018/03/no-russian-arrest-warrant-george-soros/')
    # https: // www.factcheck.org / 2018 / 03 / no - russian - arrest - warrant - george - soros /
    # result = snopes_bot()
    # print(result)
    # scrape_snopes_page('https://www.snopes.com/fact-check/amy-schumer-female-remake-saving-private-ryan/')
    # print(source_resource)
