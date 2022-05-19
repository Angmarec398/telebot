from aiogram import Bot, types
from auth import token, admin_list
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

auth_token = Bot(token=token, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
bot = Dispatcher(auth_token, storage=storage)

