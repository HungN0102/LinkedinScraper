import time
import configparser
import pandas as pd

from selenium import webdriver
from bs4 import BeautifulSoup
from numpy import random

# Retrieving account name and passwords
parser = configparser.ConfigParser()
parser.read("Webscraping/LinkedinAccount.conf")
account_name = parser.get("account1", "account")
password = parser.get("account1", "pass")

# Connecting to Linkedin
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
time.sleep(2)

# Logging in
elementID = driver.find_element_by_id("username")
elementID.send_keys(account_name)

elementID = driver.find_element_by_id("password")
elementID.send_keys(password)

elementID.submit()
time.sleep(random.random())

# Navigate to Data Engineer at London Area
link = "https://www.linkedin.com/jobs/search/?currentJobId=3023550702&geoId=90009496&keywords=%22data%20engineer%22&location=London%20Area%2C%20United%20Kingdom&refresh=true"
driver.get(link)
time.sleep(random.random() +1)

# Retrieving html script first time
driver.maximize_window()

# Definitions
def get_page(page,ul="artdeco-pagination__pages artdeco-pagination__pages--number",li="data-test-pagination-page-btn"):
    page = str(page)
    m = soup.find("ul",class_=ul)
    try:
        id = m.find("li",{li:page})["id"]
        elementID = driver.find_element_by_id(id)
        elementID.click()
    except:
        all_id = m.find_all("li")
        id = all_id[8]["id"]
        elementID = driver.find_element_by_id(id)
        elementID.click()

def get_soup(driver):
    src = driver.page_source
    soup = BeautifulSoup(src, 'html.parser')
    return soup

# Extracting data
jobs = []
errors = 0

for page in range(2,41):
    # Scroll to the bottom of the page

    driver.refresh()
    time.sleep(random.random()*5 + 5)
    running = True
    count = 0
    while running:
        soup = get_soup(driver)
        try:
            id_toscroll = soup.find_all("li", class_="jobs-search-results__list-item occludable-update p0 relative scaffold-layout__list-item ember-view")[count]["id"]
            element = driver.find_element_by_id(id_toscroll)
            driver.execute_script("arguments[0].scrollIntoView();", element)
            count += random.randint(1,4)
            time.sleep((0.4 + random.random()) /2)
        except:
            running = False


    # Extracting relevant data
    element_list = soup.find_all("li", class_="jobs-search-results__list-item occludable-update p0 relative scaffold-layout__list-item ember-view")

    for i in element_list:
        id = i.find("div" ,class_="full-width artdeco-entity-lockup__title ember-view")["id"]
        elementID = driver.find_element_by_id(id)
        elementID.click()
        time.sleep(5 + random.random() * 2)
        try:
            soup = get_soup(driver)
            job_title = soup.find('h2', class_='t-24 t-bold').text
            company_name = soup.find('span', class_='jobs-unified-top-card__company-name').text
            no_employees = soup.find_all('li', class_='jobs-unified-top-card__job-insight')[1].text
            job_details = soup.find('div', class_='jobs-box__html-content jobs-description-content__text t-14 t-normal jobs-description-content__text--stretch').text
            salary = soup.find('div', class_="mt4")
            if type(salary) == str:
                salary = salary.text
            rows = [job_title, company_name, no_employees, salary, job_details]
            jobs.append(rows)
        except Exception as e:
            print(e, errors)
            errors += 1
    get_page(page)

# save into file
df = pd.DataFrame(jobs, columns = ["job_title","company_name" ,"number_employees" ,"salary" ,"job_details"])
# df.to_csv("linkedin_dataset.csv", encoding='utf-8-sig')


# # analyzing
# len(jobs)
# df["salary"]
# page

len(soup.find_all("li"))

soup.find_all("li", class_="jobs-search-results__list-item occludable-update p0 relative scaffold-layout__list-item ember-view")