import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.driver_util import generate_driver
from utils.path_util import path_directory_generator
from utils.image_downlaod import download_image
import traceback
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

######################################################################

root = "https://www.google.com"

# 드라이버 생성
driver = generate_driver()

# 출력 폴더 경로 생성
output_path = path_directory_generator(r"google_mashup")

driver.get(root)

input("are you ready?")

# 이모지 스팬 리스트 찾기
emoji_span_list = driver.find_elements(By.CSS_SELECTOR,
                                       "#rso > div.ULSxyf > div > block-component > div > div.dG2XIf.EyBRub.Wnoohf.OJXvsb > div:nth-child(1) > div > div > div.ifM9O > div > div > div > div > div:nth-child(4) > div.Pg3sxc > div > span")


for i, emoji_a in enumerate(emoji_span_list):
    # 요소 찾기
    input_a = driver.find_element(By.CSS_SELECTOR,
                                  "#rso > div.ULSxyf > div > block-component > div > div.dG2XIf.EyBRub.Wnoohf.OJXvsb > div:nth-child(1) > div > div > div.ifM9O > div > div > div > div > div:nth-child(4) > div:nth-child(1) > div > div.z6GJoc > div:nth-child(2) > div > img")
    input_b = driver.find_element(By.CSS_SELECTOR,
                                  "#rso > div.ULSxyf > div > block-component > div > div.dG2XIf.EyBRub.Wnoohf.OJXvsb > div:nth-child(1) > div > div > div.ifM9O > div > div > div > div > div:nth-child(4) > div:nth-child(1) > div > div.z6GJoc > div:nth-child(4) > div > img")
    result_e = driver.find_element(By.CSS_SELECTOR,
                                   "#rso > div.ULSxyf > div > block-component > div > div.dG2XIf.EyBRub.Wnoohf.OJXvsb > div:nth-child(1) > div > div > div.ifM9O > div > div > div > div > div:nth-child(4) > div:nth-child(1) > div > div.z6GJoc > div.puXt0.OSfNIc.DttUDc > div.ESp68 > img")

    if emoji_a.get_attribute('tabindex') == '-1':
        continue

    input_a.click()
    time.sleep(1)

    emoji_a.click()
    time.sleep(1)

    for j, emoji_b in enumerate(emoji_span_list):
        if i == j or emoji_b.get_attribute('tabindex') == '-1':
            continue

        input_b.click()
        time.sleep(1)

        try:

            # 나머지 코드 계속...
            emoji_b.click()
            time.sleep(1)

            # 이미지 속성 추출
            input_a_src = input_a.get_attribute("src")
            input_a_aria_label = input_a.get_attribute("aria-label")
            input_a_code = input_a_src.split('/')[-2]

            input_b_src = input_b.get_attribute("src")
            input_b_aria_label = input_b.get_attribute("aria-label")
            input_b_code = input_b_src.split('/')[-2]

            result_e_src = result_e.get_attribute("src")
            result_e_alt = result_e.get_attribute("alt")

            # 폴더 이름 설정
            folder_name = f"{input_b_code}_{input_a_code}"
            folder_path = os.path.join(output_path, folder_name)

            # 폴더가 이미 존재하면 건너뜁니다.
            if os.path.exists(folder_path):
                print(f"Folder {folder_path} already exists. Skipping...")
                continue

            os.makedirs(folder_path, exist_ok=True)

            # 이미지 파일 이름 설정
            input_a_filename = os.path.join(folder_path, f"{input_a_code}.svg")
            input_b_filename = os.path.join(folder_path, f"{input_b_code}.svg")
            result_e_filename = os.path.join(folder_path, f"{input_b_code}_{input_a_code}.png")

            # 이미지 다운로드
            download_image(input_a_src, input_a_filename)
            download_image(input_b_src, input_b_filename)
            download_image(result_e_src, result_e_filename)

            # aria-label 저장 (각각의 txt 파일 생성)
            input_a_txt_filename = os.path.join(folder_path, f"{input_a_code}.txt")
            input_b_txt_filename = os.path.join(folder_path, f"{input_b_code}.txt")
            combined_txt_filename = os.path.join(folder_path, f"{input_b_code}_{input_a_code}.txt")

            with open(input_a_txt_filename, 'w', encoding='utf-8') as txt_file:
                txt_file.write(input_a_aria_label)

            with open(input_b_txt_filename, 'w', encoding='utf-8') as txt_file:
                txt_file.write(input_b_aria_label)

            with open(combined_txt_filename, 'w', encoding='utf-8') as txt_file:
                txt_file.write(f"{input_a_aria_label}\n{input_b_aria_label}")

            print(f"Images and aria-labels saved to {folder_path}")

        except Exception as e:
            print(traceback.format_exc())

# 드라이버 종료
driver.quit()
