from aiogram import types, Dispatcher
from keyboards.keyboards import menu_button


async def other_message(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(menu_button)
    await message.answer('Неизвестная команда, нажмите кнопку "Назад" или введите команду /start', reply_markup=markup)


def reg_handlers_other_message(bot: Dispatcher):
    bot.register_message_handler(other_message)
