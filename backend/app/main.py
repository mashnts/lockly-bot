from fastapi import FastAPI
from app.routers import authors, channels, webhook, transactions, subscribers
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.tasks import check_expired_subscriptions
from aiogram.types import BotCommand

async def set_commands(bot):
    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="addchannel", description="Добавить канал"),
        BotCommand(command="dashboard", description="Мой кабинет"),
        BotCommand(command="subscribe", description="Подписаться на канал"),
        BotCommand(command="mysubscriptions", description="Мои подписки"),
    ])

app = FastAPI(title="Lockly")

app.include_router(authors.router)
app.include_router(channels.router)
app.include_router(webhook.router)
app.include_router(transactions.router)
app.include_router(subscribers.router)

scheduler = AsyncIOScheduler()

@app.on_event("startup")
async def startup():
    scheduler.add_job(check_expired_subscriptions, "interval", hours=1)
    scheduler.start()

