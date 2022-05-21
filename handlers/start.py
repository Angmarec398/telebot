from aiogram import types, Dispatcher
from auth import admin_list
from create_bot import bot
from keyboards.keyboards import start_callback_message


async def start_message(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    start_1 = types.InlineKeyboardButton(text="Поиск", callback_data='Поиск')
    start_2 = types.InlineKeyboardButton(text="Стоимость сырья", callback_data="plastic_price")
    markup.add(start_1, start_2)
    start_3 = types.InlineKeyboardButton(text="Чек-листы", callback_data="Чек-листы")
    if message.from_user.id in admin_list:
        start_4 = types.InlineKeyboardButton(text="Проверка", callback_data="Проверка")
        markup.add(start_3, start_4)
    else:
        markup.add(start_3)
    start_5 = types.InlineKeyboardButton(text="Сертификаты", callback_data="Сертификаты")
    markup.add(start_5)
    await message.answer('Чем могу помочь?', reply_markup=markup)
    await message.delete()


@bot.callback_query_handler(text='start_menu')
async def replace_menu(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(start_callback_message(message=callback))


# Список комманд (пока не вызывается)
async def set_default_commands(bot):
    await bot.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("help", "Помощь"),
        types.BotCommand("test", "Тест"),
        types.BotCommand("form", "Форма"),
        types.BotCommand("menu", "Меню"),
    ])


def reg_handlers_start_message(bot: Dispatcher):
    bot.register_message_handler(start_message, content_types=['text'], text=[
        '/start', 'start', '/help', 'help', 'Назад'
    ])

