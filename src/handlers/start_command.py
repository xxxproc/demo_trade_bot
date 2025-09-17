from database import Users
from create_bot import blockchain
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboard.positions import positions_kb

router = Router()

@router.message(Command("start"))
async def start_command(msg: Message, state: FSMContext):
    await state.clear()

    user = Users(msg.from_user.id)
    balance = await user.get_user_balance()

    await msg.reply('Hi!\n'
                    f'I am the bot for demo trading with {blockchain} tokens\n'
                    'Write me a CA and i will send information\n\n'
                    f'Your balance: {balance}',
                    reply_markup=positions_kb())

