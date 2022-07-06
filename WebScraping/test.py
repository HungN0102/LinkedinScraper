from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import pandas as pd
import time
import csv
from datetime import date

class GlassdoorScraper:
    def __init__(self, url, file_tosave, pages, to_save):
        self.url = url
        self.file_tosave = file_tosave
        self.pages = pages
        self.to_save = to_save

        self.URL = None
        self.rows = []
        self.warnings = []
        self.full_link = None
        self.driver = None
        self.df = None
        self.today = date.today().strftime("%d/%m/%Y")

    def open_website(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        PATH = "C:\Program Files (x86)\chromedriver.exe"
        self.driver = webdriver.Chrome(PATH,options=options)
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
                 detail_class = "css-58vpdc ecgq1xb5"):

        soup = self.get_soup()
        matches = soup.find_all('li', class_=li_class)
        for match in matches:
            try:
                company = match.find("div", class_=company_class)
                company = company.get_text(separator=" ").strip()
            except:
                company = None
                print("Error company")

            try:
                job_title = match.find("a", {"data-test":job_class})
                job_title = job_title.get_text(separator=" ").strip()
            except:
                job_title = None
                print("Error job_title")

            try:
                location = match.find("span", class_=location_class)
                location = location.get_text(separator=" ").strip()
            except:
                location = None
                print("Error location")

            try:
                old = match.find("div", {"data-test":old_class})
                old = old.get_text(separator=" ").strip()
            except:
                old = None


            try:
                salary = match.find("span", {"data-test": salary_class})
                salary = salary.get_text(separator=" ").strip()
            except Exception as e:
                salary = None
                print("Error salary")

            try:
                self.full_link = self.get_link(match.find("a",{"data-test":job_class}))
                soup2 = self.get_soup4(self.full_link)
                job_details = soup2.find("div", class_=detail_class).get_text(separator=" ").strip()
            except:
                job_details = None
                print("Error details")
            self.rows.append([self.today, self.full_link, job_title, company, location, old, salary, job_details])

            print(len(self.rows))

    def run_me(self):
        print("Starting")
        self.open_website()

        for i in range(self.pages):
            self.get_data()
            self.next_page()

        self.df = pd.DataFrame(self.rows, columns=["date","url", "job_title", "company_name", "location", "old", "salary", "job_details"])
        if self.to_save:
            # self.df.to_csv(self.file_tosave, encoding='utf-8-sig')
            with open(self.file_tosave,"a",newline="", encoding='utf-8-sig') as f:
                for row in self.rows:
                    csv_writer = csv.writer(f)
                    csv_writer.writerow(row)

        self.driver.close()
        print("Finished")

if __name__ == "__main__":
    urls = ["https://www.glassdoor.co.uk/Job/london-software-engineer-jobs-SRCH_IL.0,6_IC2671300_KO7,24.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=software%2520engineer&typedLocation=London%252C%2520England&context=Jobs&dropdown=0"]
    file_tosaves = ["glassdoor_swe.csv"]

    url_to_file_lists = [(x, y, 6, True) for x, y in zip(urls, file_tosaves)]

    for url, file, page, to_save in url_to_file_lists:
        bot = GlassdoorScraper(url, file, page, to_save)
        #bot.run_me()


bot.open_website()
bot.get_soup()

def get_soup4(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36'}
    source = requests.get(url, headers=headers)
    soup = BeautifulSoup(source.content, 'html.parser')
    return soup

def get_data(self, li_class = 'react-job-listing',
                 company_class="d-flex justify-content-between align-items-start",
                 job_class="job-link",
                 location_class="css-1buaf54",
                 old_class = "job-age",
                 salary_class = "detailSalary",
                 detail_class = "css-58vpdc ecgq1xb5"):

        soup = self.get_soup()
        matches = soup.find_all('li', class_=li_class)
        for match in matches:
            try:
                self.full_link = self.get_link(match.find("a",{"data-test":job_class}))
                soup2 = get_soup4(self.full_link)
                print(soup2)
                job_details = soup2.find("div", class_=detail_class).get_text(separator=" ").strip()
            except:
                job_details = None
                print("Error details")
            
get_data(self=bot)


get_soup4("https://www.glassdoor.co.uk/job-listing/graduate-software-engineer-inspiring-interns-JV_IC2671300_KO0,26_KE27,44.htm?jl=1007923509197&pos=130&ao=1110586&s=58&guid=00000181d41ebc2f8384edbd1963a7e4&src=GD_JOB_AD&t=SR&vt=w&ea=1&cs=1_3c841671&cb=1657121193662&jobListingId=1007923509197&cpc=9908D8D4413DBB8A&jrtk=3-0-1g7a1tf7pkckl801-1g7a1tf87g2e4800-9aff2e8847d2f5c0--6NYlbfkN0DzwreoEVFOkXRcFH1aYDKs9BsTnM4S4dXogYMNQuxRsWEvU3NmJBXmQipkwYVPqOwydgP7d-B53NJyCOp7dB7jDvcZSg6QNGeTSuL46B9ohBKI2wJVTWx3FQgHEAIzCPpVbw6a0m-W_QLxEBeCA9ubwwxoXgSCBCqiMJ7cAg41vbW6CnUYc89YMxYZ6YLxrzSJprp05vF7bzCLpuMAu7ITf422AaK-y9VGIOCkAI07xlrVsb5NOxThfCzH4s5zgLXqXHFqJ3XmhnvaBF7ot2RRuePqPspBDJrINTJkf0IGfcYDlmNRdftTTvt23gT6mfcKqJVleILmqbs0_HbwLsOHtT6CF9YXNBQcPvOG-Br1VgiX5PfC7yi_DLWoiUY_SLIxZP794hA2Wp6ri6ZT-TwL7wAs3_PG6UA4KTBJDhGPYX-Mx4eJV2AdVuI121SnmOTdgPbFUzaenOsyMK39rSbl2LEhi4ry0F3o2AOnxo-vXx28749lrW0mbcCAn0vHkjT5mB4t3jnG_g%3D%3D&ctt=1657121592246")
