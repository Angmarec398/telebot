from aiogram import types, Dispatcher
from create_bot import bot, auth_token
from data_base.google import sheet_data
from analytics import history
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import keyboards
import requests
from auth import proxy_list
import random
from bs4 import BeautifulSoup
from urllib3 import disable_warnings, exceptions

disable_warnings(exceptions.InsecureRequestWarning)

random_proxy = random.choice(proxy_list)
need_proxy = {
    "https": f"http://{random_proxy['for connect']['login']}:{random_proxy['for connect']['password']}@{random_proxy['ip']}"
}

headers_rusprofile = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}


def rusprofile(inn):
    """ Функция по ИНН проверяет является ли данная организация действующей. Для поиска необходимо указать переменную
    inn с ИНН компании. В ответе возвращает значения 'Наименование организации' и 'Статус организации' в виде списка"""
    print(inn)
    if inn is None:
        title = 'Отсутсвует'
        status = 'Отсутсвует'
    else:
        url = f'https://www.rusprofile.ru/search?query={inn}&search_inactive=0'
        req = requests.get(url=url, proxies=need_proxy, headers=headers_rusprofile)
        soup = BeautifulSoup(req.text, 'lxml')
        title = soup.find('div', class_="company-header__row").text.strip()
        status = soup.find('div', class_="company-header__row").find('span').get('title')
    return title, status


class FSMinn(StatesGroup):
    inn = State()


# Раздел "Проверка сертификатов"
@bot.callback_query_handler(text='exam_inn')
async def manufacture_exam(message: types.CallbackQuery):
    await history.analytics_callback(message=message)
    await message.message.edit_reply_markup()
    await auth_token.send_message(message.from_user.id,
                                  text="Введите ИНН (от 10 до 13 цифр)")
    await FSMinn.inn.set()


async def save_manufacture_exam(message: types.CallbackQuery, state: FSMContext):
    if len(message.text) == 10 or len(message.text) == 13:
        async with state.proxy() as data:
            data['inn'] = message.text
            result = rusprofile(inn=data['inn'])
            print(result)
            title_manufacture = result[0]
            status_manufacture = result[1]
        await auth_token.send_message(message.from_user.id,
                                      text=f'Компания: {title_manufacture}\n'
                                           f'Статус: {status_manufacture}',
                                      reply_markup=keyboards.back_to_menu_from_exam_inn())
        await state.finish()
    else:
        await state.finish()
        await auth_token.send_message(message.from_user.id, text='Неверное количество символов',
                                      reply_markup=keyboards.back_to_menu_from_exam_inn())


def reg_handlers_manufacture(bot: Dispatcher):
    bot.register_message_handler(save_manufacture_exam, state=FSMinn.inn)
