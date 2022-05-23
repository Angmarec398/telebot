from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from analytics import history
from create_bot import bot, auth_token
from data_base import sqlite_db
from keyboards import keyboards
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


@bot.callback_query_handler(text='calc')
async def calc_plastic(callback: types.CallbackQuery):
    await history.analytics_callback(message=callback)
    await callback.message.edit_reply_markup(keyboards.start_plastic_price(calc=True))


@bot.callback_query_handler(lambda call: call.data.startswith('plast_calc'))
async def start_calc(message: types.CallbackQuery):
    try:
        price = int((str(message.data.split(':')[1]).replace(' ', '')).split('-')[0])
    except:
        price = 0
    await message.message.edit_reply_markup(keyboards.start_calc(price=price))


@bot.callback_query_handler(lambda call: call.data.startswith('SDR'))
async def calc_diameter(callback: types.CallbackQuery):
    price = callback.data.split(':')[1]
    await sqlite_db.sql_diameter_calc(message=callback, price=price)


class FSMCalc(StatesGroup):
    metr = State()
    # SDR = State()
    # diametr = State()


@bot.callback_query_handler(lambda call: call.data.startswith('dia_button'))
async def calc_diameter(callback: types.CallbackQuery):
    await auth_token.send_message(callback.from_user.id, text="Введите длину трубопровода(трубы) в метрах")
    await FSMCalc.metr.set()
    state = Dispatcher.get_current().current_state()
    await state.update_data(SDR=callback.data.split(':')[2], diameter=callback.data.split(':')[1], price=callback.data.split(':')[3])


async def cancel_handler(message: types.Message, state: FSMContext):
    current_stait = await state.get_state()
    if current_stait is None:
        return
    await state.finish()
    await message.reply("Расчет отменен")


async def calc_diameter_result(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        SDR = data.as_dict()['SDR']
        diameter = data.as_dict()['diameter']
        price = int(data.as_dict()['price'])
        mass = await sqlite_db.sql_mass_pipe_calc(SDR=SDR, diameter=diameter)
        data['metr'] = message.text
        try:
            result_mass = float(str(mass).replace(",", "."))
        except:
            result_mass = int(str(mass))
        try:
            result_metr = float(str(data['metr']).replace(",", "."))
        except:
            result_metr = int(str(data['metr']))
    if mass == 0:
        await auth_token.send_message(message.from_user.id,
                                      text='Отсутствует информация. Вероятно сооотношении SDR и диаметра некорректно')
    elif price > 0:
        mass_result = int(result_mass * result_metr)
        calc_result = int(result_mass * result_metr * price)/1000
        await auth_token.send_message(message.from_user.id, text=f'Цена за кг {price/1000} руб.\n'
                                                                 f'Общий вес труб {mass_result} кг.\n'
                                                                 f'Минимальная стоимость труб (трубопровода) {calc_result} руб.')
    else:
        calc_result = int(result_mass * result_metr)
        await auth_token.send_message(message.from_user.id,
                                      text=f'Отсутствует информация о текущей стоимости полимера,общий вес труб {calc_result} кг.')
    await state.finish()


def reg_handlers_calc(bot: Dispatcher):
    bot.register_message_handler(calc_diameter_result, state=FSMCalc.metr)
    bot.register_message_handler(cancel_handler, state='*', content_types=['text'], text='Отмена')
    bot.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')


