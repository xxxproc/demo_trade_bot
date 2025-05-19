import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
import redis.asyncio as r

load_dotenv()
token = os.getenv("token")
blockchain = os.getenv("blockchain")

storage = MemoryStorage()
bot = Bot(token=token, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher(storage=storage)

redis = r.from_url("redis://localhost:6379")  # Локальный Redis