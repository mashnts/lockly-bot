from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from bot.states import AddChannel
from bot.services import create_channel

router = Router()

@router.message(Command("addchannel"))
async def add_channel_start(message: Message, state: FSMContext):
    await state.set_state(AddChannel.waiting_chat_id)
    await message.answer("Перешлите мне любое сообщение из канала или напишите его ID (например: -1001234567890)")

@router.message(AddChannel.waiting_chat_id, ~F.text.startswith("/"))
async def get_chat_id(message: Message, state: FSMContext):
    await state.update_data(chat_id=int(message.text))
    await state.set_state(AddChannel.waiting_title)
    await message.answer("Введите название канала:")

@router.message(AddChannel.waiting_title, ~F.text.startswith("/"))
async def get_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(AddChannel.waiting_description)
    await message.answer("Введите описание канала (или напишите 'нет'):")

@router.message(AddChannel.waiting_description, ~F.text.startswith("/"))
async def get_description(message: Message, state: FSMContext):
    desc = message.text if message.text.lower() != "нет" else None
    await state.update_data(description=desc)
    await state.set_state(AddChannel.waiting_price)
    await message.answer("Цена подписки в USDT:")

@router.message(AddChannel.waiting_price, ~F.text.startswith("/"))
async def get_price(message: Message, state: FSMContext):
    await state.update_data(price=float(message.text))
    await state.set_state(AddChannel.waiting_period)
    await message.answer("На сколько дней подписка:")

@router.message(AddChannel.waiting_period, ~F.text.startswith("/"))
async def get_period(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    channel = await create_channel({
        "author_telegram_id": message.from_user.id,
        "telegram_chat_id": data["chat_id"],
        "title": data["title"],
        "description": data["description"],
        "price": data["price"],
        "period_days": int(message.text)
    })

    await message.answer(f"Канал добавлен! ID: {channel['id']}")