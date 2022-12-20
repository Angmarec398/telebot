import sqlite3
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from auth import admin_list
from create_bot import auth_token, bot
from data_base import sqlite_db
from handlers import plastic_price


# Раздел работы с клавиатурой и кнопками
# Стартовые клавиатуры
def start_keyboard(message):
    """Клавиатура основного меню"""
    markup = types.InlineKeyboardMarkup()
    start_1 = types.InlineKeyboardButton(text="Поиск", callback_data='Поиск')
    start_2 = types.InlineKeyboardButton(text="Стоимость сырья", callback_data="plastic_price")
    start_3 = types.InlineKeyboardButton(text="Калькулятор", callback_data="plast_calc")
    if message.from_user.id in admin_list:
        start_4 = types.InlineKeyboardButton(text="Проверка", callback_data="Проверка")
        markup.add(start_1, start_4)
        markup.add(start_2, start_3)
    else:
        markup.add(start_2, start_3)
    start_5 = types.InlineKeyboardButton(text="Проверка организации по ИНН", callback_data="exam_inn")
    markup.add(start_5)
    start_6 = types.InlineKeyboardButton(text="Разъяснения", callback_data="Разъяснения")
    markup.add(start_6)
    start_7 = types.InlineKeyboardButton(text="Сертификаты", callback_data="Сертификаты")
    markup.add(start_7)
    start_8 = types.InlineKeyboardButton(text='Просмотр аналитики', callback_data="analytics")
    markup.add(start_8)
    return markup


def start_callback_message(message: types.CallbackQuery):
    """Вывод стартового меню через callback запрос"""
    return start_keyboard(message=message)


def start_sert_exam():
    """ Стартовая клавиатура в разделе сертификаты """
    markup = types.InlineKeyboardMarkup()
    start_1 = types.InlineKeyboardButton(text="Найти сертификат 🔎", callback_data='search_setr')
    markup.add(start_1)
    start_2 = types.InlineKeyboardButton(text="Список сертификатов 📋", callback_data="sert_list")
    markup.add(start_2)
    start_3 = types.InlineKeyboardButton(text="Назад в меню ↩", callback_data="start_menu")
    markup.add(start_3)
    return markup


def start_talk():
    """ Стартовая клавиатура в разделе Разъяснения """
    markup = types.InlineKeyboardMarkup()
    tittle_button = types.InlineKeyboardButton(text='Выберите источник:', callback_data='start_menu')
    markup.add(tittle_button)
    start_1 = types.InlineKeyboardButton(text="Разъяснения Ассоциации", callback_data='talk_apts')
    markup.add(start_1)
    start_2 = types.InlineKeyboardButton(text="Разъяснения сторонних организаций", callback_data="talk_inter")
    markup.add(start_2)
    start_3 = types.InlineKeyboardButton(text="Назад в меню ↩", callback_data="start_menu")
    markup.add(start_3)
    return markup


def start_plastic_price(calc=None):
    """Стартовая клавиатура в разделе Стоимость полиэтилена(calk=None).
    Стартовая клавиатура в разделе Калькулятор трубы(calk=True).
    Следующие функции plastic_pe или plastic_pp или plastic_pvh в модуле plastic_price"""
    markup = types.InlineKeyboardMarkup()
    tittle_button = types.InlineKeyboardButton(text="Выберите полимер", callback_data=f'start_menu')
    markup.add(tittle_button)
    start_1 = types.InlineKeyboardButton(text="Полиэтилен", callback_data=f'plastic-pe:{calc}')
    start_3 = types.InlineKeyboardButton(text="Полипропилен", callback_data=f"plastic-pp:{calc}")
    markup.add(start_1, start_3)
    start_2 = types.InlineKeyboardButton(text="Поливинилхлорид", callback_data=f"plastic-pvh:{calc}")
    markup.add(start_2)
    start_4 = types.InlineKeyboardButton(text="Назад в меню ↩", callback_data=f"start_menu")
    markup.add(start_4)
    return markup


menu_button = types.InlineKeyboardButton('Назад')
main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True).add(menu_button)


