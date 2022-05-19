# from aiogram import types
# from aiogram.utils.markdown import hlink, hbold
#
# ### Раздел "Разяснения" ###
#
#     elif message.text.lower() == "прочесть разъяснения":
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         button_check_apts = types.KeyboardButton("Разъяснения Ассоциации")
#         markup.add(button_check_apts)
#         button_check_inter = types.KeyboardButton("Разъяснения сторонних организаций")
#         markup.add(button_check_inter)
#         await message.answer('Выберите источник'.format(message.from_user), reply_markup=markup)
#
#     elif message.text.lower() == "разъяснения ассоциации":
#         inter_file = open('talk_rapts.txt', 'r', encoding="cp1251")
#         for string in inter_file:
#             result = string.strip("(").rstrip(")\n").replace("'", "").split(" , ")
#             title = result[0]
#             link = result[1]
#             await message.answer(hlink(f'{title}', f'{link}'))
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         markup.add(menu_botton)
#         await message.answer('Что-то еще?', reply_markup=markup)
#
#     elif message.text.lower() == "разъяснения сторонних организаций":
#         inter_file = open('talk_inter.txt', 'r', encoding="cp1251")
#         for string in inter_file:
#             result = string.strip("(").rstrip(")\n").replace("'", "").split(", ")
#             title = result[0]
#             author = result[1]
#             link = result[2]
#             await message.answer(f"{hlink(f'{title}', f'{link}')}\n{hbold('Источник:')} {author}")
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         markup.add(menu_botton)
#         await message.answer('Что-то еще?', reply_markup=markup)