import requests
import time
import os
import traceback
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.config import chrome_path, driver_path

import utils.driver_util as driver_util

from utils.path_util import path_directory_generator

######################################################################

driver = driver_util.generate_driver()

url = rf"https://finance.naver.com/sise/sise_quant.naver"

emoji_category_dict = dict()

driver.get(url)
time.sleep(2)

kkkk = driver.find_element(By.CSS_SELECTOR,
                           "#contentarea > div.box_type_l > table > tbody > tr:nth-child(3) > td:nth-child(2) > a").text

print(kkkk)


