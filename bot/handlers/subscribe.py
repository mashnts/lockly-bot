from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from bot.services import get_channel, create_transaction
from bot.cryptopay import create_invoice 
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton 

router = Router()

@router.message(Command("subscribe"))
async def subscribe(message: Message):
    text = message.text.split()

    if len(text) < 2:
        await message.answer("Вы забыли айди канала!")
        return 
    
    channel_id = int(text[1])
    channel = await get_channel(channel_id)
    print(channel)


    if not channel:
        await message.answer("Канал не найден")
        return
    
    telegram_id = message.from_user.id
    payload = f"{channel_id},{telegram_id}"
    invoice = await create_invoice("USDT", channel['price'], f"Подписка на {channel['title']}", payload, 3600)
    print(invoice.__dict__)

    pay_btn = InlineKeyboardButton(text="Оплатить", url=invoice.bot_invoice_url)
    pay = InlineKeyboardMarkup(inline_keyboard=[[pay_btn]])
    
    transaction = await create_transaction({
            "channel_id": channel_id, 
            "subscriber_telegram_id": telegram_id,
            "amount": channel['price'],
            "cryptobot_invoice_id": invoice.bot_invoice_url
        })

    await message.answer(f"Информация о канале:\nНазвание: {channel['title']}, \nЦена: {channel['price']}", reply_markup=pay)