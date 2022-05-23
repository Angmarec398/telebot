from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from analytics import history
from create_bot import bot, auth_token
from data_base import sqlite_db
from keyboards import keyboards
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


@bot.callback_query_handler(text='calc')
async def start_calc(message: types.CallbackQuery):
    await history.analytics_callback(message=message)
    await message.message.edit_reply_markup(keyboards.start_calc())


@bot.callback_query_handler(lambda call: call.data.startswith('SDR'))
async def calc_diameter(callback: types.CallbackQuery):
    await sqlite_db.sql_diameter_calc(message=callback)


class FSMCalc(StatesGroup):
    metr = State()
    SDR = State()
    diametr = State()


@bot.callback_query_handler(lambda call: call.data.startswith('dia_button'))
async def calc_diameter(callback: types.CallbackQuery):
    await auth_token.send_message(callback.from_user.id, text="Введите длину трубопровода(трубы) в метрах")
    await FSMCalc.metr.set()
    state = Dispatcher.get_current().current_state()
    await state.update_data(SDR=callback.data.split(':')[2], diameter=callback.data.split(':')[1])


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
        calc_result = int(result_mass * result_metr)
    await auth_token.send_message(message.from_user.id, text=f'Вес трубопровода {calc_result} кг.')
    await state.finish()


def reg_handlers_calc(bot: Dispatcher):
    bot.register_message_handler(calc_diameter_result, state=FSMCalc.metr)
    bot.register_message_handler(cancel_handler, state='*', content_types=['text'], text='Отмена')
    bot.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')


