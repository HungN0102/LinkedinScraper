import time
import configparser
from selenium import webdriver
from bs4 import BeautifulSoup
from numpy import random

# Retrieving account name and passwords
parser = configparser.ConfigParser()
parser.read("Webscraping/LinkedinAccount.conf")
account_name = parser.get("account1","account")
password = parser.get("account1","pass")

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
driver.get("https://www.linkedin.com/jobs/search/?geoId=90009496&keywords=%22data%20engineer%22&location=London%20Area%2C%20United%20Kingdom")
time.sleep(random.random()+1)

# Retrieving html script first time
driver.maximize_window()
src = driver.page_source
soup = BeautifulSoup(src, 'html.parser')
id = soup.find_all("li",class_="jobs-search-results__list-item occludable-update p0 relative ember-view")[1]["id"]
time.sleep(random.random()+1)

# Scroll to the bottom of the page
running = True
count = 0
while running:
    src = driver.page_source
    soup = BeautifulSoup(src, 'html.parser')
    try:
        id_toscroll = soup.find_all("li", class_="jobs-search-results__list-item occludable-update p0 relative ember-view")[count]["id"]
        element = driver.find_element_by_id(id_toscroll)
        driver.execute_script("arguments[0].scrollIntoView();", element)
        count += random.randint(1,4)
        time.sleep(random.random()/5)
    except:
        running = False
# len(soup.find_all("li", class_="jobs-search-results__list-item occludable-update p0 relative ember-view"))
# Getting all id
element_list = soup.find_all("li",class_="jobs-search-results__list-item occludable-update p0 relative ember-view")
jobs = []

for i in element_list:
    id = i["id"]
    print(id)
    elementID = driver.find_element_by_id(id)
    elementID.click()
    time.sleep(5+random.random()*2)

    src = driver.page_source
    soup = BeautifulSoup(src, 'html.parser')
    job_title = soup.find('h2', class_='t-24 t-bold').text
    no_employees = soup.find_all('li', class_='jobs-unified-top-card__job-insight')[1].text
    job_details = soup.find('div', class_='jobs-box__html-content jobs-description-content__text t-14 t-normal jobs-description-content__text--stretch').text

    rows = (job_title,no_employees,job_details)
    jobs.append(rows)
# id = element_list[1]["id"]
# elementID = driver.find_element_by_id(id)
# elementID.click()
count

