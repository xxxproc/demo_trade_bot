from create_bot import bot, dp
import asyncio
import logging

from handlers.errors.base import router as base_error_router

from handlers.position import router as position_router
from handlers.start_command import router as start_router

from handlers.buying import router as buying_router

from middlewares.rate_limit import RateLimitMiddleWare

async def main():
    dp.include_router(base_error_router)

    dp.include_router(position_router)
    dp.include_router(start_router)
    dp.include_router(buying_router)

    dp.update.middleware(RateLimitMiddleWare())

    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())