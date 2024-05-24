import requests
import time
import os
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.config import chrome_path, driver_path


def scroll_down(driver, ratio):
    driver.execute_script(f"window.scrollBy(0, window.innerHeight / {ratio});")


# 스크롤을 내리는 함수
def inf_scroll_down(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # 스크롤 후 로딩을 위한 대기 시간
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def generate_driver() -> webdriver.Chrome:
    # Chrome 옵션 설정
    chrome_options = Options()  # Chrome 실행 파일 경로 설정
    chrome_options.binary_location = chrome_path
    # chrome_options.add_argument("--headless")  # Run in background
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize WebDriver
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver
