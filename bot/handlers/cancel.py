from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router()

@router.message(Command("cancel"), StateFilter("*"))
async def cancel(message: Message, state: FSMContext):
    await message.answer("Действие отменено!")
    await state.clear()