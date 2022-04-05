import time
from selenium import webdriver
import configparser

# Retrieving account name and passwords
parser = configparser.ConfigParser()
parser.read("ForFun/WebScraping/LinkedinAccount.conf")
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

time.sleep(1)
# Optional: Skip Verification
elementClass = driver.find_element_by_class_name("secondary-action-new")
elementClass.click()

