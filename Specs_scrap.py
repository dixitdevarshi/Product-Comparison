from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

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
    
    # Click the first search result
    first_result = search_results.find_element(By.TAG_NAME, "a")
    first_result.click()
    time.sleep(10)
except:
    pass

finally:
    driver.quit() # exits 
