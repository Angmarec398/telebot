import datetime
from data_base import sqlite_db


async def analytics(message):
    time = message['date']
    unic_id = message['message_id']
    text = message['text']
    user = message['from']['id']
    data = (
        unic_id,
        user,
        text,
        time
    )
    await sqlite_db.sql_save_analytics(data=data)


async def analytics_callback(message):
    time = message['message']['date']
    unic_id = message['message']['message_id']
    text = message['data']
    user = message['from']['id']
    data = (
        unic_id,
        user,
        text,
        time
    )
    await sqlite_db.sql_save_analytics(data=data)
