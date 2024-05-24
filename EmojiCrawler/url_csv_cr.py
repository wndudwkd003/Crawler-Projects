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

output_path = path_directory_generator(r"./output")

BASE_URL = r"https://emojipedia.org"
QUERY = "twitter/twemoji-15.0.1"
search_url = rf"{BASE_URL}/{QUERY}"

driver.get(search_url)
time.sleep(5)

urls = set()
while True:
    try:
        div = driver.find_elements(By.CSS_SELECTOR,
                                   "#__next > div > main > div.Container_container-wrapper__u0gtd > div > section > div > div:nth-child(5) > div.w-full.relative > div > div")
        for child in div:
            # child 안에 h2 태그가 있으면 건너뛰기
            if child.find_elements(By.TAG_NAME, 'h2'):
                continue

            # a 태그만 처리
            a_tags = child.find_elements(By.TAG_NAME, "a")
            for a in a_tags:
                urls.add(a.get_attribute("href"))
                print(a.get_attribute("href"))

        # 스크롤을 한 칸 내리기
        driver_util.scroll_down(driver, 4)
        time.sleep(2)  # 스크롤 후 로딩을 위한 대기 시간

        if len(div) == 0:
            break
    except:
        break

# 드라이버 종료
driver.quit()

# URL을 CSV 파일로 저장
urls_list = list(urls)
df = pd.DataFrame(urls_list, columns=["URL"])
csv_output_path = os.path.join(output_path, "urls.csv")
df.to_csv(csv_output_path, index=False)

print(f"URLs have been saved to {csv_output_path}")