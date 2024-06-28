import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_soup(url):
    #Fetches the HTML content of a URL with a random user-agent header.
    headers = {'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}  
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error in getting webpage:", response.status_code)
        return None  # Indicate failure to prevent unnecessary parsing

    soup = BeautifulSoup(response.text, "lxml")
    return soup

def get_all_reviews_url(product_url):
    #Extracts the URL for the 'all reviews' page from the product page.
    soup = get_soup(product_url)
    if not soup:
        return None

    review_link_element = soup.find("a", class_="a-link-emphasis a-text-bold")
    if not review_link_element:
        return None

    all_reviews_url = review_link_element["href"]

    # Handle relative vs. absolute URLs
    if all_reviews_url.startswith("/"):
        base_url = f"https://www.amazon.in{all_reviews_url}"
    else:
        base_url = all_reviews_url  # Already an absolute URL

    return base_url

def get_pagination_links(soup, base_url):
    #Extracts links to subsequent review pages from the provided soup.
    pagination_container = soup.find("ul", class_="a-pagination")
    if not pagination_container:
        return []  # No pagination found

    pagination_links = []
    for link in pagination_container.find_all("a", href=True):
        if link.text.strip() == "Next":
            next_page_url = f'{base_url}{link["href"]}'
            pagination_links.append(next_page_url)
    return pagination_links

def get_reviews(url):
    #Scrapes reviews from a single Amazon product review page URL.
    soup = get_soup(url)
    if not soup:
        return []  # Handle failure from get_soup

    review_elements = soup.select("div.review")

    scraped_reviews = []
    for review in review_elements:
        r_content_element = review.select_one("span.review-text")
        r_content = r_content_element.text if r_content_element else None

        #append the review content to the list.
        scraped_reviews.append(r_content.strip())

    return scraped_reviews

def scrape_reviews(product_url, num_pages=10):
    #Scrapes reviews from the 'all reviews' page of the specified product URL and subsequent pages (up to the specified number).
    #Returns a list of reviews, each represented as a string.
    
    all_reviews_url = get_all_reviews_url(product_url)
    if not all_reviews_url:
        print("Error: Could not find the URL for the 'all reviews' page.")
        return []

    all_reviews = []
    for page_num in range(1, num_pages + 1):
        page_url = f'{all_reviews_url}&pageNumber={page_num}'
        reviews = get_reviews(page_url)
        if reviews:
            all_reviews.extend(reviews)

    return all_reviews

def main():
    product_url = "https://www.amazon.in/Apple-iPhone-15-128-GB/dp/B0CHX1W1XY/ref=sr_1_1_sspa?crid=36Q0F978V3KO3&dib=ey"
    iphone12 = "https://www.amazon.in/New-Apple-iPhone-12-128GB/dp/B08L5TNJHG/ref=sr_1_1_sspa?crid=3NXROWPGBR3F7&dib=eyJ2IjoiMSJ9.KgUQv3qF_WTGXfg2bmJvIq4RkpxVWV6RtSW49wmpFx8pTzwddd1UzpesJ4Mv-O8QtB1O3cXk_z6ylV7g0UtiGzKuBYxZPhnUumOvGZYBYyu2GfVBJjaXluPEjJ-lPWYcQkDBUucb48cQzzTQcGvSO8K5mg1cjL7bRKIu82WYXtS58wWl4G9D9o6RQU3UeX_xtmZaThqg6Pj1jpTQUuI2WjvxhQhscXyQoSQoTBdsYGk.MziqLfTdzRKl95S88v4mox0truV-cO8BZuf2vGCheQ8&dib_tag=se&keywords=iphone+12&qid=1719476055&sprefix=%2Caps%2C250&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1"
    nordce_4 = "https://www.amazon.in/gp/product/B0CX58MTNN/ref=s9_bw_cg_Budget_6a1_w?pf_rd_m=AT95IG9ONZD7S&pf_rd_s=merchandised-search-18&pf_rd_r=C5C5HVSGH5E8E57F1Y7Y&pf_rd_t=101&pf_rd_p=ca16962b-f3d9-459e-82c9-a8c5e328e174&pf_rd_i=1389401031"
    galaxy_s24 = "https://www.amazon.in/gp/product/B0CS6H3Y9G/ref=s9_bw_cg_Budget_11c1_w?pf_rd_m=AT95IG9ONZD7S&pf_rd_s=merchandised-search-28&pf_rd_r=C5C5HVSGH5E8E57F1Y7Y&pf_rd_t=101&pf_rd_p=7b31d8f8-2563-4a95-8b9a-7c8c61c9ebf1&pf_rd_i=1389401031&th=1"
    pixel_8 = "https://www.amazon.in/Pixel-Obsidian-8GB-128GB-Storage/dp/B0CVDPL2BH/ref=sr_1_1?crid=3J8S9NB2QNW32&dib=eyJ2IjoiMSJ9.9caxnrELI5ZeTvhDMYjNpVfCSITujb7eBtsVG3XT-W3voIzOWEZ5tllndP5F_73uKvb7sKquyYCDdWiyp_KYpFh-5c1H1ykt2puOr83SrafRtNpA4dsoe7KjK7NQHtEh8qyI2gN4efWP9m2-io309TBp1MTkPqPA-LQTLPvxNTOfkphiDvNlOyQxNQXRWIsXOT1z8ib2qpy4qEpuJ5DaGJ_w5DG9ccGYwnA-zzQduAg.RJnA9cAv9hSvw1ANuEfO52fHX1moUdB5XckSiogeJb4&dib_tag=se&keywords=pixel%2B8&qid=1719478856&sprefix=%2Caps%2C233&sr=8-1&th=1"
    
    # Scrape reviews 
    reviews = scrape_reviews(pixel_8, num_pages=10)

    # Save reviews to a text file
    with open("pixel8_reviews.txt", "w", encoding="utf-8") as f:
        for review in reviews:
            f.write(review + "\n")  # Write each review to a text file

if __name__ == '__main__':
    main()
