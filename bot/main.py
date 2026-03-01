import asyncio
from aiogram import Bot, Dispatcher
from bot.config import settings
from bot.handlers import start, channel, dashboard, subscribe, my_subscriptions

async def main():
    bot = Bot(token = settings.BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(channel.router)
    dp.include_router(dashboard.router)
    dp.include_router(subscribe.router)
    dp.include_router(my_subscriptions.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())