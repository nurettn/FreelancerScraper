# Freelancer(.com) Scraper

Proejct scrapes the jobs page for given link and sends a message for each job, then starts to check the topmost job on the page for each interval and checks if a new job is posted.

### About project

  - Sends all job alerts to Discord via webhooks
  - The project is built with requests and BeautifulSoup libraries

### Usage



1. Firstly, ick skills you are interested in from [this link](https://www.freelancer.com/jobs/django_web-scraping_python_data-mining_microsoft-sql-server_tsql/?languages=en) and paste in the code
2. Open your Discord server settings, create a webhook from integrations tab, copy and paste in the code 
3. Run the project.

### Installation

```sh
$ pip install requirements
```

### Development

If you want to contribute to the project don't forget to add docstrings and use `pip freeze > requirements.txt` 


### License
This repository is licensed under the MIT License. Please see the [LICENSE](https://github.com/nurettinabaci/BlogProject/blob/master/LICENCE) file for more details.