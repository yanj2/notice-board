from selenium.webdriver import Chrome
from selenium.common.exceptions import SessionNotCreatedException
from dotenv import load_dotenv, set_key
import plistlib
import requests 
from zipfile import ZipFile
import io
import os

CURR_DIR = os.path.dirname(os.path.realpath(__file__))
DRIVER_PATH = CURR_DIR + "/chromedriver"
CHROME_DRIVER_API = "https://chromedriver.storage.googleapis.com/"
OS_VER = "mac64"

load_dotenv()

def update_driver(driver_dir):
    # Get the current installed Chrome ver by reading the property list file
    pl = plistlib.readPlist(os.getenv("P_LIST_LOC"))
    ver = pl["CFBundleShortVersionString"]
    print(f"Current Version of Chrome: {ver}")

    # Check if new version of driver is available 
    print("Checking for new version of chromedriver")
    page = requests.get(f"{CHROME_DRIVER_API}LATEST_RELEASE_{ver.split('.')[0]}")
    new_driver_version = page.text

    if "NoSuchkey" in new_driver_version:
        print("Newer version of chromedriver has not been made yet")

    elif new_driver_version == os.getenv("DRIVER_VER"):
        print("Driver already up to date")

    else:
        download_driver(new_driver_version, driver_dir)

def download_driver(new_version, driver_dir):
    # Found a new version to download
    print(f"Newer version of chromedriver exists: {new_version}")
    print(f"Attempting to update to newer version of chromedriver")

    # Download and unzip new version of chromedriver
    driver_url = f"{CHROME_DRIVER_API}{new_version}/chromedriver_{OS_VER}.zip"
    zip_file = ZipFile(io.BytesIO(requests.get(driver_url)))
    zip_file.extract("chromedriver", driver_dir)

    # Update the env variables 
    set_key(f"{os.getenv('ROOT')}/.env", "DRIVER_VER", new_version)
    print(f"Updated to version:{new_version}")

def get_driver(driver_path=DRIVER_PATH, driver_dir=CURR_DIR):

    # Try to run the chrome driver, installing any updates if necessary
    try:
        driver = Chrome(driver_path)
    except SessionNotCreatedException as e:
        print(e)
        print("Unable to initialise chromedriver")
        update_driver(driver_dir)
        driver = Chrome(driver_path)
        
    return driver


    