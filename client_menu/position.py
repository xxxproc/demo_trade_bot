from aiogram import types, Router, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from get_token_info import get_token_info

from database import Users
from create_bot import blockchain

router = Router()

@router.message(F.text == "Your positions")
async def position(msg: types.Message):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Close position", callback_data="close_position")]
        ]
    )
    # try:
    user = Users(msg.from_user.id)
    token_ca = await user.get_user_token_ca()
    buy_token_supply = await user.get_user_buy_token_supply()
    buy_usd_supply = await user.get_user_buy_usd_supply()

    jetton = get_token_info(blockchain, token_ca)["data"]["attributes"]
    price = float(jetton["price_usd"])

    print(f"{buy_token_supply} - {type(buy_token_supply)}")
    print(f"{price} - {type(price)}")

    await msg.reply("Your position:\n\n"
                    f"{jetton["name"]} ~ {jetton["symbol"]}\n"
                    f"{buy_usd_supply} -> {int(round(buy_token_supply * price, 0))}",
                    reply_markup=markup)
    # except:
    #     await msg.reply("You havent opened positions")

@router.callback_query(F.data == "close_position")
async def close_position(call: types.CallbackQuery):
    user = Users(call.from_user.id)

    token_ca = await user.get_user_token_ca()

    buy_token_supply = await user.get_user_buy_token_supply()
    price = float(get_token_info(blockchain, token_ca)["data"]["attributes"]["price_usd"])

    await user.selling_token(buy_token_supply, price)

    await call.message.edit_text("Your position closed")