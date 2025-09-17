from aiogram import Router
from aiogram.types import ErrorEvent
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.error()
async def on_error_handler(event: ErrorEvent):
    logger.critical(f"Critical error caused by {event.exception}", exc_info=True)

    if event.update.message:
        await event.update.message.delete()
        await event.update.message.answer("Что-то пошло не так\nПожалуйста, попробуйте еще раз")
        return
    
    await event.update.callback_query.message.delete()
    await event.update.callback_query.message.answer("Что-то пошло не так\nПожалуйста, попробуйте еще раз")