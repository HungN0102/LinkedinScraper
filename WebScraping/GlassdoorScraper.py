from bs4 import BeautifulSoup
import requests
import numpy as np
import re
import pandas as pd

class GlassdoorScraper:
    def __init__(self,url,pages):
        self.url = url[:-4]
        self.pages = pages
        self.URL = None
        self.rows = []

    def get_soup(self,url):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
        source = requests.get(url, headers=headers)
        soup = BeautifulSoup(source.content, 'html.parser')
        return soup

    def get_link(self,job_tag):
        link_origin = "https://www.glassdoor.co.uk/partner/jobListing.htm?"
        link_destination = job_tag.attrs["href"]
        link_destination = link_destination.split("?")[1]
        full_link = link_origin + link_destination
        return full_link

    def get_data(self, li_class = 'react-job-listing',
                 company_class="d-flex justify-content-between align-items-start",
                 job_class="jobLink job-search-key-1rd3saf eigr9kq1",
                 location_class="css-1buaf54 pr-xxsm job-search-key-iii9i8 e1rrn5ka4",
                 old_class = "d-flex align-items-end pl-std css-17n8uzw",
                 salary_class = "detailSalary",
                 detail_class = "css-1yuy9gt ecgq1xb3"):

        for i in range(1, self.pages + 1):
            if i == 1:
                self.URL = self.url + '.htm'
            else:
                self.URL = self.url + '_IP' + str(i) + '.htm'

            soup = self.get_soup(self.URL)
            matches = soup.find_all('li', class_=li_class)
            for match in matches:
                company = match.find("div", class_=company_class)
                company = company.get_text(separator=" ").strip()

                job_title = match.find("a", class_=job_class)
                job_title = job_title.get_text(separator=" ").strip()

                location = match.find("span", class_=location_class)
                location = location.get_text(separator=" ").strip()

                old = match.find("div", class_=old_class)
                old = old.get_text(separator=" ").strip()

                try:
                    salary = match.find("span", {"data-test": salary_class})
                    salary = salary.get_text(separator=" ").strip()
                except Exception as e:
                    salary = None

                full_link = self.get_link(match.find("a", class_=job_class))
                soup2 = self.get_soup(full_link)

                job_details = soup2.find("div", class_=detail_class).get_text(separator=" ").strip()

                self.rows.append([full_link, job_title, company, location, old, salary, job_details])
            print(len(self.rows))
if __name__ == "__main__":
    url = "https://www.glassdoor.co.uk/Job/uk-data-engineer-jobs-SRCH_IL.0,2_IN2_KO3,16.htm"
    pages = 25

    bot = GlassdoorScraper(url,pages)
    bot.get_data()

    df = pd.DataFrame(bot.rows, columns = ["url", "job_title", "company_name", "location", "old", "salary", "job_details"])