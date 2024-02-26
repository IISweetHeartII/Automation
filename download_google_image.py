# pip install webdriver-manager selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import urllib.request
import os
import time

def download_google_images(search_query, max_images):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')  # 창 없는 모드
    chrome_options.add_argument('--start-fullscreen') # 전체화면 모드
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    current_dir = os.getcwd() # 현재 작업 디렉토리 경로를 가져옴
    folder_path = os.path.join(current_dir, search_query) # search_query 이름의 폴더 경로 생성
    if not os.path.exists(folder_path):
        os.makedirs(folder_path) # search_query 폴더가 없으면 생성

    URL = 'https://www.google.co.kr/imghp'
    driver.get(url=URL)
    driver.implicitly_wait(time_to_wait=10) # time.sleep=fixed, implicitly_wait=flexible
    keyElement = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea')
    keyElement.send_keys(search_query)
    keyElement.send_keys(Keys.RETURN) # 엔터키
    time.sleep(3)

    bodyElement = driver.find_element(By.TAG_NAME, 'body') # html <body 태그
    time.sleep(2)

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True: # 가장 아래까지 계속 실행
        for i in range(10):
            bodyElement.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2) # Wait to load page
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            try:
                driver.find_element(By.CSS_SELECTOR, ".LZ4I").click() # 결과 더보기 버튼 클릭
            except:
                break # 버튼을 클릭하지 못하면 빠져나가기
        last_height = new_height

    images = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd") # full XPATH를 시도해봤지만, 실패...
    print(f"찾은 {search_query}의 이미지의 개수는 {len(images)}개입니다.")
    imagecnt = 1
    for image in images:
        if imagecnt > max_images:  # 이미지 카운트가 최대 이미지 개수를 초과하면 반복문 종료
            print(f"max_images에 설정한 {max_images}개의 이미지를 저장했습니다.")
            break

        driver.execute_script("arguments[0].click();", image)
        time.sleep(0.5)

        highImages = driver.find_elements(By.XPATH, '//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]')
        # print(highImages[0].get_attribute('src')) # 진행과정을 보기 위한 출력함수
        if not highImages:  # 고화질 이미지가 없는 경우 다음 이미지로 넘어감
            print("고화질 이미지를 찾을 수 없습니다.")
            continue

        realImage = highImages[0].get_attribute('src')
        try:
            # 파일 확장자를 확인하고 .jpg만 저장합니다.
            if realImage.endswith('.jpg'):
                filename = f"{search_query}{imagecnt}.jpg"
                image_path = os.path.join(folder_path, filename)
                urllib.request.urlretrieve(realImage, image_path)
                imagecnt += 1
                time.sleep(0.5)
            elif realImage.endswith('.jpeg'):
                print(f"다운로드 건너뜀 (jpeg 파일): {realImage}")
            elif realImage.endswith('.png'):
                print(f"다운로드 건너뜀 (png 파일): {realImage}")
            elif realImage.endswith('.gif'):
                print(f"다운로드 건너뜀 (gif 파일): {realImage}")
            else:
                print(f"다운로드 건너뜀 (기타 파일): {realImage}")
                time.sleep(0.5)
                pass
        except urllib.error.HTTPError as e:
            print(f"HTTP 오류: {e.code} - {e.reason}")
        except IndexError as e:
            print(f"IndexError: {e} - 이미지가 페이지에 존재하지 않습니다.")
        except Exception as e:
            print(f"기타 예외 발생: {e}")
    
    print(f"{search_query}의 이미지 {imagecnt-1}개 저장 과정 완료.")


SQ_list1 = ['박보영', '한소희', '뉴진스 민지' '이민호']

for search_query in SQ_list1:
    max_images = 120 # 여기 있는 숫자만큼 저장
    download_google_images(search_query, max_images)

