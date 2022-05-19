from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from googleapiclient import discovery
from google.oauth2 import service_account
import os
from analytics import history
from create_bot import bot
from keyboards.keyboards import menu_button


def sheet_data(link, list):
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


# Раздел "Стоимость полиэтилена"
async def plastic_price(message: types.Message):
    await history.analytics(message=message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_pe = types.KeyboardButton("Полиэтилен")
    markup.add(button_pe)
    button_pvh = types.KeyboardButton("Поливинилхлорид")
    markup.add(button_pvh)
    button_pvh = types.KeyboardButton("Полипропилен")
    markup.add(button_pvh)
    await message.answer('Выберите сырье', reply_markup=markup)
    await message.delete()


@bot.message_handler(Text(equals="Полиэтилен", ignore_case=True), state='*')
async def pe(message: types.Message):
    await history.analytics(message=message)
    await message.answer("Пожалуйста, подождите...")
    actual_pe_price = sheet_data("1zq3eIl3ppLUU-3WqtuT1Da9unN7qZFGzyvEycUR7WlY", "'Актуальная (ПЭ)'!A2:C15")
    price_data = sheet_data("1zq3eIl3ppLUU-3WqtuT1Da9unN7qZFGzyvEycUR7WlY", "'Актуальная (ПЭ)'!D2")
    await message.answer(f"<b>Изготовитель; марка; стоимость на {str(price_data)[3:13]} за тонну</b>")
    for price_pe in actual_pe_price:
        if len(price_pe) == 0:
            continue
        else:
            await message.answer(f"<b>{price_pe[0]}</b>: {price_pe[1]}\n{price_pe[2]}")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(menu_button)
    await message.answer('Что-то еще?', reply_markup=markup)


@bot.message_handler(Text(equals="Поливинилхлорид", ignore_case=True), state='*')
async def pvh(message: types.Message):
    await history.analytics(message=message)
    await message.answer("Пожалуйста, подождите...")
    actual_pvh_price = sheet_data("1zq3eIl3ppLUU-3WqtuT1Da9unN7qZFGzyvEycUR7WlY", "'Актуальная (ПВХ)'!A2:C15")
    price_data = sheet_data("1zq3eIl3ppLUU-3WqtuT1Da9unN7qZFGzyvEycUR7WlY", "'Актуальная (ПВХ)'!D2")
    await message.answer(f"<b>Изготовитель; марка; стоимость на {str(price_data)[3:13]} за тонну</b>")
    for price_pvh in actual_pvh_price:
        if len(price_pvh) == 0:
            continue
        else:
            await message.answer(f"<b>{price_pvh[0]}</b>: {price_pvh[1]}\n{price_pvh[2]}")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(menu_button)
    await message.answer('Что-то еще?', reply_markup=markup)


@bot.message_handler(Text(equals="Полипропилен", ignore_case=True), state='*')
async def pp(message: types.Message):
    await history.analytics(message=message)
    await message.answer("Пожалуйста, подождите...")
    actual_pp_price = sheet_data("1zq3eIl3ppLUU-3WqtuT1Da9unN7qZFGzyvEycUR7WlY", "'Актуальная (ППР)'!A2:C15")
    price_data = sheet_data("1zq3eIl3ppLUU-3WqtuT1Da9unN7qZFGzyvEycUR7WlY", "'Актуальная (ППР)'!D2")
    await message.answer(f"<b>Изготовитель; марка; стоимость на {str(price_data)[3:13]} за тонну</b>")
    for price_pp in actual_pp_price:
        if len(price_pp) == 0:
            continue
        else:
            await message.answer(f"<b>{price_pp[0]}</b>: {price_pp[1]}\n{price_pp[2]}")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(menu_button)
    await message.answer('Что-то еще?', reply_markup=markup)


def reg_handlers_plastic_price(bot: Dispatcher):
    bot.register_message_handler(plastic_price, content_types=['text'], text='Стоимость сырья')


