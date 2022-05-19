from aiogram import types, Dispatcher
from create_bot import bot
from data_base import sqlite_db
from analytics import history


# # Раздел "Новое обращение"
@bot.callback_query_handler(text='Поиск')
async def new_order(callback: types.CallbackQuery):
    await history.analytics_callback(message=callback)
    await sqlite_db.sql_read(message=callback)



