from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from bot.services import create_author

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await create_author(
        telegram_id=message.from_user.id,
        username=message.from_user.username
    )
    await message.answer("Привет! Я Lockly 🔐\n\nКоманды:\n/addchannel — добавить канал\n/dashboard — мой кабинет")