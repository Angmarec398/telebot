import sqlite3
from create_bot import auth_token
from aiogram import types
from keyboards import keyboards


# Раздел работы с SQL базой данных
def sql_start():
    """ Создание БД """
    global base, cur
    base = sqlite3.connect('rapts.db')
    cur = base.cursor()
    if base:
        print("Database is connect")
    base.execute('CREATE TABLE IF NOT EXISTS info (description TEXT, sert TEXT PRIMARY KEY, passport TEXT, id TEXT )')
    base.execute('CREATE TABLE IF NOT EXISTS analytics (unic_id TEXT PRIMARY KEY, user TEXT, text TEXT, message TEXT )')
    base.commit()


async def sql_add_command(state):
    """ Запись данных в машину состояний """
    async with state.proxy() as data:
        cur.execute('INSERT INTO info VALUES(?,?,?,?)', tuple(data.values()))
        base.commit()


async def sql_read(message: types.CallbackQuery):
    """ Вывод данных из машины состояний """
    cur.execute('''SELECT * FROM info''')
    data = cur.fetchall()
    await message.message.edit_reply_markup(keyboards.keyboard_search(data))


async def sql_reach_info(callback_query: types.CallbackQuery):
    """ Подробная информация по записям """
    await auth_token.answer_callback_query(callback_query.id)
    collum = (str(callback_query['data'])).split(':')[2]
    table = (str(callback_query['data'])).split(':')[3]
    table_name_collum = cur.execute(f'PRAGMA table_info ({table})').fetchall()
    cur.execute(f'SELECT {collum} FROM {table}')
    sqldata = cur.fetchall()
    sortdata = []
    for name_collum in table_name_collum:
        if name_collum[1] == collum:
            for item in sqldata:
                sortdata.append(item[0])
            if str(callback_query.data.split(':')[1]) in sortdata:
                cur.execute(f'SELECT * FROM {table} WHERE {collum} = (?)', (str(callback_query.data.split(':')[1]),))
                row = cur.fetchall()
                return row


async def sql_save_analytics(data):
    """ Запись данных в БД в раздел аналитики """
    try:
        cur.execute('INSERT INTO analytics VALUES(?,?,?,?)', data)
        base.commit()
    except:
        pass


async def sql_sert_read(message: types.CallbackQuery):
    """ Вывод данных из БД по списки сертификатов """
    table = 'sert_list'
    name_collum = 'numbersert'
    cur.execute(f'SELECT * FROM {table}')
    data = cur.fetchall()
    await message.message.edit_reply_markup(keyboards.keyboard_search(data=data, table=table,
                                                                      collum_text=3, row_width=1,
                                                                      count_button=10, collum_callback=3,
                                                                      name_collum=name_collum))


async def sql_sert_search(call_message: types.CallbackQuery):
    """ Вывод данных из БД по найденым сертификатам """
    table = 'sert_list'
    name_collum = 'numbersert'
    cur.execute(f'SELECT * FROM {table}')
    all_data = cur.fetchall()
    data = []
    for item in all_data:
        if str(item[3][-5:]) == call_message.text:
            data.append(item)
    if len(data) == 0:
        await auth_token.send_message(call_message.from_user.id, text='Данного сертификата нет в базе',
                                      reply_markup=keyboards.keyboard_search(data=data, table=table, collum_text=3,
                                                                             row_width=1, count_button=10,
                                                                             collum_callback=3,
                                                                             name_collum=name_collum))
    else:
        await auth_token.send_message(call_message.from_user.id, text='Результат:',
                                      reply_markup=keyboards.keyboard_search(data=data, table=table, collum_text=3,
                                                                             row_width=1, count_button=10,
                                                                             collum_callback=3,
                                                                             name_collum=name_collum))


async def sql_diameter_calc(message: types.CallbackQuery, price=None):
    """ Вывод данных из БД по список диаметров труб. Передает информацию о диаметрах труб, SDR и стоимости"""
    cur.execute(f'SELECT Diameter FROM calc')
    SDR = message.data.lstrip('SDR')
    all_diameter = []
    data = cur.fetchall()
    [all_diameter.append(int(str(item[0]).lstrip('\ufeff'))) for item in data]
    all_diameter.sort()
    await message.message.edit_reply_markup(keyboards.diameter_calc(data=all_diameter, SDR=SDR, price=price))


async def sql_mass_pipe_calc(SDR, diameter):
    """ Вывод данных из БД по список диаметров труб """
    cur.execute(f'SELECT SDR{SDR} FROM calc where Diameter = ?', (diameter,))
    data = cur.fetchall()
    try:
        result = data[0][0]
    except:
        result = 0
    return result
