import logging
from bs4 import BeautifulSoup as soup
from fake_useragent import UserAgent
from selenium import webdriver
import re

EXECUTABLE_PATH = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
MAIN_LINK = "https://www.freelancer.com"

class Common:
    @staticmethod
    def getDriver():
        try:
            user_agent = UserAgent()
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('user-agent={0}'.format(user_agent.random))
            driver = webdriver.Chrome(executable_path=EXECUTABLE_PATH, chrome_options=chrome_options)
            return driver
        except Exception as e:
            print(e)
            Common.sendLog("critical", e)

    @staticmethod
    def getItemName(container):
        try:
            name_block = container.find("div", {"class": "JobSearchCard-primary-heading"})

            job_name = name_block.find("a", {"class": "JobSearchCard-primary-heading-link"}).get_text().strip()
            job_link = name_block.find("a", {"class": "JobSearchCard-primary-heading-link"}, href=True)
            job_link = MAIN_LINK + job_link["href"]

            return job_name, job_link
        except Exception as e:
            Common.sendLog("critical", e)

    @staticmethod
    def getPriceAndBidCount(container):
        try:
            price_block = container.find("div", {"class": "JobSearchCard-secondary"})
            item_price_raw = price_block.find("div", {"class": "JobSearchCard-secondary-price"}).get_text().strip()
            item_price = re.findall("([$][\d]+)", item_price_raw)[0]
            if 'Avg Bid' in item_price_raw:
                item_price += ' Avg Bid'
            count_of_bids = price_block.find("div", {"class": "JobSearchCard-secondary-entry"}).get_text().strip()
            return item_price, count_of_bids
        except Exception as e:
            Common.sendLog("critical", e)

    @staticmethod
    def getContainers(driver):
        try:
            response = driver.page_source
            page_soup = soup(response, "html.parser")
            containers = page_soup.find_all("div", {"class": "JobSearchCard-item"})
            return containers
        except Exception as e:
            Common.sendLog("critical", e)

    @staticmethod
    def sendLog(level, message):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%d-%m-%Y %H:%M:%S',
                            filename='trade.log',
                            filemode='a+')
        if level == "debug":
            logging.debug(message)
        elif level == "info":
            logging.info(message)
        elif level == "warning":
            logging.warning(message)
        elif level == "error":
            logging.error(message)
        elif level == "critical":
            logging.critical(message)

    @staticmethod
    def getMaxPages(driver):
        max_page_number = None
        try:
            response = driver.page_source
            page_soup = soup(response, "html.parser")
            pagination = page_soup.find_all('div', class_="Pagination")
            pagination_items = pagination[0].find_all("li", class_="Pagination-item")
            max_page_number = int(max([item.get_text() for item in pagination_items]))
        except Exception as e:
            Common.sendLog("critical", e)

        return int(max_page_number)

    @staticmethod
    def getiCurrentPage(driver):
        "return number of current page"
        current_page = 0
        try:
            response = driver.page_source
            page_soup = soup(response, "html.parser")
            pagination_container = page_soup.find_all('div', class_="ProjectSearch-result Card")
            pagination_items = pagination_container[0].find_all("a", class_="btn number Pagination-link is-active")
            current_page = pagination_items[0].get_text()
        except Exception as e:
            Common.sendLog("critical", e)
        return current_page
