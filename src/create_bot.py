import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
import redis.asyncio as r

load_dotenv()
token = os.getenv("token")
blockchain = os.getenv("blockchain")

redis = r.StrictRedis()
storage = RedisStorage(redis)
bot = Bot(token=token, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher(storage=storage)