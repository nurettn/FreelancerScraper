from bs4 import BeautifulSoup as soap
from Discord import Discord
import time
import requests
import re

# CATEGORIES - Pick skills you are interested in freelancer.com and copy link.
CATEGORIES = 'https://www.freelancer.com/jobs/django_web-scraping_python_data-mining_' \
             'microsoft-sql-server_tsql/?languages=en'
MAIN_LINK = "https://www.freelancer.com"

last_job_name = ""  # global var


def get_item_name(container):
    """Returns the job name, its description and the link of job detail page."""
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


def get_price_and_bid_count(container):
    """Returns the job price and total number of bids."""
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


def get_containers():
    """Sends a request and returns all of the div containers for jobs as a list """
    response = requests.get(CATEGORIES).text
    if response.status_code != 200:
        raise requests.ConnectionError

    page_soup = soap(response, "html.parser")
    containers = page_soup.find_all("div", {"class": "JobSearchCard-item"})
    return containers


def check_last():
    """Checks for the last posted job, if it wasn't previously posted
    then sends job detail to Discord channel via webhook."""
    global last_job_name
    while 1:
        containers = get_containers()
        container = containers[0]
        message = ""
        try:
            job_name, job_description, job_link = get_item_name(container)
        except Exception as e:
            print(e)
        # check if there is a new job
        if job_name != last_job_name:
            try:
                job_price, bids_count = get_price_and_bid_count(container)
            except Exception as e:
                print(e)
            last_job_name = job_name
            message += f"__[{job_name}]({job_link})__"
            message += f"\nBids: **{bids_count}**"
            message += '\n' + 3 * '-' + f"**{job_price}**" + 3 * '-'
            message += f'\n{job_description}'
            Discord.Sender(message)
            # print(15*'*', '\n', message)
        time.sleep(30)  # check every 30 sec


def run():
    """Scrapes the first page and then sends all of job
    details to Discord channel via webhook."""
    containers = get_containers()
    for container in containers:
        message = ""
        try:
            job_name, job_description, job_link = get_item_name(container)
            job_price, bids_count = get_price_and_bid_count(container)
        except Exception as e:
            print(e)
        message += f"__[{job_name}]({job_link})__"
        message += f"\nBids: **{bids_count}**"
        message += '\n' + 3 * '-' + f"**{job_price}**" + 3 * '-'
        message += f'\n{job_description}'
        time.sleep(4)
        try:
            Discord.Sender(message)
        except Exception as e:
            print(e)
        # print(15*'*', '\n', message)
    check_last()


# Run driver function
run()
