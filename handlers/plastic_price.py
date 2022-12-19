from aiogram import types, Dispatcher
from googleapiclient import discovery
from google.oauth2 import service_account
import os
from analytics import history
from create_bot import bot
from keyboards import keyboards


def sheet_data(link, list):
    """ Считываем данные с Google Sheets"""
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
    ]
    secret_file = os.path.join(os.getcwd(), "lab-reestr-6aa81a2d3150.json")
    spreadsheet_id = link
    range_name = list
    credentials = service_account.Credentials.from_service_account_file(
        secret_file, scopes=scopes
    )
    service = discovery.build("sheets", "v4", credentials=credentials)
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range_name,
    ).execute()
    return values.get('values')


@bot.callback_query_handler(text='plastic_price')
async def sert_exam(message: types.CallbackQuery):
    await history.analytics_callback(message=message)
    await message.message.edit_reply_markup(keyboards.start_plastic_price())


@bot.callback_query_handler(lambda call: call.data.startswith('plastic-pe'))
async def plastic_pe(callback_message: types.CallbackQuery):
    """ Уточнение актуальной стоимости полиэтилена.
    Если calc True, значит данные для Калькулятора труб, если False, то для раздела Стоимость полимеров"""
    actual_pe_price = sheet_data("1zq3eIl3ppLUU-3WqtuT1Da9unN7qZFGzyvEycUR7WlY", "'Актуальная (ПЭ)'!A2:C15")
    try:
        calc = str(callback_message['data']).split(':')[1]
    except:
        calc = None
    await callback_message.message.edit_reply_markup(keyboards.plastic_price_info(actual_price=actual_pe_price,
                                                                                  row_width=2, plastic_sort='pe',
                                                                                  calc=calc))


@bot.callback_query_handler(lambda call: call.data.startswith('plastic-pp'))
async def plastic_pe(callback_message: types.CallbackQuery):
    """ Уточнение актуальной стоимости полипропилена.
    Если calc True, значит данные для Калькулятора труб, если False, то для раздела Стоимость полимеров"""
    try:
        calc = str(callback_message['data']).split(':')[1]
    except:
        calc = None
    actual_pp_price = sheet_data("1zq3eIl3ppLUU-3WqtuT1Da9unN7qZFGzyvEycUR7WlY", "'Актуальная (ППР)'!A2:C15")
    await callback_message.message.edit_reply_markup(keyboards.plastic_price_info(actual_price=actual_pp_price,
                                                                                  row_width=2, plastic_sort='pp',
                                                                                  calc=calc))


@bot.callback_query_handler(lambda call: call.data.startswith('plastic-pvh'))
async def plastic_pe(callback_message: types.CallbackQuery):
    """ Уточнение актуальной стоимости поливинилхлорида.
    Если calc True, значит данные для Калькулятора труб, если False, то для раздела Стоимость полимеров"""
    actual_pvh_price = sheet_data("1zq3eIl3ppLUU-3WqtuT1Da9unN7qZFGzyvEycUR7WlY", "'Актуальная (ПВХ)'!A2:C15")
    try:
        calc = str(callback_message['data']).split(':')[1]
    except:
        calc = None
    await callback_message.message.edit_reply_markup(keyboards.plastic_price_info(actual_price=actual_pvh_price,
                                                                                  row_width=2, plastic_sort='pvh',
                                                                                  calc=calc))

