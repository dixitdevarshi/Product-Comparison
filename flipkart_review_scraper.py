from bs4 import BeautifulSoup as bs
import requests
from fake_useragent import UserAgent

ua = UserAgent()
agent = ua.random

custom_headers = {
    "user-agent" : agent, 
    "Accept-Language" : "en-US,en;q=0.9"
}

product_url = "https://www.flipkart.com/apple-iphone-15-blue-128-gb/p/itmbf14ef54f645d?pid=MOBGTAGPAQNVFZZY&lid=LSTMOBGTAGPAQNVFZZYO7HQ2L&marketplace=FLIPKART&q=iphone+15&store=tyy%2F4io&spotlightTagId=BestsellerId_tyy%2F4io&srno=s_1_1&otracker=AS_Query_HistoryAutoSuggest_1_1_na_na_na&otracker1=AS_Query_HistoryAutoSuggest_1_1_na_na_na&fm=search-autosuggest&iid=7be0c255-4126-4347-ab60-47f82736b1dc.MOBGTAGPAQNVFZZY.SEARCH&ppt=sp&ppn=sp&ssid=700fa3djwg0000001719471055670&qH=2f54b45b321e3ae5"
#product_url = "https://www.flipkart.com/apple-iphone-12-blue-128-gb/p/itm02853ae92e90a?pid=MOBFWBYZKPTZF9VG&lid=LSTMOBFWBYZKPTZF9VGHUA0UC&marketplace=FLIPKART&q=iphone+12&store=tyy%2F4io&srno=s_1_3&otracker=search&otracker1=search&fm=search-autosuggest&iid=ef95a48c-98d2-4866-9105-c2346968e66f.MOBFWBYZKPTZF9VG.SEARCH&ppt=browse&ppn=browse&ssid=vkvdzgrbk00000001719497264323&qH=7b7504afcaf2e1ea"
#product_url = "https://www.flipkart.com/oneplus-8-pro-onyx-black-128-gb/p/itm88bfc88328fcc?pid=MOBFU897GY96PPXR&lid=LSTMOBFU897GY96PPXR3TJDQO&marketplace=FLIPKART&q=oneplus+8+pro&store=tyy%2F4io&srno=s_1_9&otracker=AS_Query_OrganicAutoSuggest_3_9_na_na_na&otracker1=AS_Query_OrganicAutoSuggest_3_9_na_na_na&iid=e41cf0f4-335d-4571-8c8b-f0d9488020d1.MOBFU897GY96PPXR.SEARCH&ssid=3hzp9biaf40000001719478517176&qH=ea0a91036285d079"

product_page = requests.get(product_url,headers=custom_headers)
product_page_html = bs(product_page.text, "html.parser")
#print(product_page_html)

# getting the name of the phone
name_parent = product_page_html.find("div", {"class" : "DOjaWF gdgoEp col-8-12"})
full_phone_name = name_parent.find("span", {"class" : "VU-ZEz"}).text
final_phone_name = ""
parts = full_phone_name.split()
for i, part in enumerate(parts):
    if part in ['3G', '4G', '5G', '6G'] or '(' in part:
        p_name = ' '.join(parts[:i])
        final_phone_name = p_name
        break

all_reviews_parent_class = product_page_html.find("div", {"class" : "col pPAw9M"})
if all_reviews_parent_class:
    all_reviews_tag = all_reviews_parent_class.find_all("a")

    all_reviews_link = ""
    if all_reviews_tag:
        for tag in all_reviews_tag:
            verify_class = tag.find("div", {"class" : "_23J90q RcXBOT"})
            if verify_class:
                button = "https://www.flipkart.com" + tag['href']
                all_reviews_link = all_reviews_link + button

page_1 = requests.get(all_reviews_link, headers=custom_headers)
page_1_html = bs(page_1.text, "html.parser")
#print(page_1_html)

all_urls = []
all_reviews = []

all_boxes = page_1_html.find_all("div", {"class" : "cPHDOP col-12-12"})

parent_div_found = False

# getting the links of all review pages
for box in all_boxes:
    parent_div = box.find("div", {"class": "_1G0WLw mpIySA"})
    if parent_div:
        parent_div_found = True
        nav_div = parent_div.find("nav", {"class" : "WSL9JP"})
        nav_pages = nav_div.find_all("a",{"class": "cn++Ap"})
        for a in nav_pages:
            link_tag = a['href']
            link = "https://www.flipkart.com" + link_tag
            all_urls.append(link)
    else:
        continue
        
# if only 1 review page is present 
if not parent_div_found:
    all_urls.append(all_reviews_link)
    
# fetching reviews
for url in all_urls:
    page = requests.get(url, headers=custom_headers)
    page_html = bs(page.text, "html.parser")
    all_boxes = page_html.find_all("div", {"class" : "cPHDOP col-12-12"})
    
    for box in all_boxes:
        inner_tag = box.find("div", {"class" : "ZmyHeo"})

        # Check if inner_tag is not None
        if inner_tag:  
            review_div = inner_tag.find("div")

            # Check if review_div is not None
            if review_div:  
                for span in review_div.find("span"):
                    span.decompose()
                review_in_list = review_div.text.strip().split('\n')
                review = "\n".join(review_in_list) #to convert it into a string from list elements
                all_reviews.append(review)               
            else:
                continue
        else:
            continue

#Save reviews to a text file with each review in new line
with open(f"{final_phone_name.replace(" ","_")}_reviews.txt", "w", encoding='utf-8') as file:
    for review in all_reviews:
        file.write(f"{review}\n\n")  