def keyboard_search(data, new_row=0, table='info', collum_text=0, collum_callback=1,
                    row_width=2, count_button=4, name_collum='sert', back_to_menu=True):
    """# Первая линия Inline-кнопок при работе с БД """
    markup = InlineKeyboardMarkup()
    markup.row_width = row_width
    row = count_button + new_row
    markup.add(*[InlineKeyboardButton(text=button[collum_text],
                                      callback_data=f'button:{button[collum_callback]}:{name_collum}:{table}') for
                 button in data[new_row:row]])
    button_go = InlineKeyboardButton(text="Вперед ➡",
                                     callback_data=f'lets_go_search:{row}:{table}:{collum_text}:{collum_callback}:{row_width}:{count_button}:{name_collum}')
    button_back = InlineKeyboardButton(text="Назад ↩️",
                                       callback_data=f'lets_back_search:{row - (count_button * 2)}:{table}:{collum_text}:{collum_callback}:{row_width}:{count_button}:{name_collum}')
    if count_button < row > len(data):
        markup.add(button_back)
    elif new_row == 0 and count_button < len(data):
        markup.add(button_go)
    elif count_button > len(data):
        pass
    else:
        markup.add(button_back, button_go)
    if table == 'sert_list':
        button_search = InlineKeyboardButton(text='Поиск 🔎', callback_data='search_setr')
        markup.add(button_search)
    if back_to_menu:
        button_menu = InlineKeyboardButton(text='Назад в меню ↩', callback_data='start_menu')
        markup.add(button_menu)
    return markup


@bot.callback_query_handler(text_contains='lets_go_search')
async def callback_key(callback: types.CallbackQuery):
    """ Кнопка 'Вперед' в Inline-кнопках """
    await auth_token.answer_callback_query(callback.id)
    new_page = int((str(callback['data'])).split(':')[1])
    base = sqlite3.connect('rapts.db')
    cur = base.cursor()
    table = (str(callback['data'])).split(':')[2]
    cur.execute(f'SELECT * FROM {table}')
    collum_text = int((str(callback['data'])).split(':')[3])
    collum_callback = int((str(callback['data'])).split(':')[4])
    row_width = int((str(callback['data'])).split(':')[5])
    count_button = int((str(callback['data'])).split(':')[6])
    name_collum = (str(callback['data'])).split(':')[7]
    data = cur.fetchall()
    call = callback
    await call.message.edit_reply_markup(keyboard_search(data, table=table, new_row=new_page, collum_text=collum_text,
                                                         collum_callback=collum_callback, row_width=row_width,
                                                         count_button=count_button, name_collum=name_collum))


@bot.callback_query_handler(text_contains='lets_back_search')
async def callback_key(callback: types.CallbackQuery):
    """ Кнопка 'Назад' в Inline-кнопках """
    await auth_token.answer_callback_query(callback.id)
    new_page = int((str(callback['data'])).split(':')[1])
    base = sqlite3.connect('rapts.db')
    cur = base.cursor()
    table = (str(callback['data'])).split(':')[2]
    cur.execute(f'SELECT * FROM {table}')
    collum_text = int((str(callback['data'])).split(':')[3])
    collum_callback = int((str(callback['data'])).split(':')[4])
    row_width = int((str(callback['data'])).split(':')[5])
    count_button = int((str(callback['data'])).split(':')[6])
    name_collum = (str(callback['data'])).split(':')[7]
    data = cur.fetchall()
    call = callback
    await call.message.edit_reply_markup(keyboard_search(data, table=table, new_row=new_page, collum_text=collum_text,
                                                         collum_callback=collum_callback, row_width=row_width,
                                                         count_button=count_button, name_collum=name_collum))


@bot.callback_query_handler(lambda call: call.data.startswith('button'))
async def brain(callback: types.CallbackQuery):
    """ Вывод подробной информации со сертификату при нажатии на Inline-кнопку """
    row = await sqlite_db.sql_reach_info(callback_query=callback)
    if (str(callback['data'])).split(':')[3] == 'info':
        await callback.message.edit_reply_markup()
        await auth_token.send_message(callback.from_user.id,
                                      f'{row[0][0]},\n{row[0][1]},\n{row[0][2]}',
                                      reply_markup=back_to_menu_from_sert_exam())
    elif (str(callback['data'])).split(':')[3] == 'sert_list':
        await callback.message.edit_reply_markup()
        await auth_token.send_message(callback.from_user.id,
                                      f'{row[0][3]}\n{row[0][1]}\n{row[0][2]}',
                                      reply_markup=back_to_menu_from_sert_exam())


