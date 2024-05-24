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

# 드라이버 생성
driver = driver_util.generate_driver()

# 출력 폴더 경로 생성
output_path = path_directory_generator(r"./output/result")

# CSV 파일 경로
csv_input_path = r"./output/urls.csv"

# CSV 파일 읽기
try:
    urls_df = pd.read_csv(csv_input_path)
except FileNotFoundError:
    print(f"CSV file not found at {csv_input_path}")
    driver.quit()
    exit(1)

# URL 컬럼에 존재하는 각 URL을 하나씩 처리
for url in urls_df['URL']:
    # URL에서 이미지 이름 추출
    name = url.rstrip('/').split('/')[-1]

    # 이미지 파일 경로 설정
    img_path = os.path.join(output_path, f"{name}.png")

    # 이미지 파일이 이미 존재하는 경우 건너뛰기
    if os.path.exists(img_path):
        print(f"Image {img_path} already exists. Skipping URL: {url}")
        continue

    print(f"Processing URL: {url}")
    driver.get(url)
    time.sleep(5)  # URL을 열고 작업을 수행하기 전 대기 시간

    # URL에서 수행할 작업
    try:
        img_element = driver.find_element(By.CSS_SELECTOR, "#__next > div > main > div.Container_container-wrapper__u0gtd > div > section > div > div.grid.grid-cols-12.gap-4.md\:gap-5.md\:mt-4 > div.col-span-12.md\:col-span-4.flex.flex-col.justify-center.items-center.p-8 > div > img")
        img_src = img_element.get_attribute('src')

        # 이미지 다운로드 및 저장
        img_data = requests.get(img_src).content
        with open(img_path, 'wb') as handler:
            handler.write(img_data)
        print(f"Image saved to {img_path}")

    except Exception as e:
        print(f"An error occurred while processing URL {url}: {e}")
        traceback.print_exc()

# 드라이버 종료
driver.quit()
