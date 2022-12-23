from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from analytics import history
from create_bot import bot, auth_token
from data_base import sqlite_db
from keyboards import keyboards
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


async def isint(exam_string):
    """Функция проверки является ли строка целым числом"""
    try:
        int(exam_string)
        return True
    except ValueError:
        return False


@bot.callback_query_handler(text='calc')
async def calc_plastic(callback: types.CallbackQuery):
    """ Старт калькулятора по расчету цены на трубу"""
    try:
        await history.analytics_callback(message=callback)
    except:
        pass
    await callback.message.edit_reply_markup(keyboards.start_plastic_price(calc=True))


@bot.callback_query_handler(lambda call: call.data.startswith('plast_calc'))
async def start_calc(message: types.CallbackQuery):
    """В колбеке функция принимает информацию о наименовании марки полиэтилена и ее стоимости.
    Дальше передается информация только о стоимости."""
    try:
        price = int((str(message.data.split(':')[1]).replace(' ', '')).split('-')[0])
    except:
        price = 0
    await message.message.edit_reply_markup(keyboards.start_calc(price=price))


@bot.callback_query_handler(lambda call: call.data.startswith('SDR'))
async def calc_diameter(callback: types.CallbackQuery):
    """Функция получает данные о цене и о SDR трубы. Делает запрос информации о диаметрах труб из базы данных"""
    price = callback.data.split(':')[1]
    await sqlite_db.sql_diameter_calc(message=callback, price=price)


class FSMCalc(StatesGroup):
    metr = State()
    plastic_price = State()
    # SDR = State()
    # diametr = State()


@bot.callback_query_handler(lambda call: call.data.startswith('dia_button'))
async def calc_diameter(callback: types.CallbackQuery):
    """Функция получает данные о цене, диаметре и о SDR трубы. Запуск машины состояний для ввода метража трубы"""
    await callback.message.edit_reply_markup()
    SDR = callback.data.split(':')[2]
    diameter = callback.data.split(':')[1]
    if str(SDR) == "136":
        change_SDR = "13,6"
    elif str(SDR) == "74":
        change_SDR = "7,4"
    elif str(SDR) == "176":
        change_SDR = "17,6"
    else:
        change_SDR = SDR
    await auth_token.send_message(callback.from_user.id, text=f"Вводные данные:\n"
                                                              f"<b>SDR</b>: {change_SDR}\n"
                                                              f"<b>Диаметр</b>: {diameter}\n"
                                                              f"<b>Введите длину трубы в метрах</b>",
                                  parse_mode="HTML")
    await FSMCalc.metr.set()
    state = Dispatcher.get_current().current_state()
    await state.update_data(SDR=SDR, diameter=diameter,
                            price=callback.data.split(':')[3])


async def cancel_handler(message: types.Message, state: FSMContext):
    """Возможность отменить расчет"""
    current_stait = await state.get_state()
    if current_stait is None:
        return
    await state.finish()
    await message.reply("Расчет отменен")


async def give_pipe_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['plastic_price'] = message
    await FSMCalc.next()
    await message.reply('Введите стоимость полиэтилена за 1 кг (без копеек).')


async def calc_diameter_result(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        """ Вывод информации по расчету стоимости"""
        SDR = data.as_dict()['SDR']
        diameter = data.as_dict()['diameter']
        price = int(data.as_dict()['price'])
        if await isint(data.as_dict()['plastic_price']['text']):
            plastic_price = int(data.as_dict()['plastic_price']['text'])
        else:
            plastic_price = None
            await auth_token.send_message(message.from_user.id,
                                          text='Введена некорректная цена или метраж',
                                          reply_markup=keyboards.back_to_menu_from_calc())
        mass = await sqlite_db.sql_mass_pipe_calc(SDR=SDR, diameter=diameter)
        data['metr'] = message.text
        try:
            result_mass = float(str(mass).replace(",", "."))
        except:
            if await isint(str(mass)):
                result_mass = int(str(mass))
            else:
                result_mass = None
                await auth_token.send_message(message.from_user.id,
                                              text='Отсутствует информация. Вероятно соотношение SDR и диаметра некорректно',
                                              reply_markup=keyboards.back_to_menu_from_calc())
        try:
            result_metr = float(str(data['metr']).replace(",", "."))
        except:
            if await isint(str(data['metr'])):
                result_metr = int(str(data['metr']))
            else:
                result_metr = None
                await auth_token.send_message(message.from_user.id,
                                              text='Введен неокоренный метраж. Необходимо ввести целое число',
                                              reply_markup=keyboards.back_to_menu_from_calc())
    if mass == 0:
        await auth_token.send_message(message.from_user.id,
                                      text='Отсутствует информация. Вероятно соотношение SDR и диаметра некорректно',
                                      reply_markup=keyboards.back_to_menu_from_calc())
    elif result_mass is None:
        pass
    elif plastic_price is None:
        pass
    elif plastic_price > 0:
        mass_result = int(result_mass * result_metr)
        calc_result = int((result_mass * result_metr * plastic_price) * 1.27)
        calc_result_after_format = '{0:,}'.format(calc_result).replace(',', ' ')
        await auth_token.send_message(message.from_user.id, text=f'<b>Общий вес труб</b>: {mass_result} кг.\n'
                                                                 f'<b>Минимальная стоимость труб, '
                                                                 f'без учета доставки</b>: {calc_result_after_format} руб.',
                                      reply_markup=keyboards.back_to_menu_from_calc(), parse_mode="HTML")
    else:
        calc_result = int(result_mass * result_metr)
        await auth_token.send_message(message.from_user.id,
                                      text=f'Отсутствует информация о текущей стоимости полимера,общий вес труб {calc_result} кг.',
                                      reply_markup=keyboards.back_to_menu_from_calc())
    await state.finish()


def reg_handlers_calc(bot: Dispatcher):
    bot.register_message_handler(give_pipe_price, state=FSMCalc.metr)
    bot.register_message_handler(calc_diameter_result, state=FSMCalc.plastic_price)
    bot.register_message_handler(cancel_handler, state='*', content_types=['text'], text='Отмена')
    bot.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
