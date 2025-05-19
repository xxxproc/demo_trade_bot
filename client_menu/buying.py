from aiogram.fsm.state import State, StatesGroup 
from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from create_bot import blockchain
from get_token_info import get_token_info
from database import Users

router = Router()

class quantity_state(StatesGroup):
    quantity = State()

@router.message(F.text == "Отмена")
async def cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Succesfully canceled", reply_markup=ReplyKeyboardRemove())

@router.callback_query(F.data == "demo")
async def get_quantity(call: types.CallbackQuery, state: FSMContext):
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Отмена")]
        ],
        resize_keyboard=True
    )
    user = Users(call.from_user.id)
    balance = await user.add_user_if_not_else_get_balance()
    await call.message.delete()
    await call.message.answer(f"Your demo balance have {balance}$\n\n"
                                f"How much money do you want to buy it?",
                                reply_markup=markup)
    await state.set_state(quantity_state.quantity)

@router.message(quantity_state.quantity)
async def buy(msg: types.Message, state: FSMContext):
    # try:
        dollar_quantity = int(msg.text)
        user = Users(msg.from_user.id)
        balance = await user.add_user_if_not_else_get_balance()
        token_ca = await user.get_user_token_ca()

        price = float(get_token_info(blockchain, token_ca)["data"]["attributes"]["price_usd"])

        if balance >= dollar_quantity:
            await state.update_data(quantity=dollar_quantity)

            buy_token_supply = int(round(dollar_quantity / price, 0))

            await user.buying_token(dollar_quantity, buy_token_supply)

            await msg.answer("Token succesfully bought.\n"
                            "You can see position by button down", reply_markup=ReplyKeyboardRemove())
            await state.clear()
        else:
            await msg.answer("Your balance is less")
    # except ValueError:
    #     await msg.answer("Enter an integer")