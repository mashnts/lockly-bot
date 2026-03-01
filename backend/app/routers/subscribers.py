from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Subscriber, Channel

router = APIRouter(prefix="/subscribers")

@router.get("/{telegram_id}")
async def get_subscriptions(telegram_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute.select(Subscriber, Channel).join(Channel, Channel.id == Subscriber.channel_id).where(Subscriber.telegram_id == telegram_id, Subscriber.is_active == True)
    rows = result.all()
    return [
        {
            "channel_title": channel.title,
            "expires_at": subscriber.expires_at,
        }
        for subscriber, channel in rows
    ]