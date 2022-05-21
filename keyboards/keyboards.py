import sqlite3
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from auth import admin_list
from create_bot import auth_token, bot
from data_base import sqlite_db
from handlers import plastic_price


# Раздел работы с клавиатурой и кнопками
def start_callback_message(message: types.CallbackQuery):
    """ Стартовая клавиатура бота """
    markup = types.InlineKeyboardMarkup()
    start_1 = types.InlineKeyboardButton(text="Поиск", callback_data='Поиск')
    start_2 = types.InlineKeyboardButton(text="Стоимость сырья", callback_data="plastic_price")
    markup.add(start_1, start_2)
    start_3 = types.InlineKeyboardButton(text="Чек-листы", callback_data="Чек-листы")
    if message.from_user.id in admin_list:
        start_4 = types.InlineKeyboardButton(text="Проверка", callback_data="Проверка")
        markup.add(start_3, start_4)
    else:
        markup.add(start_3)
    start_5 = types.InlineKeyboardButton(text="Сертификаты", callback_data="Сертификаты")
    markup.add(start_5)
    return markup


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


def start_plastic_price():
    """ Стартовая клавиатура в разделе Стоимость полиэтилена """
    markup = types.InlineKeyboardMarkup()
    start_1 = types.InlineKeyboardButton(text="Полиэтилен", callback_data='plastic-pe')
    start_3 = types.InlineKeyboardButton(text="Полипропилен", callback_data="plastic-pp")
    markup.add(start_1, start_3)
    start_2 = types.InlineKeyboardButton(text="Поливинилхлорид", callback_data="plastic-pvh")
    markup.add(start_2)
    start_4 = types.InlineKeyboardButton(text="Назад в меню ↩", callback_data="start_menu")
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
                                      callback_data=f'button:{button[collum_callback]}:{name_collum}:{table}') for button in data[new_row:row]])
    button_go = InlineKeyboardButton(text="Вперед ➡",
                                     callback_data=f'lets_go_search:{row}:{table}:{collum_text}:{collum_callback}:{row_width}:{count_button}:{name_collum}')
    button_back = InlineKeyboardButton(text="Назад ↩️",
                                       callback_data=f'lets_back_search:{row - (count_button*2)}:{table}:{collum_text}:{collum_callback}:{row_width}:{count_button}:{name_collum}')
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


@bot.callback_query_handler(text_contains='button')
async def brain(callback: types.CallbackQuery):
    """ Запрос подробной информации при нажатии на Inline-кнопку """
    row = await sqlite_db.sql_reach_info(callback_query=callback)
    if (str(callback['data'])).split(':')[3] == 'info':
        await auth_token.send_message(callback.from_user.id,
                                      f'{row[0][0]},\n{row[0][1]},\n{row[0][2]}')
    elif (str(callback['data'])).split(':')[3] == 'sert_list':
        await auth_token.send_message(callback.from_user.id,
                                      f'{row[0][3]}\n{row[0][1]}\n{row[0][2]}')


# @bot.callback_query_handler(lambda call: True)
# async def brain(callback: types.CallbackQuery):
#     await sqlite_db.stoptopupcall(callback_query=callback)

def plastic_price_info(actual_price, price_data, row_width=2, plastic_sort=None):
    markup = InlineKeyboardMarkup()
    markup.row_width = row_width
    markup.add(*[InlineKeyboardButton(text=button[1],
                                      callback_data=f'plastic_task:{button[1]}:{plastic_sort}') for
                 button in actual_price])
    button_menu = InlineKeyboardButton(text='Назад ↩', callback_data='plastic_price')
    markup.add(button_menu)
    return markup


# @bot.callback_query_handler(text_contains='plastic_task')
# async def plastic_brain(callback: types.CallbackQuery):
#     """ Запрос подробной информации по полимерам при нажатии на Inline-кнопку """
#     print(callback)
    # row = await sqlite_db.sql_reach_info(callback_query=callback)
    # if (str(callback['data'])).split(':')[3] == 'info':
    #     await auth_token.send_message(callback.from_user.id,
    #                                   f'{row[0][0]},\n{row[0][1]},\n{row[0][2]}')
    # elif (str(callback['data'])).split(':')[3] == 'sert_list':
    #     await auth_token.send_message(callback.from_user.id,
    #                                   f'{row[0][3]}\n{row[0][1]}\n{row[0][2]}')
    # for price_pp in actual_price:
    #     if len(price_pp) == 0:
    #         continue
    #     else:
    #         f"<b>{price_pp[0]}</b>: {price_pp[1]}\n{price_pp[2]}"
