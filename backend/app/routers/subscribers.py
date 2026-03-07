from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Channel, Author, Subscriber
from app.schemas import SubscriberResponse

router = APIRouter(prefix="/subscribers")

@router.get("/check", response_model=SubscriberResponse)
async def get_active_subscriber(channel_id: int, telegram_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Subscriber).where(Subscriber.channel_id == channel_id, Subscriber.telegram_id == telegram_id, Subscriber.is_active == True))
    subscriber = result.scalar_one_or_none()
    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    return subscriber 


@router.get("/{telegram_id}")
async def get_subscriptions(telegram_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Subscriber, Channel).join(Channel, Channel.id == Subscriber.channel_id).where(Subscriber.telegram_id == telegram_id, Subscriber.is_active == True))
    rows = result.all()
    return [
        {
            "channel_title": channel.title,
            "expires_at": subscriber.expires_at,
        }
        for subscriber, channel in rows
    ]