def plastic_price_info(actual_price, row_width=2, plastic_sort=None, calc=None):
    """Вывод клавиатуры выбора марки полимеров. Работает как с разделом калькулятор труб, так и стоимость полимеров.
    Следующие шаги: вывод информации через функцию plastic_brain в модуле keyboards или дальнейшее использование через
    функцию start_calc в модуле calculation"""
    if calc != 'True':
        markup = InlineKeyboardMarkup()
        markup.row_width = row_width
        tittle_button = types.InlineKeyboardButton(text="Выберите марку", callback_data=f'plastic_price')
        markup.add(tittle_button)
        markup.add(*[InlineKeyboardButton(text=button[1],
                                          callback_data=f'plastic_task:{button[1]}:{plastic_sort}:{calc}') for
                     button in actual_price])
        button_menu = InlineKeyboardButton(text='Назад ↩', callback_data='plastic_price')
        markup.add(button_menu)
        return markup
    else:
        markup = InlineKeyboardMarkup()
        markup.row_width = row_width
        tittle_button = types.InlineKeyboardButton(text="Выберите марку", callback_data=f'calc')
        markup.add(tittle_button)
        markup.add(*[InlineKeyboardButton(text=button[1],
                                          callback_data=f'plast_calc:{button[2]}:') for
                     button in actual_price])
        button_menu = InlineKeyboardButton(text='Назад ↩', callback_data='calc')
        markup.add(button_menu)
        return markup


@bot.callback_query_handler(text_contains='plastic_task')
async def plastic_brain(callback: types.CallbackQuery):
    """ Запрос подробной информации по полимерам при нажатии на Inline-кнопку """
    plastic_name = callback.data.split(':')[1]
    sheet_name = callback.data.split(':')[2]
    if sheet_name == 'pe':
        pp_list = plastic_price.sheet_data("1zq3eIl3ppLUU-3WqtuT1Da9unN7qZFGzyvEycUR7WlY", "'Актуальная (ПЭ)'!A2:C15",
                                           path="lab-reestr-6aa81a2d3150.json")
        price_data = plastic_price.sheet_data("1zq3eIl3ppLUU-3WqtuT1Da9unN7qZFGzyvEycUR7WlY", "'Актуальная (ПЭ)'!D2",
                                              path="lab-reestr-6aa81a2d3150.json")
        for plastic_item in pp_list:
            if plastic_item[1] == plastic_name:
                await callback.message.edit_reply_markup()
                await auth_token.send_message(callback.from_user.id,
                                              f'Марка: {plastic_item[1]}\nИзготовитель: {plastic_item[0]}\n'
                                              f'Стоимость за тонну: {plastic_item[2]}\nИнформация от {price_data[0][0]}',
                                              reply_markup=back_to_menu_from_plastic_price())
    elif sheet_name == 'pp':
        pp_list = plastic_price.sheet_data("1zq3eIl3ppLUU-3WqtuT1Da9unN7qZFGzyvEycUR7WlY", "'Актуальная (ППР)'!A2:C15",
                                           path="lab-reestr-6aa81a2d3150.json")
        price_data = plastic_price.sheet_data("1zq3eIl3ppLUU-3WqtuT1Da9unN7qZFGzyvEycUR7WlY", "'Актуальная (ППР)'!D2",
                                              path="lab-reestr-6aa81a2d3150.json")
        for plastic_item in pp_list:
            if plastic_item[1] == plastic_name:
                await callback.message.edit_reply_markup()
                await auth_token.send_message(callback.from_user.id,
                                              f'Марка: {plastic_item[1]}\nИзготовитель: {plastic_item[0]}\n'
                                              f'Стоимость за тонну: {plastic_item[2]}\nИнформация от {price_data[0][0]}',
                                              reply_markup=back_to_menu_from_plastic_price())
    elif sheet_name == 'pvh':
        pp_list = plastic_price.sheet_data("1zq3eIl3ppLUU-3WqtuT1Da9unN7qZFGzyvEycUR7WlY", "'Актуальная (ПВХ)'!A2:C15",
                                           path="lab-reestr-6aa81a2d3150.json")
        price_data = plastic_price.sheet_data("1zq3eIl3ppLUU-3WqtuT1Da9unN7qZFGzyvEycUR7WlY", "'Актуальная (ПВХ)'!D2",
                                              path="lab-reestr-6aa81a2d3150.json")
        for plastic_item in pp_list:
            if plastic_item[1] == plastic_name:
                await callback.message.edit_reply_markup()
                await auth_token.send_message(callback.from_user.id,
                                              f'Марка: {plastic_item[1]}\nИзготовитель: {plastic_item[0]}\n'
                                              f'Стоимость за тонну: {plastic_item[2]}\nИнформация от {price_data[0][0]}',
                                              reply_markup=back_to_menu_from_plastic_price())


