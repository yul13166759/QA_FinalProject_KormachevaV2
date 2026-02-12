from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
options.add_argument('--start-maximized')

print("Запускаем Chrome...")
driver = webdriver.Chrome(options=options)

try:
    url = "https://app.tandoor.dev/accounts/login/"
    print(f"Открываем {url}")
    driver.get(url)
    
    print(f"Текущий URL: {driver.current_url}")
    print(f"Заголовок страницы: {driver.title}")
    
    # Ждем загрузки
    time.sleep(5)
    
    # Пробуем найти body
    try:
        body = driver.find_element(By.TAG_NAME, "body")
        print(f"Body найден! HTML часть: {body.text[:500]}")
    except Exception as e:
        print(f"Body не найден: {e}")
    
    # Делаем скриншот
    driver.save_screenshot("debug_screenshot.png")
    print("Скриншот сохранен как debug_screenshot.png")
    
    # Ждем 10 секунд чтобы можно было посмотреть
    print("Ждем 10 секунд...")
    time.sleep(10)
    
finally:
    print("Закрываем браузер")
    driver.quit()
