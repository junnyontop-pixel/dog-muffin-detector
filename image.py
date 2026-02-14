import os
import time
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def collect_images(keyword, save_path, count):
    print(f"🚀 {keyword} 이미지 수집 시작 (목표: {count}개)")
    
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
    options.add_argument('--headless')          # 화면 없이 실행
    options.add_argument('--no-sandbox')         # 보안 컨테이너 해제 (리눅스 필수)
    options.add_argument('--disable-dev-shm-usage') # 공유 메모리 부족 방지
    
    # 💡 드라이버는 한 번만 선언!
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # 봇 감지 우회 스크립트 실행
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    url = f"https://www.bing.com/images/search?q={keyword}"
    driver.get(url)
    time.sleep(3) # 이미지 로딩 대기시간을 조금 늘렸어

    # 스크롤 내리기
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    images = driver.find_elements(By.CSS_SELECTOR, "img.mimg")
    downloaded = 0

    for i, img in enumerate(images):
        if downloaded >= count:
            break
        
        try:
            # 덕덕고는 src 혹은 data-src에 이미지 주소가 있어
            img_url = img.get_attribute('src') or img.get_attribute('data-src')
            
            if img_url and 'http' in img_url:
                urllib.request.urlretrieve(img_url, os.path.join(save_path, f"{downloaded}.jpg"))
                downloaded += 1
                if downloaded % 10 == 0:
                    print(f"✅ {downloaded}개 완료...")
        except Exception as e:
            continue

    driver.quit()
    print(f"✨ {keyword} 수집 종료! (총 {downloaded}개)")

if __name__ == "__main__":
    # 키워드를 영어로 하면 더 정확한 이미지가 많이 나와!
    collect_images("chihuahua dog", "data/dog", 50)
    collect_images("muffin", "data/muffin", 50)