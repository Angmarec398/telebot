from aiogram import types, Dispatcher
from create_bot import bot, auth_token
from analytics import history
from keyboards import keyboards
from bs4 import BeautifulSoup
import aiohttp


@bot.callback_query_handler(text='Разъяснения')
async def sert_exam(message: types.CallbackQuery):
    """Вызов стартовой клавиатуры по разъяснениям"""
    try:
        await history.analytics_callback(message=message)
    except:
        pass
    await message.message.edit_reply_markup(keyboards.start_talk())


@bot.callback_query_handler(text='talk_apts')
async def talk_apts(message: types.CallbackQuery):
    """Сбор наименований разъяснений АПТС и ссылок на них с сайта rapts.ru"""
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }
    url = 'https://rapts.ru/talk_apts'
    async with aiohttp.ClientSession() as session:
        req = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await req.text(), 'lxml')
        l_replace = '<div class="t431"><div class="t-container"> <div class="t-col t-col_12 t-prefix_ t431__tdscale_1 t-text t-text_sm t-align_left t431__withoutmobilescroll"> <div class="t431__wrapper-for-mobile"> <div class="t431__table-wrapper" data-auto-correct-mobile-width="false"> <table class="t431__table" data-table-width="10%;90%" width="100%"> </table> </div> </div> <div class="t431__data-part1" data-auto-correct-mobile-width="false" style="display: none">№;Наименование;</div> <div class="t431__data-part2" data-auto-correct-mobile-width="false" style="display: none">'
        r_replace = '</div> </div></div></div>'
        table = f"1; {str(soup.find_all(class_='t431')[0]).lstrip(l_replace).rstrip(r_replace)}".split('\n')
        data = {}
        for row in table:
            iter_step = row.split(';')[1]
            name = iter_step.split('link=')[0]
            link = f"{url}{iter_step.split('link=')[1]}"
            data.update({name: link})
        await message.message.edit_reply_markup(keyboards.talk(data=data))


@bot.callback_query_handler(text='talk_inter')
async def talk_inter(message: types.CallbackQuery):
    """Сбор наименований разъяснений сторонних организаций и ссылок на них с сайта rapts.ru"""
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }
    url = 'https://rapts.ru/talk_inter'
    async with aiohttp.ClientSession() as inter_session:
        req_inter = await inter_session.get(url=url, headers=headers)
        soup = BeautifulSoup(await req_inter.text(), 'lxml')
        result_inter_search = soup.find('div', attrs={"id": "rec431563719"}).text.lstrip(
            "№;Наименование; Источник ").split("\n")
        inter_data = {}
        for iter_note in result_inter_search:
            need_iter_text = str(iter_note.split(";")[1]).split("link=")
            name = need_iter_text[0].strip()
            link = f"{url}{need_iter_text[1].strip()}"
            inter_data.update({name: link})
        await message.message.edit_reply_markup(keyboards.talk(data=inter_data))
