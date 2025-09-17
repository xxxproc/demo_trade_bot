from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def positions_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Your positions")]
        ], resize_keyboard=True
    )