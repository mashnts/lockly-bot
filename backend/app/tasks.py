from datetime import datetime
from sqlalchemy import select
from app.database import async_session_maker
from app.models import Subscriber, Channel 
from app.config import settings
from aiogram import Bot

async def check_expired_subscriptions():
    async with async_session_maker() as db:
        result = await db.execute(select(Subscriber).where(Subscriber.expires_at < datetime.now(), Subscriber.is_active == True))
        expired = result.scalars.all()

        bot = Bot(token=settings.BOT_TOKEN)
        try:
            for subscriber in expired:
                subscriber.is_activate == False

                channel_result = await db.execute(select(Channel).where(Channel.id == subscriber.channel_id))
                channel = channel_result.sclar_one_or_none()

                if channel:
                    await bot.ban_chat_member(channel.telegram_chat_id, subscriber.telegram_id)
                    await bot.unban_chat_member(channel.telegram_chat_id, subscriber.telegram_id)
            await db.commit()
        finally:
            await bot.session.close()