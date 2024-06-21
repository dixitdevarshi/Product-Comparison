#CURRENT RESULTS OF THIS FILE ARE ALREADY PRESENT IN THE REPO
#FILE TO BE USED FOR PERIODIC UPDATION

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from typing import List
import time


chromedriver_path = ChromeDriverManager().install() 
service = Service(executable_path=chromedriver_path)

driver = webdriver.Chrome(service=service)


#opens the page
url = "https://www.gsmarena.com/makers.php3"
url_open = urlopen(url)
page = url_open.read()
phone_list_html = bs(page,"html.parser")
# print(phone_list_html)
url_open.close

fullbox = phone_list_html.find("div", {"class": "st-text"})
table = fullbox.find("table")
# print(table)

all_tr = table.find_all("tr")

all_brand_names = []
all_brand_links: List[WebElement] = []
all_model_names = []
data = {}

for tr in all_tr:
    all_td = tr.find_all("td")

    for td in all_td:
        a_tag = td.find("a")
        for span in a_tag.find_all('span'):
            span.decompose()

        full_name = a_tag.text.strip()
        brand_name = full_name.split('\n')[0]
        
        link_tag = td.find("a")["href"]
        brand_link = "https://www.gsmarena.com/" + link_tag
        all_brand_names.append(brand_name)
        all_brand_links.append(brand_link)
        


for i in range(len(all_brand_names)):
    driver.get(all_brand_links[i])
    time.sleep(1)

    model_names = []

    while True:
        try:
            parent_class = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "makers")))
            sub_parent = parent_class.find_element(By.TAG_NAME, "ul")
            models_in_page = sub_parent.find_elements(By.TAG_NAME, "li")
            
            for model in models_in_page:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "strong")))
                strong = model.find_element(By.TAG_NAME, "strong")
                span = strong.find_element(By.TAG_NAME, "span")
                modelName = span.text
                model_names.append(modelName)

            # moving to next page
            try:
                class1 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "review-nav-v2")))
                nav_pages = class1.find_element(By.CLASS_NAME, "nav-pages")
                next_button = nav_pages.find_element(By.CSS_SELECTOR, 'a[title="Next page"]')
                next_button.click()

                # wait for the next page to load
                WebDriverWait(driver, 20).until(EC.staleness_of(parent_class))

            except (NoSuchElementException, TimeoutException):
                all_model_names.append(model_names)
                break
        except NoSuchElementException:
            all_model_names.append(model_names)
            break



# final brand - models pair storage 
if len(all_brand_names) == len(all_model_names):
    for i in range(len(all_brand_names)):
        data[all_brand_names[i]] = all_model_names[i]
else:
    print("unequal sizes of lists!!!")



# returning data as json file
with open("phone_models_list.json", "w") as json_file:
    json.dump(data, json_file, indent=4)


time.sleep(5)

driver.quit() #exits
