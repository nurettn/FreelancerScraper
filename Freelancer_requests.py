# https://github.com/PovilasKud/Freelancer-notifications/blob/master/main.py

import time

import requests
from lxml import html
from bs4 import BeautifulSoup as soup
import re

class FreelancerScraper():
    """
    Class with functionality of scraping freelancer.com
    """

    def __init__(self, categories):
        self.categories = categories
        self.init_links = []

    def _make_request(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            raise requests.ConnectionError
        else:
            return response

    def _get_all_links(self):
        temp_links = []
        response = self._make_request(self.categories)
        tree = html.fromstring(response.content)
        links = tree.xpath("//tr[contains(@class, 'ProjectTable-row')]/td[1]/a/@href")
        temp_links = temp_links + links
        return temp_links

    def _get_budget(self, url):
        response = self._make_request(url[0])
        tree = soup(response, 'html.parser')
        budget = tree.xpath("//span[@class='project-statistic-value']/text()")[0].strip()
        return budget

    def get_init_links(self):
        self.init_links = self._get_all_links()

    def getContainers(self, page_soup):
        try:
            containers = page_soup.find_all("tr", class_="ProjectTable-row project-details even" )
            table_body = page_soup.find('tbody', attrs={'class': 'ProjectTable-body'})
            return containers
        except Exception as e:
            print(e)

    def get_new_listings(self):
        response = requests.get(self.categories)

        html_bs4= soup(response.content, "html.parser")
        table_whole = html_bs4.find_all('table', attrs={"id":"project_table_static"})
        table_body = table_whole.find_all('tbody', attrs={"class": "ProjectTable-body"})

        rows =  self.getContainers(tree)
        new_listings = []
        for row in rows:
            link = row.xpath('td[1]/a/@href')
            if not link in self.init_links:
                self.init_links.append(link)

                listing = {
                    'title': ''.join(map(str, row.xpath('td[1]/a/text()'))),
                    'link': ''.join(map(str, link)),
                    'skills': ' | '.join(map(str, row.xpath('td[4]/a/text()'))),
                    'desc': ''.join(map(str, row.xpath('td[2]/text()'))),
                    'budget': ''.join(map(str, self._get_budget(link)))
                }
                new_listings.append(listing)

        return new_listings

