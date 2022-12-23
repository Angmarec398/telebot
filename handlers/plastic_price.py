from aiogram import types, Dispatcher
from data_base.google import sheet_data
from analytics import history
from create_bot import bot
from keyboards import keyboards


@bot.callback_query_handler(text='plastic_price')
async def sert_exam(message: types.CallbackQuery):
    try:
        await history.analytics_callback(message=message)
    except:
        pass
    await message.message.edit_reply_markup(keyboards.start_plastic_price())


@bot.callback_query_handler(lambda call: call.data.startswith('plastic-pe'))
async def plastic_pe(callback_message: types.CallbackQuery):
    """ Уточнение актуальной стоимости полиэтилена.
    Если calc True, значит данные для Калькулятора труб, если False, то для раздела Стоимость полимеров"""
    actual_pe_price = sheet_data(link="1zq3eIl3ppLUU-3WqtuT1Da9unN7qZFGzyvEycUR7WlY", list="'Актуальная (ПЭ)'!A2:C15",
                                 path="lab-reestr-6aa81a2d3150.json")
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
    actual_pp_price = sheet_data(link="1zq3eIl3ppLUU-3WqtuT1Da9unN7qZFGzyvEycUR7WlY", list="'Актуальная (ППР)'!A2:C15",
                                 path="lab-reestr-6aa81a2d3150.json")
    await callback_message.message.edit_reply_markup(keyboards.plastic_price_info(actual_price=actual_pp_price,
                                                                                  row_width=2, plastic_sort='pp',
                                                                                  calc=calc))


@bot.callback_query_handler(lambda call: call.data.startswith('plastic-pvh'))
async def plastic_pe(callback_message: types.CallbackQuery):
    """ Уточнение актуальной стоимости поливинилхлорида.
    Если calc True, значит данные для Калькулятора труб, если False, то для раздела Стоимость полимеров"""
    actual_pvh_price = sheet_data(link="1zq3eIl3ppLUU-3WqtuT1Da9unN7qZFGzyvEycUR7WlY", list="'Актуальная (ПВХ)'!A2:C15",
                                  path="lab-reestr-6aa81a2d3150.json")
    try:
        calc = str(callback_message['data']).split(':')[1]
    except:
        calc = None
    await callback_message.message.edit_reply_markup(keyboards.plastic_price_info(actual_price=actual_pvh_price,
                                                                                  row_width=2, plastic_sort='pvh',
                                                                                  calc=calc))
