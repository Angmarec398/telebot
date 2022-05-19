#
#
# ### Раздел "Чек листы" ###
#
#     elif message.text.lower() == "получить чек-лист":
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         button_check_vnut_18599 = types.KeyboardButton("Трубы для водопровода (ГОСТ 18599)")
#         markup.add(button_check_vnut_18599)
#         button_check_vnut_58121 = types.KeyboardButton("Трубы для газа (ГОСТ Р 58121, 50838)")
#         markup.add(button_check_vnut_58121)
#         button_check_vnut = types.KeyboardButton("Внутренняя канализация (ГОСТ 32414)")
#         markup.add(button_check_vnut)
#         button_check_vnut_napor = types.KeyboardButton("Внутренние напорные трубы (ГОСТ 32415, 53630)")
#         markup.add(button_check_vnut_napor)
#         await message.answer('Выберите чек-лист'.format(message.from_user), reply_markup=markup)
#
#     elif message.text == "Внутренняя канализация (ГОСТ 32414)":
#         media = types.MediaGroup()
#         media.attach_document(types.InputFile('Внутрянняя канализация/Чек-лист для определения соответствия труб.docx.docx'))
#         media.attach_document(types.InputFile('Внутрянняя канализация/Акт входного контроля.xlsx'))
#         media.attach_document(types.InputFile('Внутрянняя канализация/Шаблон акта отбора образцов .docx'))
#         await message.reply_media_group(media=media)
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         markup.add(menu_botton)
#         await message.answer('Что-то еще?', reply_markup=markup)
#
#     elif message.text == "Внутренние напорные трубы (ГОСТ 32415, 53630)":
#         media = types.MediaGroup()
#         media.attach_document(types.InputFile('Внутренние напорные трубы/Чек-лист для определения соответствия труб.docx'))
#         media.attach_document(types.InputFile('Внутренние напорные трубы/Акт входного контроля.xlsx'))
#         media.attach_document(types.InputFile('Внутренние напорные трубы/Шаблон акта отбора образцов .docx'))
#         await message.reply_media_group(media=media)
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         markup.add(menu_botton)
#         await message.answer('Что-то еще?', reply_markup=markup)
#
#     elif message.text == "Трубы для водопровода (ГОСТ 18599)":
#         media = types.MediaGroup()
#         media.attach_document(types.InputFile('Трубы для водопровода (18599)/Чек-лист для определения соответствия труб.docx'))
#         media.attach_document(types.InputFile('Трубы для водопровода (18599)/Акт входного контроля.xlsx'))
#         media.attach_document(types.InputFile('Трубы для водопровода (18599)/Шаблон акта отбора образцов .docx'))
#         await message.reply_media_group(media=media)
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         markup.add(menu_botton)
#         await message.answer('Что-то еще?', reply_markup=markup)
#
#     elif message.text == "Трубы для газа (ГОСТ Р 58121, 50838)":
#         media = types.MediaGroup()
#         media.attach_document(types.InputFile('Трубы для газа (58121, 50838)/Чек-лист для определения соответствия труб.docx'))
#         media.attach_document(types.InputFile('Трубы для газа (58121, 50838)/Акт входного контроля.xlsx'))
#         media.attach_document(types.InputFile('Трубы для газа (58121, 50838)/Шаблон акта отбора образцов .docx'))
#         await message.reply_media_group(media=media)
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         markup.add(menu_botton)
#         await message.answer('Что-то еще?', reply_markup=markup)