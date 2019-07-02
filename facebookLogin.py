from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os       
import json

def login(driver, wait, username, password):
    driver.get("https://facebook.com")
    driver.find_element_by_id("email").send_keys(username)
    driver.find_element_by_id("pass").send_keys(password + "\n")



def search(driver, wait, keyword):
    keyword = "%20".join(keyword.split())
    url = "https://www.facebook.com/search/people/?q=" + keyword + "&epa=SERP_TAB"
    driver.get(url)



def scrapeGeneral(driver, wait):

    fp = open('fb_test_generals.json', encoding="utf8")
    results = json.load(fp)

    results["old_results"].update(results["new_results"])

    old_results = results["old_results"]
    new_results = {}

    if(len(old_results) == 0):
        main = driver.find_element_by_id("initial_browse_result")    
        lis = main.find_elements_by_class_name("_4p2o")

        for i, li in enumerate(lis):
            print("{0}/{1}".format(i+1, len(lis)))
            link = li.find_element_by_tag_name("a").get_attribute("href")
            text = li.text.split("\n")
            new_results[link] = {}
            new_results[link]["name"] = text[0]
            new_results[link]["info"] = "" 
            for t in text[1:]:
                if t.strip().lower() == "add friend" or t.strip().lower() == "more options":
                    continue
                new_results[link]["info"] += t + "\n"
            with open("fb_test_generals.json", "w") as f:
                json.dump({ "old_results": old_results, "new_results": new_results, "progress": "{0}/{1}".format(i + 1, len(lis)) }, f)

    
    else:
        oldies_len = len(old_results)
        main = driver.find_element_by_id("initial_browse_result")    
        lis = main.find_elements_by_class_name("_4p2o")
        while len(lis) <= oldies_len + 10:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")  
            main = driver.find_element_by_id("initial_browse_result")    
            lis = main.find_elements_by_class_name("_4p2o")
            # print(len(lis), oldies_len)
        lis = lis[oldies_len:]
        for i, li in enumerate(lis):
            print("{0}/{1}".format(i+1, len(lis)))
            link = li.find_element_by_tag_name("a").get_attribute("href")
            text = li.text.split("\n")
            new_results[link] = {}
            new_results[link]["name"] = text[0]
            new_results[link]["info"] = "" 
            for t in text[1:]:
                if t.strip().lower() == "add friend" or t.strip().lower() == "more options":
                    continue
                new_results[link]["info"] += t + "\n"
            with open("fb_test_generals.json", "w") as f:
                json.dump({ "old_results": old_results, "new_results": new_results, "progress": "{0}/{1}".format(i + 1, len(lis)) }, f)


def scrapeProfile(driver, wait, link):
    
    temp = {}
    
    if "&ref=" in link:
        link = link[:link.index("&ref=")]
    if "?ref=" in link:
        link = link[:link.index("?ref=")]
    if "profile.php" in link:
        link = link + "&sk=about&section="
    else:
        link += "/about?section="
    
    # education
    driver.get(link + "education")
    uls = driver.find_elements_by_class_name("fbProfileEditExperiences")
    heads = driver.find_elements_by_xpath("//span[@role='heading']")
    heads = heads[7:]
    
    for i,ul in enumerate(uls):
        temp[heads[i].text.lower()] = []
        lis = ul.find_elements_by_class_name("fbEditProfileViewExperience")
        for li in lis:
            hmm = {}
            org = li.find_elements_by_tag_name("a")[-1]
            hmm["organisation"] = org.text
            hmm["organistaion_link"] = org.get_attribute("href")
            hmm["details"] = "\n".join(li.text.split("\n")[1:])
            temp[heads[i].text.lower()].append(hmm)
    
    #living
    driver.get(link + "living")

    temp["places"] = {}
    try:
        temp["places"]["current_city"] = driver.find_element_by_id("current_city").find_element_by_tag_name("a").text
    except:
        temp["places"]["current_city"] = ""
    try:
        temp["places"]["hometown"] = driver.find_element_by_id("hometown").find_element_by_tag_name("a").text
    except:
        temp["places"]["hometown"] = ""

    uls = driver.find_elements_by_class_name("fbProfileEditExperiences")

    if len(uls) > 1:
        for i,ul in enumerate(uls[1:]):
            temp["places"]["other_places"] = []
            lis = ul.find_elements_by_class_name("fbEditProfileViewExperience")
            for li in lis:
                temp["places"]["other_places"].append(li.find_element_by_tag_name("a").text)

    #contact-info
    driver.get(link + "contact-info")

    uls = driver.find_elements_by_class_name("fbProfileEditExperiences")
    heads = driver.find_elements_by_xpath("//span[@role='heading']")
    heads = heads[7:]
    
    for i,ul in enumerate(uls):
        try:
            curr = "_".join(heads[i].text.lower().split())
            temp[curr] = {}
            lis = ul.find_elements_by_tag_name("li")
            for li in lis:
                if "No contact info to show" in li.text:
                    continue
                temp[curr][li.text.split("\n")[0]] = li.text.split("\n")[1]
        except:
            continue
                    
    return temp



# ch = os.getcwd() + '/tools/chromedriver.exe'

# options = Options()
# options.add_argument("--headless")
# options.add_argument("log-level=3")
# options.add_argument("--incognito")
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# driver = webdriver.Chrome(options=options, executable_path=ch)
# wait = WebDriverWait(driver, 10)
# driver.implicitly_wait(0.5)

# fp = open('test.json', encoding="utf8")
# results = json.load(fp)
# results["progress"] = "init"
# with open("test.json", "w") as f:
#     json.dump(results, f)

# print("logging in")
# login(driver, wait, "sanzermartin1@gmail.com", "anzcallahan")
# print("logged in going for first profile")
# search(driver, wait, "business man berlin")
# scrapeGeneral(driver, wait)

# fp = open('test.json', encoding="utf8")
# test = json.load(fp)["old_results"]
# data = {}
# for i,link in enumerate(test.keys()):
#     print("scraping profile {0} of {1}".format(i,len(test.keys())))
#     data[link] = scrapeProfile(driver,wait, link)
# with open("profies.json", "w", encoding="utf8") as f:
#     json.dump(data, f, ensure_ascii=False)
