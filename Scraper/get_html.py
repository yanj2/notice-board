import requests 
from urllib3.connection import socket
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError

# Static websites will give html. Dynamic ones probbaly javascript to look at

URL = "https://www.ozbargain.com.au"

def get_page(url):
    
    try:
        page = requests.get(url)
    except (OSError, socket.gaierror):
        return f"Failed to make a connection to {url}. Make sure the URL is valid"

    return page if page.status_code == requests.codes.ok else f"Unsuccessful HTTP request for {url} with error code: {page.status_code}"

print(get_page(URL).text)