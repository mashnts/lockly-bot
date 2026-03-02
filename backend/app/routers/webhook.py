from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from app.database import get_db
from app.models import Transaction, Subscriber, Channel
from app.schemas import CryptoBotWebhook
from app.config import settings
from aiogram import Bot
import hmac
import hashlib  

router = APIRouter(prefix="/webhook")

def verify_signature(token: str, body: bytes, signature: str) -> bool:
    secret = hashlib.sha256(token.encode()).digest()
    hmac_hash = hmac.new(secret, body, hashlib.sha256).hexdigest()

    return hmac_hash == signature

@router.post("/cryptobot")
async def cryptobot_webhook(request: Request, data: CryptoBotWebhook, db: AsyncSession = Depends(get_db)):
    body = await request.body()
    signature = request.headers.get("crypto-pay-api-signature", "")
    res = verify_signature(settings.CRYPTOBOT_TOKEN, body, signature)

    if res == False:
        raise HTTPException(403, detail="Invalid signature")

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

    bot = Bot(token=settings.BOT_TOKEN)

    try:
        await bot.send_message(
        transaction.subscriber_telegram_id,
        "✅ Поздравляю, Подписка активирована!"
        )
        link = await bot.create_chat_invite_link(
        chat_id=channel.telegram_chat_id,
        member_limit=1
        )
        await bot.send_message(transaction.subscriber_telegram_id, f"Ссылка для вступления: {link.invite_link}")
        print("Сообщение отправлено успешно!")
    except Exception as e:
        print("ОШИБКА при отправке:", e)
    finally:
        await bot.session.close()
    
    
    

    db.add(subscriber)
    await db.commit()
    return {"ok": True}

