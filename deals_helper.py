from driver import get_driver
import json 
import csv 
import page
from datetime import datetime 
from selenium.common.exceptions import InvalidArgumentException
SITES_PATH = "sites.json"
with open(SITES_PATH) as f:
    websites = json.load(f)
    # print(websites, id(websites))

IGNORE = {"OUT OF STOCK", "EXPIRED", "CLOSED"}
FN_CALL = "fn_call"

class Deal():

    def __init__(self, title, desc, url, expiry):
        self.title = title
        self.desc = desc
        self.url = url
        self.img_src = ""
        self.valid_from = datetime.now()
        self.valid_to = expiry 

def retrieve(keyword):

    with open("history/seen.csv") as fp:
        reader = csv.reader(fp)
        output = [row for row in reader if keyword in row[0]]

    return output

def search(keyword):
    browser = get_driver()

    for site in websites:
        site_dict = websites[site]
        search_url = site_dict["dir_str"]["search"]["content"].replace("~", site_dict["site_url"]).replace("query", keyword)
        # print(search_url)
        try:
            browser.get(search_url)
        except InvalidArgumentException:
            print(f"{search_url} is invalid. Please double check the site records")
            return 0, "Unable to complete search request. Argument was invalid"

        # ozbargain search results -> className: search-results, deal itself is the same 
        search_results = browser.find_element_by_class_name("search-results")
        deals = search_results.find_elements_by_class_name("title")

        links = set()
        for deal in deals:

            #TODO: Still need to skip over related-store content.
            if True in map(lambda x: x in deal.text, IGNORE):
                    continue
            a_tag = deal.find_element_by_tag_name("a")
            link = a_tag.get_attribute("href")
            # text = a_tag.text
            if "/node/" in link:

                #TODO: Currently repeated links are showing up because some links don't carry text with it. Need to test for 
                # the link unique-ness
                links.add(link)

        # links = [a.get_attribute("href") for deal in deals for a in deal.find_elements_by_tag_name("a")]
        browser.close()
    return 1, links 

def call_fn(query, keyword):
    return fn_mapping[query][FN_CALL](keyword)

def str_valid_queries():
    return str(list(fn_mapping.keys()))

def valid_query(query):
    return query in fn_mapping 

fn_mapping = {"search": {FN_CALL: search, "num_args": 1}, "retrieve": {FN_CALL: retrieve, "num_args": 1}}