def start_calc(price=0):
    """ Стартовая клавиатура в разделе Калькулятор. На вход получает информацию о цене. Передача информации в
    функцию calc_diameter в модуле calculation"""
    markup = types.InlineKeyboardMarkup()
    tittle_button = types.InlineKeyboardButton(text='Выберите SDR', callback_data='start_menu')
    markup.add(tittle_button)
    start_1 = types.InlineKeyboardButton(text='SDR 6', callback_data=f'SDR6:{price}')
    start_2 = types.InlineKeyboardButton(text='SDR 7,4', callback_data=f'SDR74:{price}')
    markup.add(start_1, start_2)
    start_3 = types.InlineKeyboardButton(text='SDR 9', callback_data=f'SDR9:{price}')
    start_4 = types.InlineKeyboardButton(text='SDR 11', callback_data=f'SDR11:{price}')
    markup.add(start_3, start_4)
    start_5 = types.InlineKeyboardButton(text='SDR 13,6', callback_data=f'SDR136:{price}')
    start_6 = types.InlineKeyboardButton(text='SDR 17', callback_data=f'SDR17:{price}')
    markup.add(start_5, start_6)
    start_7 = types.InlineKeyboardButton(text='SDR 17,6', callback_data=f'SDR176:{price}')
    start_8 = types.InlineKeyboardButton(text='SDR 21', callback_data=f'SDR21:{price}')
    markup.add(start_7, start_8)
    start_9 = types.InlineKeyboardButton(text='SDR 26', callback_data=f'SDR26:{price}')
    start_10 = types.InlineKeyboardButton(text='SDR 33', callback_data=f'SDR33:{price}')
    markup.add(start_9, start_10)
    start_11 = types.InlineKeyboardButton(text="Назад в меню ↩", callback_data="start_menu")
    markup.add(start_11)
    return markup


def diameter_calc(data, SDR=None, back_to_menu=True, price=None):
    """ Inline-кнопки для выбора диаметра трубы """
    markup = InlineKeyboardMarkup()
    markup.row_width = 5
    tittle_button = types.InlineKeyboardButton(text='Выберите диаметр', callback_data='start_menu')
    markup.add(tittle_button)
    markup.add(*[InlineKeyboardButton(text=button,
                                      callback_data=f'dia_button:{button}:{SDR}:{price}') for
                 button in data])
    if back_to_menu:
        button_menu = InlineKeyboardButton(text='Назад в меню ↩', callback_data='start_menu')
        markup.add(button_menu)
    return markup


def talk(data):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(*[InlineKeyboardButton(text=text,
                                      url=link) for
                 text, link in data.items()])
    button_menu = InlineKeyboardButton(text='Назад в меню ↩', callback_data='start_menu')
    markup.add(button_menu)
    return markup


def back_to_menu_from_calc():
    """Кнопки "Назад в меню" или "Проверить еще" в разделе Калькулятор трубы """
    markup = InlineKeyboardMarkup()
    button_menu = InlineKeyboardButton(text='Назад в меню ↩', callback_data='start_menu')
    button_calc = InlineKeyboardButton(text="Проверить еще 🔎", callback_data='plast_calc')
    markup.add(button_calc, button_menu)
    return markup


def back_to_menu_from_plastic_price():
    """Кнопки "Назад в меню" или "Проверить еще" в разделе Калькулятор трубы """
    markup = InlineKeyboardMarkup()
    button_menu = InlineKeyboardButton(text='Назад в меню ↩', callback_data='start_menu')
    button_calc = InlineKeyboardButton(text="Проверить еще 🔎", callback_data='plastic_price')
    markup.add(button_calc, button_menu)
    return markup


def back_to_menu_from_sert_exam():
    """Кнопки "Назад в меню" или "Проверить еще" в разделе Проверка сертификатов """
    markup = InlineKeyboardMarkup()
    button_menu = InlineKeyboardButton(text='Назад в меню ↩', callback_data='start_menu')
    button_sert = InlineKeyboardButton(text="Проверить еще 🔎", callback_data='search_setr')
    markup.add(button_sert, button_menu)
    return markup


def back_to_menu_from_exam_inn():
    """Кнопки "Назад в меню" или "Проверить еще" в разделе Проверка по ИНН """
    markup = InlineKeyboardMarkup()
    button_menu = InlineKeyboardButton(text='Назад в меню ↩', callback_data='start_menu')
    button_inn = InlineKeyboardButton(text="Проверить еще 🔎", callback_data='exam_inn')
    markup.add(button_inn, button_menu)
    return markup

# def cancel_sert_exam():
#     """Кнопки "Назад в меню" или "Проверить еще" в разделе Калькулятор трубы """
#     markup = InlineKeyboardMarkup()
#     button_cancel = InlineKeyboardButton(text="Отмена", callback_data='sert_cancel')
#     markup.add(button_cancel)
#     return markup
# @bot.callback_query_handler(lambda call: True)
# async def brain(callback: types.CallbackQuery):
#     await sqlite_db.stoptopupcall(callback_query=callback)
