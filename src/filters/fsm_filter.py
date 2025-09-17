from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

class IsActiveFSM(BaseFilter):
    async def __call__(self, event: CallbackQuery | Message, state: FSMContext) -> bool:
        data = await state.get_data()
        return True if data is not None else False