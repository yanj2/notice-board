import requests 
from urllib3.connection import socket
from bs4 import BeautifulSoup

# Static websites will give html. Dynamic ones probbaly javascript to look at

URL = "https://www.ozbargain.com.au"

def get_page(url):
    
    try:
        page = requests.get(url)
    except (OSError, socket.gaierror):
        return f"Failed to make a connection to {url}. Make sure the URL is valid"

    return page if page.status_code == requests.codes.ok else f"Unsuccessful HTTP request for {url} with error code: {page.status_code}"

page = get_page(URL)
soup = BeautifulSoup(page, 'html-parser')


# Boot up the driver 
# open the link to the deals page
# search page for deals 
# if nothing relevant -> open search for predefined or specific tags/words 