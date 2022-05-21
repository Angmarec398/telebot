from aiogram import executor
from create_bot import bot
from handlers import start, plastic_price, admin, sert_exam, other
from data_base import sqlite_db


async def online(_):
    print("Скрипт 'Чат-бот тест' запущен")
    sqlite_db.sql_start()


if __name__ == '__main__':
    # Регистрируем хендлеры
    start.reg_handlers_start_message(bot=bot)
    # plastic_price.reg_handlers_plastic_price(bot=bot)
    admin.reg_handlers_admin(bot=bot)
    sert_exam.reg_handlers_sert(bot=bot)

    other.reg_handlers_other_message(bot=bot)
    # Запускаем бота
    executor.start_polling(bot, skip_updates=True, on_startup=online)
