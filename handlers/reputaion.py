from aiogram import types, Dispatcher
from create_bot import bot, auth_token
from data_base.google import as_sheet_data
from analytics import history
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import keyboards
import requests
from auth import proxy_list
import random
from handlers.calculation import isint
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


async def rusprofile(inn):
    """ Функция по ИНН проверяет является ли данная организация действующей. Для поиска необходимо указать переменную
    inn с ИНН компании. В ответе возвращает значения 'Наименование организации' и 'Статус организации' в виде списка"""
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
    """Функция запускает машину состояний для ввода ИНН пользователем"""
    try:
        await history.analytics_callback(message=message)
    except:
        pass
    await message.message.edit_reply_markup()
    await auth_token.send_message(message.from_user.id,
                                  text="Введите ИНН (от 10 до 13 цифр)")
    await FSMinn.inn.set()


async def save_manufacture_exam(message: types.CallbackQuery, state: FSMContext):
    """Функция проверяет ИНН на сайте Руспрофиля и через гугл-таблицы реестра лабораторных испытаний
    и реестр обязательных сертификатов"""
    if not await isint(message.text):
        await state.finish()
        await auth_token.send_message(message.from_user.id,
                                      text='Некорректный формат ввода. ИНН должно быть целым числом',
                                      reply_markup=keyboards.back_to_menu_from_exam_inn(order=False))
    else:
        if len(message.text) == 10 or len(message.text) == 13:
            async with state.proxy() as data:
                data['inn'] = message.text
                exam_status_manufacture = await rusprofile(inn=data['inn'])
                title_manufacture = exam_status_manufacture[0]
                status_manufacture = exam_status_manufacture[1]
                count_all_lab_exam = 0
                count_bad_lab_exam = 0
                count_all_sert_exam = 0
                count_bad_sert_exam = 0
                exam_labtest_manufacture = await as_sheet_data(link="1zxWTxu6TsMf--fqIAWe-JIQVOgb0z4Yt8OJZhRFV52w",
                                                               list="'Обновлен 18.11.2022'!A2:M1100",
                                                               path="lab-reestr-6aa81a2d3150.json")
                for poin_lab_exam in exam_labtest_manufacture:
                    if str(poin_lab_exam[4]) == str(data['inn']):
                        count_all_lab_exam += 1
                        if str(poin_lab_exam[-1]) == 'Не соответствует НД':
                            count_bad_lab_exam += 1
                exam_sert_manufacture = await as_sheet_data(link='1NG2gg8YmPmW3g5qWNz_c08e4q0SJGxV3let9BVIxfh8',
                                                            list="'Обязательные СС'!A2:Q550",
                                                            path="lab-reestr-6aa81a2d3150.json")
                for point_sert_exam in exam_sert_manufacture:
                    if len(point_sert_exam[-2]) == 9:
                        edit_point_sert_exam = "0" + str(point_sert_exam[-2])
                    else:
                        edit_point_sert_exam = str(point_sert_exam[-2])
                    if edit_point_sert_exam == str(data['inn']):
                        count_all_sert_exam += 1
                        if point_sert_exam[0] == "есть нарушения":
                            count_bad_sert_exam += 1
            await auth_token.send_message(message.from_user.id,
                                          text=f'<b>Компания</b>: {title_manufacture}\n'
                                               f'<b>Статус</b>: {status_manufacture}\n\n'
                                               f'<b>Количество проведенный испытаний</b>: {count_all_lab_exam}\n'
                                               f'<b>Количество испытаний с нарушениями</b>: {count_bad_lab_exam}\n\n'
                                               f'<b>Количество обязательных сертификатов</b>: {count_all_sert_exam}\n'
                                               f'<b>Количество обязательных сертификатов с нарушениями</b>: {count_bad_sert_exam}',
                                          reply_markup=keyboards.back_to_menu_from_exam_inn(order=True), parse_mode="HTML")
            await state.finish()
        else:
            await state.finish()
            await auth_token.send_message(message.from_user.id, text='Неверное количество символов',
                                          reply_markup=keyboards.back_to_menu_from_exam_inn(order=False))


def reg_handlers_manufacture(bot: Dispatcher):
    bot.register_message_handler(save_manufacture_exam, state=FSMinn.inn)
