from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.services import get_my_subscriptions

router = Router()

@router.message(Command("mysubscriptions"))
async def my_subscriptions(message: Message):
    subs = await get_my_subscriptions(message.from_user.id)

    if not subs:
        await message.answer("У вас нет активных подписок на текущее время")
        return
    
    text = "Ваши активные подписки:\n"
    
    for sub in subs:
        text += f"🔷 {sub['channel_title']}\n"
        text += f"   Активна до: {sub['expires_at'][:10]}\n\n"

    await message.answer(text)