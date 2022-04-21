from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import pandas as pd
import time

class GlassdoorScraper:
    def __init__(self,url):
        self.url = url
        self.URL = None
        self.rows = []
        self.warnings = []
        self.full_link = None
        self.driver = None

    def open_website(self):
        PATH = "C:\Program Files (x86)\chromedriver.exe"
        self.driver = webdriver.Chrome(PATH)
        self.driver.get(self.url)

    def get_link(self,job_tag):
        link_origin = "https://www.glassdoor.co.uk/partner/jobListing.htm?"
        link_destination = job_tag.attrs["href"]
        link_destination = link_destination.split("?")[1]
        full_link = link_origin + link_destination
        return full_link

    def get_soup(self):
        # Get bs4 soup
        src = self.driver.page_source
        soup = BeautifulSoup(src, 'html.parser')
        return soup

    def get_soup4(self,url):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
        source = requests.get(url, headers=headers)
        soup = BeautifulSoup(source.content, 'html.parser')
        return soup

    def next_page(self):
        element = self.driver.find_element_by_xpath("//ul/li[29]")
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        self.driver.find_element_by_class_name("nextButton").click()
        time.sleep(4)

        try:
            self.driver.find_element_by_xpath("//span[@class='SVGInline modal_closeIcon']").click()
        except:
            pass

    def get_data(self, li_class = 'react-job-listing',
                 company_class="d-flex justify-content-between align-items-start",
                 job_class="job-link",
                 location_class="css-1buaf54",
                 old_class = "job-age",
                 salary_class = "detailSalary",
                 detail_class = "css-1yuy9gt ecgq1xb4"):

        soup = self.get_soup()
        matches = soup.find_all('li', class_=li_class)
        for match in matches:
            company = match.find("div", class_=company_class)
            company = company.get_text(separator=" ").strip()

            job_title = match.find("a", {"data-test":job_class})
            job_title = job_title.get_text(separator=" ").strip()

            location = match.find("span", class_=location_class)
            location = location.get_text(separator=" ").strip()

            old = match.find("div", {"data-test":old_class})
            old = old.get_text(separator=" ").strip()

            try:
                salary = match.find("span", {"data-test": salary_class})
                salary = salary.get_text(separator=" ").strip()
            except Exception as e:
                self.warnings.append(e)

            self.full_link = self.get_link(match.find("a",{"data-test":job_class}))
            soup2 = self.get_soup4(self.full_link)
            job_details = soup2.find("div", class_=detail_class).get_text(separator=" ").strip()
            self.rows.append([self.full_link, job_title, company, location, old, salary, job_details])

            print(len(self.rows))

if __name__ == "__main__":
    url = "https://www.glassdoor.co.uk/Job/london-data-engineer-jobs-SRCH_IL.0,6_IC2671300_KO7,20.htm"
    pages = 25
    print("Starting")
    bot = GlassdoorScraper(url)
    bot.open_website()

    for i in range(pages):
        bot.get_data(detail_class="css-1yuy9gt ecgq1xb4")
        bot.next_page()

    df = pd.DataFrame(bot.rows, columns = ["url", "job_title", "company_name", "location", "old", "salary", "job_details"])
    print("Finished")

# df.to_csv("glassdoor_accountant.csv", encoding='utf-8-sig')

# soup = bot.get_soup()
# matches = soup.find_all('li', class_='react-job-listing')
# match = matches[0]
#
# match.find("span", class_="css-1buaf54").text

df