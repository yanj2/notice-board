import json
import os
import requests 
from driver import get_driver
import pandas as pd

# current directory that this python file is in
CURR_DIR = os.path.dirname(os.path.realpath(__file__))
SITES_PATH = CURR_DIR + "/sites.json"
ignore = ["OUT OF STOCK", "EXPIRED", "CLOSED"]

with open(SITES_PATH) as f:
    sites = json.load(f)

chrome = get_driver(f"{CURR_DIR}/chromedriver", CURR_DIR)
chrome.get("https://www.ozbargain.com.au")

deals = chrome.find_elements_by_class_name("node-ozbdeal")

scraped = []
for deal in deals:
    title = deal.find_elements_by_class_name("title")[0].text

    if True in map(lambda x: x in title, ignore):
        continue
    
    #TODO: Expand the description by going to the actual link and scraping the description from link 
    descr = deal.find_elements_by_class_name("content")[0].find_elements_by_tag_name("p")[0].text
    # link = deal.find_elements_by_class_name("submitted")[0].find_elements_by_class_name("via")[0]
    print(title, descr)
    print("\n\n\n")
    scraped.append((title, descr))

df = pd.DataFrame(scraped, columns=["title", "descr"])
df.to_csv(f"{os.getenv('ROOT')}/history/seen.csv")


# Makes the driver scroll to bottom of the page. 
# chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")
chrome.quit()



