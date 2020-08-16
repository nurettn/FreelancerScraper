import time
from Discord import Discord
import requests
from bs4 import BeautifulSoup as soap
import re

# CATEGORIES - Pick skills you are interested in freelancer.com and copy link.
# CATEGORIES = 'https://www.freelancer.com/jobs/s-Python-Data_Mining-Web_Scraping-software_development-Django-programming/' # deprecated
CATEGORIES = 'https://www.freelancer.com/jobs/django_web-scraping_python_data-mining_microsoft-sql-server_tsql/?languages=en'
MAIN_LINK = "https://www.freelancer.com"

cache = "last_task"

def check_last():
    # TODO: Caching the last task topic

    container = containers[0]
    message = ""
    job_name, job_description, job_link = getItemName(container)
    job_price, bids_count = getPriceAndBidCount(container)
    message += f"__[{job_name}]({job_link})__"
    message += f"\nBids: **{bids_count}**"
    message += '\n' + 3 * '-' + f"**{job_price}**" + 3 * '-'
    message += f'\n{job_description}'
    Discord.Sender(message)
    time.sleep(60) # check per min
    # print(15*'*', '\n', message)

def getItemName(container):
    try:
        name_block = container.find("div", {"class": "JobSearchCard-primary-heading"})
        job_name = name_block.find("a", {"class": "JobSearchCard-primary-heading-link"}).get_text().strip()
        job_link = name_block.find("a", {"class": "JobSearchCard-primary-heading-link"}, href=True)
        job_link = MAIN_LINK + job_link["href"] + "details"
        job_description = container.find("p", {"class": "JobSearchCard-primary-description"})
        job_description = " ".join(job_description.contents[0].split())
        return job_name, job_description, job_link
    except Exception as e:
        print(e)


def getPriceAndBidCount(container):
    try:
        price_block = container.find("div", {"class": "JobSearchCard-secondary"})
        item_price_raw = price_block.find("div", {"class": "JobSearchCard-secondary-price"}).get_text().strip()
        item_price = re.findall(r"([$][\d]+)", item_price_raw)[0] + " Dolar"
        if 'Avg Bid' in item_price_raw:
            item_price += ' Avg Bid'
        count_of_bids = price_block.find("div", {"class": "JobSearchCard-secondary-entry"}).get_text().strip()
        return item_price, count_of_bids
    except Exception as e:
        print(e)


response = requests.get(CATEGORIES).text
page_soup = soap(response, "html.parser")
containers = page_soup.find_all("div", {"class": "JobSearchCard-item"})

for container in containers:
    message = ""
    job_name, job_description, job_link = getItemName(container)
    job_price, bids_count = getPriceAndBidCount(container)
    message += f"__[{job_name}]({job_link})__"
    message += f"\nBids: **{bids_count}**"
    message += '\n' + 3 * '-' + f"**{job_price}**" + 3 * '-'
    message += f'\n{job_description}'
    Discord.Sender(message)
    check_last()
    # print(15*'*', '\n', message)


