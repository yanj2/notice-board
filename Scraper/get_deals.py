from selenium.webdriver import Chrome
from selenium.common.exceptions import SessionNotCreatedException
import json
import os
import plistlib
from dotenv import load_dotenv
import requests 
from zipfile import ZipFile
import io
# import logging 

load_dotenv()

#Note that getcwd gets the current working dir where python is run from 
# SITES_PATH = os.getcwd() + "sites.json"
CURR_DIR = os.path.dirname(os.path.realpath(__file__))
SITES_PATH = CURR_DIR + "/sites.json"
DRIVER_PATH = CURR_DIR + "/chromedriver"

# logger = logging.logger("NoticeBot")

# print(os.path.exists(os.getenv("PATH_TO_CHROME_APP")))
# Get the current installed Chrome ver by reading the property list file
pl = plistlib.readPlist(os.getenv("P_LIST_LOC"))
ver = pl["CFBundleShortVersionString"]
print(f"Current Version of Chrome: {ver}")

with open(SITES_PATH) as f:
    sites = json.load(f)

# Try to run the chrome driver, installing any updates if necessary
try:
    driver = Chrome(DRIVER_PATH)
except SessionNotCreatedException as e:
    print(e)
    print("Unable to initialise chromedriver")
finally:
   
    # Check for updates 
    print("Checking for new version of chromedriver")
    page = requests.get(f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{ver.split('.')[0]}")
    new_driver_version = page.text

    if "NoSuchkey" in new_driver_version:
        print("Newer version of chromedriver has not been made yet")

    elif new_driver_version == os.getenv("DRIVER_VER"):
        print("Driver already up to date")

    else:
        # Found a new version to download
        print(f"Newer version of chromedriver exists: {new_driver_version}")
        print(f"Attempting to update to newer version of chromedriver")

        # Download and unzip new version of chromedriver
        driver_url = f"https://chromedriver.storage.googleapis.com/{new_driver_version}/chromedriver_mac64.zip"
        driver_download_page = requests.get(driver_url)
        zip_file = ZipFile(io.BytesIO(driver_download_page.content))
        zip_file.extract("chromedriver", CURR_DIR)
