import time
import configparser
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup, Tag
from numpy import random

class LinkedinScraper:
    def __init__(self,account,link,li_class):
        # Retrieving account name and passwords
        parser = configparser.ConfigParser()
        parser.read("Webscraping/LinkedinAccount.conf")

        self.account_name = parser.get(account, "account")
        self.password = parser.get(account, "pass")
        self.link = link
        self.li_class = li_class
        self.driver = None
        self.soup = None
        self.jobs = []
        self.errors = 0
        self.warnings = []

    def logging_in(self):
        # Connecting to Linkedin
        PATH = "C:\Program Files (x86)\chromedriver.exe"
        self.driver = webdriver.Chrome(PATH)
        self.driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
        time.sleep(2)

        # Enter username
        elementID = self.driver.find_element_by_id("username")
        elementID.send_keys(self.account_name)

        # Enter password
        elementID = self.driver.find_element_by_id("password")
        elementID.send_keys(self.password)

        # Submit form
        elementID.submit()

    def scraped_site(self):
        # Navigate to Data Engineer at London Area
        self.driver.get(self.link)
        sleep_time = random.random()
        time.sleep(sleep_time + 1)

        # Retrieving html script first time
        self.driver.maximize_window()

    def get_soup(self):
        # Get bs4 soup
        src = self.driver.page_source
        soup = BeautifulSoup(src, 'html.parser')
        return soup

    def scroll_down(self):
        # Refresh initially
        self.driver.refresh()
        time.sleep(4)

        # Refresh if needed again
        soup = self.get_soup()
        matches = soup.find_all("li", class_= self.li_class)
        count = 0
        while len(matches) == 0 and count <= 10:
            soup = self.get_soup()
            matches = soup.find_all("li", class_=self.li_class)

            count += 1
            self.driver.refresh()
            time.sleep(2)

        # Scrolling to view
        running = True
        count = 0
        while running:
            self.soup = self.get_soup()
            try:
                id_toscroll = self.soup.find_all("li", class_=self.li_class)[count]["id"]
                element = self.driver.find_element_by_id(id_toscroll)
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
                count += random.randint(1,4)
                time.sleep(random.randint(1,4)/5)
            except:
                running = False

    def get_data(self):
        # List of posts
        element_list = self.soup.find_all("li",class_=li_class)
        for i in element_list:

            # Click on each post
            id = i.find("div", class_="full-width artdeco-entity-lockup__title ember-view")["id"]
            elementID = self.driver.find_element_by_id(id)
            elementID.click()
            time.sleep(5 + random.random() * 2)
            try:
                # Extract relevant data
                soup = self.get_soup()
                current_url = self.driver.current_url
                job_title = soup.find('h2', class_='t-24 t-bold').text
                company_name = soup.find('span', class_='jobs-unified-top-card__company-name').text
                no_employees = soup.find_all('li', class_='jobs-unified-top-card__job-insight')[1].text
                job_details = soup.find('div', class_='jobs-box__html-content jobs-description-content__text t-14 t-normal jobs-description-content__text--stretch').text
                try:
                    salary = soup.find_all('li', class_='jobs-unified-top-card__job-insight')[0].text
                except:
                    salary = None
                rows = [current_url, job_title, company_name, no_employees, salary, job_details]

                # Append to jobs list
                self.jobs.append(rows)

                number_of_jobs = len(self.jobs)
                if number_of_jobs % 50 == 0:
                    print(f"Total number of jobs extracted: {number_of_jobs}")

            except Exception as e:
                # Count errors
                self.errors += 1

                # Error type
                warning = [self.errors,e]

                # Add to list of warning errors
                self.warnings.append(warning)

    def get_page(self,page, ul="artdeco-pagination__pages artdeco-pagination__pages--number", li="data-test-pagination-page-btn"):
        # Page number
        page = str(page)
        m = self.soup.find("ul", class_=ul)
        try:
            # Get to next page
            id = m.find("li", {li: page})["id"]
            elementID = self.driver.find_element_by_id(id)
            elementID.click()
        except:
            # Click "..." button
            all_id = m.find_all("li")
            id = all_id[8]["id"]
            elementID = self.driver.find_element_by_id(id)
            elementID.click()

    def scrape(self):
        # Initializing the scraper
        self.logging_in()
        time.sleep(1)

        # Going to the site
        self.scraped_site()
        time.sleep(1)

        # Go to each page and scrape it
        for i in range(2, 42):
            self.scroll_down()
            self.get_data()
            self.get_page(i)

if __name__ == "__main__":
    account = "account1"
    job_site = "https://www.linkedin.com/jobs/search/?currentJobId=3023550702&geoId=90009496&keywords=%22data%20engineer%22&location=London%20Area%2C%20United%20Kingdom&refresh=true"
    li_class = "jobs-search-results__list-item occludable-update p0 relative scaffold-layout__list-item ember-view"
    bot = LinkedinScraper(account,job_site,li_class)
    bot.scrape()


df = pd.DataFrame(bot.jobs, columns = ["url","job_title","company_name" ,"number_employees" ,"salary" ,"job_details"])
# df.to_csv("linkedin_dataset.csv", encoding='utf-8-sig')
