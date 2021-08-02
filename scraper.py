import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from loguru import logger
import sys

logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>", level="DEBUG")
url = "https://www.fia.com/documents/list/"

# If folder doesn't exist, it will be created. You can change this if you want.
folder_location = r'documents/'
if not os.path.exists(folder_location):
    os.mkdir(folder_location)
    logger.info(f"{folder_location} didn't exist until created")

response = requests.get(url)
logger.debug(f"{url} downloaded")
soup= BeautifulSoup(response.text, "html.parser")  

for link in soup.select("a[href$='.pdf']"):
    race = link['href'].split('/')[-1]
    race = race.split('-')[0]
    if not "Grand Prix" in race:
        continue
    year = race.split()[0]
    race_folder = folder_location + year + "/" + race
    year_folder = folder_location + year
    if not os.path.exists(year_folder):
        os.mkdir(year_folder)
        logger.info(f"{year_folder} didn't exist until created")
    if not os.path.exists(race_folder):
        os.mkdir(race_folder)
        logger.info(f"{race_folder} didn't exist until created")
    filename = os.path.join(race_folder,link['href'].split('/')[-1])
    if os.path.isfile(filename):
        logger.info(f"{filename} exists. Ignoring.")
    else:
        with open(filename, 'wb') as f:
            logger.debug(f"Found {filename} - downloading...")
            f.write(requests.get(urljoin(url,link['href'])).content)