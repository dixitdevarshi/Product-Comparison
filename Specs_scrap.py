from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from typing import List
import time

def find_element_with_retries(context, by, value, retries=10, wait_time=1):
    attempt = 0
    while attempt < retries:
        try:
            return context.find_element(by, value)
        except StaleElementReferenceException:
            print(f"Retry {attempt + 1}/{retries} for element {value}")
            time.sleep(wait_time)
            attempt += 1
    raise TimeoutException(f"Element not found after {retries} retries")

chromedriver_path = ChromeDriverManager().install() #install driver
service = Service(executable_path=chromedriver_path)

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=service, options=options)

url = "https://www.gsmarena.com/"
phone = 'iphone 13'

try:
    driver.get(url) # Open the website

    # search for the phone
    search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "sSearch"))
        )
    
    search_box.send_keys(phone)
    search_box.send_keys(Keys.RETURN)

    search_results = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "makers"))
        )
    
    all_phone_links = search_results.find_elements(By.TAG_NAME, "a")

    strong: List[WebElement] = []
    for s in all_phone_links:
        temp = find_element_with_retries(s, By.TAG_NAME, "strong")
        strong.append(temp)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "span")))

    for st in strong:
        try:
            span = find_element_with_retries(st, By.TAG_NAME, "span")
            if span.text.replace(" ", "").replace("\n", "").casefold() == phone.replace(" ", "").casefold():
                #print(f"Matching span text: {span.text}")
                
                for s in all_phone_links:
                    try:
                        if st in s.find_elements(By.TAG_NAME, "strong"):
                            s.click()
                            break
                    except StaleElementReferenceException:
                        print("Stale element encountered while clicking, retrying...")
                        all_phone_links = search_results.find_elements(By.TAG_NAME, "a")
                        break
        except TimeoutException:
            try:
                print(f"Span element not found in retries for {st.text}")
            except StaleElementReferenceException:
                print("Stale element encountered while logging, skipping...")
    
    # # Click the first search result
    # first_result = search_results.find_element(By.TAG_NAME, "a")
    # first_result.click()
    # time.sleep(10)
except:
    pass

def data_fetching(driver):
    all_info = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "specs-list")))

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "table")))

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))

    all_tables = all_info.find_elements(By.TAG_NAME, "table")

    data = {}

    for table in all_tables:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "tr")))
        first_key = find_element_with_retries(table, By.TAG_NAME, "th").text
        data[first_key] = {}

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ttl")))

        for inner_info in table.find_elements(By.TAG_NAME, "tr"):
            try:
                title_key = find_element_with_retries(inner_info, By.CLASS_NAME, "ttl")
                title = title_key.text
                value_key = find_element_with_retries(inner_info, By.CLASS_NAME, "nfo")
                value = value_key.text
                data[first_key][title] = value
            except NoSuchElementException:
                print("No ttl or nfo element found, skipping...")
            except StaleElementReferenceException:
                print("Stale element encountered while processing, skipping...")

    return data

data_fetching(driver)    
time.sleep(10)

driver.quit() #exits
