from database import Users
from create_bot import blockchain
from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from get_token_info import get_token_info

router = Router()

@router.message(Command("start"))
async def start_command(msg: types.Message):
    user = Users(msg.from_user.id)
    balance = await user.add_user_if_not_else_get_balance()

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Your positions")]
        ], 
        resize_keyboard=True
    )

    await msg.reply('Hi!\n'
                    f'I am the bot who does the analysis about {blockchain} tokens\n'
                    'Write me a CA and i will send information\n\n' \
                    f'Your balance: {balance}',
                    reply_markup=keyboard)

@router.message(F.text)
async def analize(msg: types.Message):
        token_ca = msg.text
        jetton = get_token_info(blockchain, token_ca)
        if jetton:
            jetton = jetton["data"]["attributes"]
            price = float(jetton["price_usd"])

            markup = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Demo buy", callback_data="demo")]
                ]
            )

            await msg.reply(f"{jetton["name"]} ~ {jetton["symbol"]}\n"
                            f"Price: {round(price, 5)}$\n"
                            f"<a href='https://dexscreener.com/{blockchain}/{msg.text}'>DEX</a>"
                            f" - <a href='https://www.geckoterminal.com/ru/{blockchain}/pools/{msg.text}'>Gecko</a>",
                            disable_web_page_preview=True,
                            reply_markup=markup)
            user = Users(msg.from_user.id)
            await user.set_token_ca(msg.text)
        else:
            await msg.reply("I am sorry\n"
                    "But your message has not a CA")