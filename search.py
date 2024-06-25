from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.keys import Keys
from typing import List
import time

#chromedriver_path = ChromeDriverManager().install() #install driver
service = Service(executable_path="chromedriver.exe")

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=service, options=options)

def find_element_with_retries(context, by, value, retries=10, wait_time=1):
    attempt = 0
    while attempt < retries:
        try:
            return context.find_element(by, value)
        except StaleElementReferenceException:
            time.sleep(wait_time)
            attempt += 1
    raise TimeoutException(f"Element not found after {retries} retries")

phone_url = ""

def seach_phone(phone_name):
    url = "https://www.gsmarena.com/"

    try:
        driver.get(url) # Open the website

        # search for the phone_name
        search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "sSearch"))
            )
        
        search_box.send_keys(phone_name)
        search_box.send_keys(Keys.RETURN)

        search_results = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "makers"))
            )
        
        # check all result links
        PhoneLinks = search_results.find_elements(By.TAG_NAME, "a")

        strong: List[WebElement] = []
        for s in PhoneLinks:
            temp = find_element_with_retries(s, By.TAG_NAME, "strong")
            strong.append(temp)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "span")))
        
        # match the text of the links with phone_name
        for st in strong:
            try:
                LastTag = find_element_with_retries(st, By.TAG_NAME, "span")
                if LastTag.text.replace(" ", "").replace("\n", "").casefold() == phone_name.replace(" ", "").casefold():
                    for s in PhoneLinks:
                        try:
                            if st in s.find_elements(By.TAG_NAME, "strong"):
                                phone_url = s.get_attribute("href")
                                break
                        except StaleElementReferenceException:
                            PhoneLinks = search_results.find_elements(By.TAG_NAME, "a")
                            break
            except TimeoutException:
                pass
    
    except:
        pass

    finally:
        driver.quit() #exit
        return phone_url
    

seach_phone("apple iphone 14")