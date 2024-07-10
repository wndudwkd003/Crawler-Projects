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

output_path = path_directory_generator(r"./emoji_category")

work_url = ["https://emojipedia.org/nature#list", "https://emojipedia.org/food-drink#list",
            "https://emojipedia.org/activity#list", "https://emojipedia.org/travel-places#list",
            "https://emojipedia.org/objects#list", "https://emojipedia.org/symbols#list",
            "https://emojipedia.org/flags#list"]

emoji_category_dict = dict()

for url in work_url:
    driver.get(url)
    time.sleep(2)

    driver_util.scroll_down(driver, 4)
    time.sleep(2)  # 스크롤 후 로딩을 위한 대기 시간

    div_list = driver.find_elements(By.XPATH, "//div[contains(@class, 'mb-4') and contains(@class, 'scroll-mt-')]")

    for div in div_list:
        try:
            h2 = div.find_element(By.TAG_NAME, "h2")
            title = h2.text
            print("title: ", end="")
            print(title)
            emoji_name_list = div.find_elements(By.TAG_NAME, "a")

            if title not in emoji_category_dict:
                emoji_category_dict[title] = set()

            for name in emoji_name_list:
                name_text = name.find_element(By.TAG_NAME, "span").text
                print(name_text)
                emoji_category_dict[title].add(name_text)


        except Exception as e:
            print(f"Error processing div: {e}")
            continue

# 데이터프레임 생성 및 CSV 저장
for category, emojis in emoji_category_dict.items():
    df = pd.DataFrame(emojis, columns=["Emoji"])
    category_clean = category.replace(" ", "_").replace("/", "_")
    df.to_csv(os.path.join(output_path, f"{category_clean}.csv"), index=False, encoding='utf-8')

driver.quit()
