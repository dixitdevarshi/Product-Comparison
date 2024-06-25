import requests
from bs4 import BeautifulSoup as bs
import json
import re
from fake_useragent import UserAgent

def getSpecs(url):
    ua = UserAgent()
    #headers = {'User-Agent': ua.random}

    response = requests.get(url, headers={'User-Agent': ua.random})

    if response.status_code == 200: #check for succesful loading of page
        soup = bs(response.content, "html.parser")

        # Extract the phone name
        phone_name_tag = soup.find("h1", {"class": "specs-phone-name-title"})
        if not phone_name_tag:
            raise Exception("Phone name not found on the page")
        phone_name = phone_name_tag.text
        phone_name_clean = re.sub(r'\W+', '_', phone_name)  # Clean the phone name to be a valid filename

        specs_box = soup.find("div", {"id": "specs-list"}) #Full specifications box
        if not specs_box:
            raise Exception("Specs list not found on the page")
        
        specs = {}
        # adding specs data to file 
        for table in specs_box.find_all("table", {"cellspacing": 0}):
            category = table.find('th').text
            specs[category] = {}

            for row in table.find_all('tr'):
                spec_name_tag = row.find('td', {'class': 'ttl'})
                spec_value_tag = row.find('td', {'class': 'nfo'})

                if spec_name_tag and spec_value_tag:
                    spec_name = spec_name_tag.get_text(strip=True)
                    spec_value = spec_value_tag.get_text(strip=True)
                    specs[category][spec_name] = spec_value

        file_name = f"{phone_name_clean}.json"
        with open(file_name, "w") as f: # saving the phone specs in json file
            json.dump(specs, f, indent=4)

    elif response.status_code == 429: #raising too many requests error
        raise Exception("Rate limit exceeded. Too many requests.")
    
    else: # for all the other exceptions
        raise Exception(f"Failed to fetch page, status code: {response.status_code}")
# for checking
try:
    getSpecs("https://www.gsmarena.com/oneplus_12-12725.php")
except Exception as e:
    print(f"Error occurred: {str(e)}")