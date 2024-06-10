from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from typing import List
import time

chromedriver_path = ChromeDriverManager().install()
service = Service(executable_path=chromedriver_path)

# service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

url = "https://www.gsmarena.com/"
element = "apple iphone 14"

driver.get(url)

WebDriverWait(driver,10).until(
    EC.presence_of_element_located((By.ID,"topsearch-text"))
)

inputSearch = driver.find_element(By.ID,"topsearch-text")
inputSearch.send_keys(element + Keys.ENTER)

all_phones = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "makers"))
)

all_phone_links = all_phones.find_elements(By.TAG_NAME, "a")

strong: List[WebElement] = []
for s in all_phone_links:
    temp = s.find_element(By.TAG_NAME, "strong")
    strong.append(temp)

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, "span"))
)

for st in strong:
    span = st.find_element(By.TAG_NAME, "span")
    if span.text.replace(" ", "").replace("\n","").casefold() == element.replace(" ", "").casefold():
        for s in all_phone_links:
            if st in s.find_elements(By.TAG_NAME, "strong"):
                s.click()
                break

time.sleep(10)

driver.quit()