from aiogram.fsm.state import State, StatesGroup 
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from keyboard.cancel_fsm import cancel_kb
from keyboard.positions import positions_kb
from create_bot import blockchain
from utils.token import get_token_info
from database import Users
from filters.fsm_filter import IsActiveFSM
from utils.get_num_by_text import get_num

router = Router()

class quantity_state(StatesGroup):
    quantity = State()

@router.message(F.text == "Отмена", IsActiveFSM())
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Succesfully canceled", reply_markup=positions_kb())

@router.callback_query(F.data == "demo")
async def get_quantity(call: CallbackQuery, state: FSMContext):
    user = Users(call.from_user.id)
    balance = await user.get_user_balance()

    await call.message.delete()
    await call.message.answer(f"Your demo balance have {balance}$\n\n"
                                f"How much money do you want to buy it?",
                                reply_markup=cancel_kb())
    await state.set_state(quantity_state.quantity)

@router.message(quantity_state.quantity)
async def buy(msg: Message, state: FSMContext):
    try:
        dollar_quantity = int(msg.text)
    except ValueError:
        await msg.answer("Enter an integer")
        return

    user = Users(msg.from_user.id)
    balance = await user.get_user_balance()
    token_ca = await user.get_user_token_ca()

    if balance < dollar_quantity:
        await msg.answer("Your balance is less")
        return

    jetton = await get_token_info(token_ca)
    price = get_num(jetton["data"]["attributes"]["price_usd"])

    buy_token_supply = get_num(round(dollar_quantity / price, 5))

    await user.buying_token(dollar_quantity, buy_token_supply)

    await msg.answer("Token succesfully bought.\n"
                    "You can see position by button down", reply_markup=positions_kb())
    await state.clear()


@router.message(F.text)
async def analize(msg: Message):
    token_ca = msg.text
    jetton = await get_token_info(token_ca)

    if not jetton:
        await msg.reply("Your message has not a CA")
        return
    
    jetton = jetton["data"]["attributes"]
    price = get_num(jetton["price_usd"])

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
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
    await user.set_token_ca(token_ca)