from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import schedule
import time
from  _datetime import datetime

print("Скрипт запущен")

### Добавляем входные данные ###

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--no-sandbox')
options.headless = True

def refresh():
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        url = 'https://docs.google.com/spreadsheets/d/1xdnoVc0AVklCF070uJ_9tLj58XGHYhSDcO7Oh4VQXhA/edit'
        driver.get(url)
        time.sleep(5)
        driver.close()
        driver.quit()
        print(f"Обход завершен: {datetime.now().strftime('%d.%m.%Y - %H.%M.%S')}")
    except Exception as ex:
        print(f"Ошибка {ex}: {datetime.now().strftime('%d.%m.%Y - %H.%M.%S')}")

schedule.every(59).minutes.do(refresh)

while True:
    schedule.run_pending()
    time.sleep(1)