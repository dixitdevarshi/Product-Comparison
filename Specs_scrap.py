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
    
    PhoneLinks = search_results.find_elements(By.TAG_NAME, "a")

    strong: List[WebElement] = []
    for s in PhoneLinks:
        temp = find_element_with_retries(s, By.TAG_NAME, "strong")
        strong.append(temp)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "span")))

    for st in strong:
        try:
            LastTag = find_element_with_retries(st, By.TAG_NAME, "span")
            if LastTag.text.replace(" ", "").replace("\n", "").casefold() == phone.replace(" ", "").casefold():
                for s in PhoneLinks:
                    try:
                        if st in s.find_elements(By.TAG_NAME, "strong"):
                            s.click()
                            break
                    except StaleElementReferenceException:
                        print("Stale element encountered while clicking, retrying...")
                        PhoneLinks = search_results.find_elements(By.TAG_NAME, "a")
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

def specs_scrap(driver):
    
    fullbox = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "specs-list")))
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
    tables = fullbox.find_elements(By.TAG_NAME, "table")

    data = {}

    for table in tables:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "tr")))
        MainKey = find_element_with_retries(table, By.TAG_NAME, "th").text
        data[MainKey] = {}

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ttl")))

        for InsideTags in table.find_elements(By.TAG_NAME, "tr"):
            try:
                ttl = find_element_with_retries(InsideTags, By.CLASS_NAME, "ttl")
                title = ttl.text
                nfo = find_element_with_retries(InsideTags, By.CLASS_NAME, "nfo")
                value = nfo.text
                data[MainKey][title] = value
            except NoSuchElementException:
                print("No ttl or nfo element found, skipping...")
            except StaleElementReferenceException:
                print("Stale element encountered while processing, skipping...")
    return data

specs_scrap(driver)    
time.sleep(10)

driver.quit() #exits
