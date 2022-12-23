import asyncio
from aiogram import types, Dispatcher
import auth
from create_bot import auth_token
from analytics import history
from create_bot import bot
from keyboards import keyboards


@bot.callback_query_handler(text='check_list')
async def sert_exam(message: types.CallbackQuery):
    try:
        await history.analytics_callback(message=message)
    except:
        pass
    await message.message.edit_reply_markup(keyboards.start_check_list())


@bot.callback_query_handler(lambda call: call.data.startswith('check_18599'))
async def check_18599(callback_message: types.CallbackQuery):
    await callback_message.message.edit_reply_markup()
    media = types.MediaGroup()
    media.attach_document(
        types.InputFile('Чек-листы/Трубы для водопровода (18599)/Чек-лист для определения соответствия труб.docx'))
    media.attach_document(types.InputFile('Чек-листы/Трубы для водопровода (18599)/Акт входного контроля.xlsx'))
    media.attach_document(types.InputFile('Чек-листы/Трубы для водопровода (18599)/Шаблон акта отбора образцов .docx'))
    await callback_message.message.reply_media_group(media=media)
    await auth_token.send_message(callback_message.from_user.id, text="ГОСТ 18599",
                                  reply_markup=keyboards.back_to_menu_from_checklist())


@bot.callback_query_handler(lambda call: call.data.startswith('check_58121'))
async def check_58121(callback_message: types.CallbackQuery):
    await callback_message.message.edit_reply_markup()
    media = types.MediaGroup()
    media.attach_document(
        types.InputFile('Чек-листы/Трубы для газа (58121, 50838)/Чек-лист для определения соответствия труб.docx'))
    media.attach_document(types.InputFile('Чек-листы/Трубы для газа (58121, 50838)/Акт входного контроля.xlsx'))
    media.attach_document(types.InputFile('Чек-листы/Трубы для газа (58121, 50838)/Шаблон акта отбора образцов .docx'))
    await callback_message.message.reply_media_group(media=media)
    await auth_token.send_message(callback_message.from_user.id, text="ГОСТ Р 58121",
                                  reply_markup=keyboards.back_to_menu_from_checklist())


@bot.callback_query_handler(lambda call: call.data.startswith('check_32414'))
async def check_32414(callback_message: types.CallbackQuery):
    await callback_message.message.edit_reply_markup()
    media = types.MediaGroup()
    media.attach_document(
        types.InputFile('Чек-листы/Внутренняя канализация (32414)/Чек-лист для определения соответствия труб.docx'))
    media.attach_document(types.InputFile('Чек-листы/Внутренняя канализация (32414)/Акт входного контроля.xlsx'))
    media.attach_document(types.InputFile('Чек-листы/Внутренняя канализация (32414)/Шаблон акта отбора образцов .docx'))
    await callback_message.message.reply_media_group(media=media)
    await auth_token.send_message(callback_message.from_user.id, text="ГОСТ 32414",
                                  reply_markup=keyboards.back_to_menu_from_checklist())


@bot.callback_query_handler(lambda call: call.data.startswith('check_54475'))
async def check_54475(callback_message: types.CallbackQuery):
    await callback_message.message.edit_reply_markup()
    media = types.MediaGroup()
    media.attach_document(
        types.InputFile('Чек-листы/Наружная канализация (54475)/Алгоритм отбора образцов труб.docx'))
    media.attach_document(types.InputFile('Чек-листы/Наружная канализация (54475)/Шаблон акта отбора образцов.docx'))
    await callback_message.message.reply_media_group(media=media)
    await auth_token.send_message(callback_message.from_user.id, text="ГОСТ 54475",
                                  reply_markup=keyboards.back_to_menu_from_checklist())


@bot.callback_query_handler(lambda call: call.data.startswith('check_32415'))
async def check_32415(callback_message: types.CallbackQuery):
    await callback_message.message.edit_reply_markup()
    media = types.MediaGroup()
    media.attach_document(
        types.InputFile('Чек-листы/Внутренние напорные трубы (32415)/Чек-лист для определения соответствия труб.docx'))
    media.attach_document(types.InputFile('Чек-листы/Внутренние напорные трубы (32415)/Акт входного контроля.xlsx'))
    media.attach_document(types.InputFile('Чек-листы/Внутренние напорные трубы (32415)/Шаблон акта отбора образцов .docx'))
    await callback_message.message.reply_media_group(media=media)
    await auth_token.send_message(callback_message.from_user.id, text="ГОСТ 32415",
                                  reply_markup=keyboards.back_to_menu_from_checklist())
