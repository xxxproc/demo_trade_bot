from create_bot import bot, dp
import asyncio
import logging

from client_menu.buying import router as buying_router
from client_menu.main_menu import router as main_menu_router
from client_menu.position import router as posititon_router

async def main():
    dp.include_router(buying_router)
    dp.include_router(posititon_router)
    dp.include_router(main_menu_router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())