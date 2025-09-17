from aiogram import Router, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from utils.token import get_token_info
from utils.get_num_by_text import get_num
from database import Users

router = Router()

@router.message(F.text == "Your positions")
async def position(msg: Message):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Close position", callback_data="close_position")]
        ]
    )
    user = Users(msg.from_user.id)
    token_ca = await user.get_user_token_ca()
    buy_token_supply = await user.get_user_buy_token_supply()
    buy_usd_supply = await user.get_user_buy_usd_supply()

    if not token_ca or not buy_token_supply or not buy_usd_supply:
        await msg.reply("You havent opened positions")
        return
    
    jetton = await get_token_info(token_ca)
    jetton = jetton["data"]["attributes"]
    price = get_num(jetton["price_usd"])

    await msg.reply("Your position:\n\n"
                    f"{jetton["name"]} ~ {jetton["symbol"]}\n"
                    f"{buy_usd_supply} -> {get_num(round(buy_token_supply * price, 5))}",
                    reply_markup=markup)

@router.callback_query(F.data == "close_position")
async def close_position(call: CallbackQuery):
    user = Users(call.from_user.id)
    token_ca = await user.get_user_token_ca()
    buy_token_supply = await user.get_user_buy_token_supply()

    jetton = await get_token_info(token_ca)
    jetton = jetton["data"]["attributes"]
    price = get_num(jetton["price_usd"])

    await user.selling_token(buy_token_supply, price)

    await call.message.edit_text("Your position closed")