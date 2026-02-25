from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.services import get_author

router = Router()

@router.message(Command("dashboard"))
async def dashboard(message: Message):
    author = await get_author(message.from_user.id)
    await message.answer(
        f"Твой кабинет:\n\n"
        f"Баланс: {author['balance']} USDT\n"
        f"ID: {author['id']}"
    )
