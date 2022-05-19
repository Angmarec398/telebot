from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from analytics import history
from auth import admin_list
from keyboards.keyboards import menu_button
from data_base import sqlite_db


class FSMAdmin(StatesGroup):
    notes = State()
    sert = State()
    passport = State()
    id = State()


# Начало диолога - Запуск машины состояния
async def fsm_start(message: types.Message):
    await history.analytics(message=message)
    if message.from_user.id in admin_list:
        await FSMAdmin.notes.set()
        await message.answer('Опишите ситуацию', reply_markup=types.ReplyKeyboardRemove())
        await message.delete()


async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id in admin_list:
        current_stait = await state.get_state()
        if current_stait is None:
            return
        await state.finish()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(menu_button)
        await message.reply("OK", reply_markup=markup)


# Запись в словарь
async def save_start(message: types.Message, state: FSMContext):
    if message.from_user.id in admin_list:
        async with state.proxy() as data:
            data['notes'] = message.text
        await FSMAdmin.next()
        await message.reply('Приложите сертификат пожалуйста')


# Шаг второй
async def fsm_step_two(message: types.Message, state: FSMContext):
    if message.from_user.id in admin_list:
        async with state.proxy() as data:
            data['sert'] = message.text
        await FSMAdmin.next()
        await message.reply('Приложите паспорт пожалуйста')


async def fsm_step_three(message: types.Message, state: FSMContext):
    if message.from_user.id in admin_list:
        async with state.proxy() as data:
            data['passport'] = message.text
        await FSMAdmin.next()
        await message.reply('Приложите ID пожалуйста')


async def fsm_step_four(message: types.Message, state: FSMContext):
    if message.from_user.id in admin_list:
        async with state.proxy() as data:
            data['id'] = message.from_user.id
        await sqlite_db.sql_add_command(state)
        # Остановка машины состояния
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(menu_button)
        await message.reply('Данные отправлены', reply_markup=markup)
        await state.finish()


def reg_handlers_admin(bot: Dispatcher):
    bot.register_message_handler(fsm_start, content_types=['text'], text='Проверка', state=None)
    bot.register_message_handler(cancel_handler, state='*', content_types=['text'], text='Отмена')
    bot.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    bot.register_message_handler(save_start,  state=FSMAdmin.notes)
    bot.register_message_handler(fsm_step_two, state=FSMAdmin.sert)
    bot.register_message_handler(fsm_step_three, state=FSMAdmin.passport)
    bot.register_message_handler(fsm_step_four, state=FSMAdmin.id)
