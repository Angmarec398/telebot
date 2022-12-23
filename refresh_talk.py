from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import schedule
import time
from _datetime import datetime
from bs4 import BeautifulSoup
import requests
import random
from auth import proxy_list
from urllib3 import disable_warnings, exceptions

disable_warnings(exceptions.InsecureRequestWarning)

random_proxy = random.choice(proxy_list)
need_proxy = {
    "https": f"http://{random_proxy['for connect']['login']}:{random_proxy['for connect']['password']}@{random_proxy['ip']}"
}
url = "https://rapts.ru/talk_inter"

headers_apts = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36'
}

req = requests.get(url=url, headers=headers_apts)
soup = BeautifulSoup(req.text, 'lxml')
result = soup.find('div', attrs={"id": "rec431563719"}).text.lstrip("№;Наименование; Источник ").split("\n")
for item in result:
    need_iter_text = str(item.split(";")[1]).split("link=")
    name = need_iter_text[0].strip()
    link = need_iter_text[1].strip()
    print(f"{name} : {link}")




# print("Скрипт запущен")
# def refresh():
#     try:
#         ### Добавляем входные данные ###
#
#         options = webdriver.ChromeOptions()
#         options.add_argument("--disable-blink-features=AutomationControlled")
#         options.add_argument('--ignore-certificate-errors')
#         options.add_argument('--ignore-ssl-errors')
#         # options.add_argument('--no-sandbox')
#         options.headless = True
#         driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
#
#         ### Обходим страницы на сайте rapts ###
#
#         driver.get('https://rapts.ru/talk_inter')
#         first_soup = BeautifulSoup(driver.page_source, 'lxml')
#         time.sleep(1)
#         with open("talk_inter.txt", "w", encoding='cp1251') as first_file:
#             table = first_soup.find('tbody', class_='t431__tbody')
#             for row in table:
#                 string = row.find_all('a')
#                 for item in string:
#                     author = item.next_element.next_element.text
#                     link = f"https://rapts.ru/talk_inter{item.get('href')}"
#                     name = item.text
#                     first_file.write(f'{name, author, link}\n')
#
#         driver.get('https://rapts.ru/talk_apts')
#         second_soup = BeautifulSoup(driver.page_source, 'lxml')
#         time.sleep(1)
#         driver.close()
#         driver.quit()
#
#         with open("talk_rapts.txt", "w", encoding='cp1251') as second_file:
#             table = second_soup.find('tbody', class_='t431__tbody')
#             for row in table:
#                 string = row.find_all('a')
#                 for item in string:
#                     link = f"https://rapts.ru/talk_apts{item.get('href')}"
#                     name = item.text
#                     second_file.write(f'{name, link}\n')
#
#         print(f"Обход завершен: {datetime.now().strftime('%d.%m.%Y - %H.%M.%S')}")
#     except Exception as ex:
#         print(f"Ошибка {ex}: {datetime.now().strftime('%d.%m.%Y - %H.%M.%S')}")
#
# schedule.every(59).minutes.do(refresh)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
