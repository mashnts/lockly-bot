from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from app.database import get_db
from app.models import Transaction, Subscriber, Channel
from app.schemas import CryptoBotWebhook

router = APIRouter(prefix="/webhook")

@router.post("/cryptobot")
async def cryptobot_webhook(data: CryptoBotWebhook, db: AsyncSession = Depends(get_db)):
    if data.update_type != "invoice_paid":
        return {"ok": True}
    
    invoice_id = str(data.payload.get("invoice_id"))

    result = await db.execute(select(Transaction).where(Transaction.cryptobot_invoice_id == invoice_id))
    transaction = result.scalar_one_or_none()
    
    if not transaction:
        return {"ok": True}

    transaction.status = "paid"

    result2 = await db.execute(select(Channel).where(Channel.id == transaction.channel_id))
    channel = result2.scalar_one_or_none()

    subscriber = Subscriber(
    channel_id=transaction.channel_id,
    telegram_id=transaction.subscriber_telegram_id,
    expires_at=datetime.now() + timedelta(days=channel.period_days)
    )
    db.add(subscriber)
    await db.commit()
    return {"ok": True}
