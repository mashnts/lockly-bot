from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Channel, Author, Subscriber
from app.schemas import ChannelCreate, ChannelResponse, SubscriberResponse
from app.deps import verify_internal_token

router = APIRouter(prefix="/channels", tags=["channels"])


@router.post("/", response_model=ChannelResponse)
async def create_channel(data: ChannelCreate, db: AsyncSession = Depends(get_db), _=Depends(verify_internal_token)):
    result = await db.execute(select(Author).where(Author.telegram_id == data.author_telegram_id))
    author = result.scalar_one_or_none()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    channel = Channel(
        author_id=author.id,
        telegram_chat_id=data.telegram_chat_id,
        title=data.title,
        description=data.description,
        price=data.price,
        period_days=data.period_days
    )
    db.add(channel)
    await db.commit()
    await db.refresh(channel)
    return channel


@router.get("/{channel_id}/subscribers", response_model=list[SubscriberResponse])
async def get_subscribers(channel_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Subscriber).where(Subscriber.channel_id == channel_id))
    subscribers = result.scalars().all()
    return subscribers


@router.get("/{channel_id}", response_model=ChannelResponse)
async def get_channel(channel_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Channel).where(Channel.id == channel_id))
    channel = result.scalar_one_or_none()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    return channel

