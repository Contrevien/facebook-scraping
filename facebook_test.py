from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver
import os
import getpass
from facebookLogin import login, search, scrapeGeneral, scrapeProfile
import json

ch = os.getcwd() + '/tools/chromedriver.exe'

options = Options()
options.add_argument("--headless")
options.add_argument("log-level=3")
options.add_argument("--incognito")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options, executable_path=ch)
wait = WebDriverWait(driver, 10)
driver.implicitly_wait(0.5)

fp = open('fb_test_generals.json', encoding="utf8")
results = json.load(fp)

results["old_results"] = {}
results["new_results"] = {}
results["progress"] = ""

results["old_results"].update(results["new_results"])
with open('fb_test_generals.json', 'w') as f:
    json.dump(results, f)


time.sleep(1)
print("Welcome to facebook test")
time.sleep(1)
username = input("Please enter your facebook username: ")
password = getpass.getpass()
print("trying to log in...")
login(driver, wait, username, password)

if "/login/" in driver.current_url:
    print("wrong username/pass exiting")
    exit()

print("logged in")
time.sleep(1)
keyword = input("Enter keyword: ")
print("searching for keyword...")

search(driver, wait, keyword)

print("Initializing scraper..")

done = False
while not done:
    scrapeGeneral(driver, wait)
    if input("Do you want to scrape more results? (y/n): ") not in ["y", "Y"]:
        done = True

fp = open('fb_test_generals.json', encoding="utf8")
results = json.load(fp)

results["old_results"].update(results["new_results"])
with open('fb_test_generals.json', 'w') as f:
    json.dump(results, f)

print("Dumped the results in fp_test_generals.json")
time.sleep(1)

print("Demonstrating full profile scraping using these proflies")
time.sleep(1)

fp = open('fb_test_generals.json', encoding="utf8")
test = json.load(fp)["old_results"]
data = {}
for i,link in enumerate(test.keys()):
    print("{0}/{1}".format(i,len(test.keys())))
    data[link] = scrapeProfile(driver, wait, link)
with open("fb_test_complete.json", "w", encoding="utf8") as f:
    json.dump(data, f, ensure_ascii=False)

print("Dumped the results in fp_test_complete.json")
