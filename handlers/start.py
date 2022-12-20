from aiogram import types, Dispatcher
from auth import admin_list
from create_bot import bot
from keyboards.keyboards import start_callback_message, start_keyboard


async def start_message(message: types.Message):
    """Вывод стартового меню через сообщения или команды"""
    await message.answer('Чем могу помочь?', reply_markup=start_keyboard(message=message))
    await message.delete()


@bot.callback_query_handler(text='start_menu')
async def replace_menu(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(start_callback_message(message=callback))


@bot.message_handler(content_types=types.ContentType.DOCUMENT)
async def scan_message(message: types.Message):
    print("downloading document")
    number = 1
    destination = f"C:\\Users\\ASUS\PycharmProjects\\telegram (test_version)\\{number}.pdf"
    await message.document.download(destination)
    print("success")


# Список комманд (пока не вызывается)
async def set_default_commands(bot):
    await bot.bot.set_my_commands([
        types.BotCommand("start", "Открыть меню"),
        types.BotCommand("help", "Помощь"),
        types.BotCommand("search_setr", "Найти сертификат")
    ])


def reg_handlers_start_message(bot: Dispatcher):
    bot.register_message_handler(start_message, content_types=['text'], text=[
        '/start', 'start', '/help', 'help', 'Назад'
    ])
