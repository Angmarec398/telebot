from aiogram import types, Dispatcher
from create_bot import bot, auth_token
from data_base import sqlite_db
from analytics import history
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import keyboards
from aiogram.dispatcher.filters import Text


# Раздел "Проверка сертификатов"
@bot.callback_query_handler(text='Сертификаты')
async def sert_exam(message: types.CallbackQuery):
    await history.analytics_callback(message=message)
    await message.message.edit_reply_markup(keyboards.start_sert_exam())


@bot.callback_query_handler(text='sert_list')
async def sert_exam(message: types.CallbackQuery):
    await history.analytics_callback(message=message)
    await sqlite_db.sql_sert_read(message=message)


class FSMSert(StatesGroup):
    sert = State()


@bot.callback_query_handler(text='search_setr')
async def start_search_sert(callback_sert: types.CallbackQuery):
    await callback_sert.message.edit_reply_markup()
    await auth_token.send_message(callback_sert.from_user.id,
                                  text="Введите последние 5 символов в сертификате. Пример 31/21 или 02575")
    await FSMSert.sert.set()


async def cancel_handler(message: types.Message, state: FSMSert):
    """Возможность отменить расчет"""
    current_stait = await state.get_state()
    if current_stait is None:
        return
    await state.finish()
    await message.reply("Проверка отменена")


async def save_start(message: types.CallbackQuery, state: FSMContext):
    if len(message.text) != 5:
        await state.finish()
        await auth_token.send_message(message.from_user.id, text='Неверное количество символов',
                                      reply_markup=keyboards.back_to_menu_from_sert_exam())
    else:
        async with state.proxy() as data:
            data['sert'] = message.text
        await auth_token.send_message(message.from_user.id,
                                      text=f'Проверяются сертификаты заканчивающиеся на {data["sert"]}...')
        await sqlite_db.sql_sert_search(call_message=message)
        await state.finish()


def reg_handlers_sert(bot: Dispatcher):
    bot.register_message_handler(save_start, state=FSMSert.sert)
    bot.register_message_handler(cancel_handler, state='*', content_types=['text'], text='Отмена')
    bot.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')

