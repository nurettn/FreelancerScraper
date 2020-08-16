from Common import Common

# use requests instead of selenium

SITE_LINK = "https://www.freelancer.com/work/projects/?w=f&skills=13,95,113,695,1114&languages=en,tr"

delay_time = 10


def run():
    driver = Common.getDriver()
    driver.get(SITE_LINK)

    # m_cMaxPages = Common.getMaxPages(driver)

    # for page_count in range(1, m_cMaxPages):
    #     print("hello")
        # time.sleep(delay_time)
    Common.sendLog("info", 'The {0}. page is analyzing'.format(Common.getiCurrentPage(driver)))
    containers = Common.getContainers(driver)


    for container in containers:
        print('**'*30)
        job_name, job_link = Common.getItemName(container)
        print("Job name: ", job_name, "\nJob link: ", job_link)
        job_price, bids_count = Common.getPriceAndBidCount(container)
        print(3*'-', job_price, "Dolar", 3*'-')
        print("Number of bits:", bids_count)

    # driver.quit()