from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Transaction
from app.schemas import TransactionCreate, TransactionResponse

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/", response_model=TransactionResponse)
async def create_transaction(data: TransactionCreate, db: AsyncSession = Depends(get_db)):

    transaction = Transaction(
        channel_id = data.channel_id,
        subscriber_telegram_id = data.subscriber_telegram_id,
        amount = data.amount,
        cryptobot_invoice_id = data.cryptobot_invoice_id,
    )
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)
    return transaction

@router.get("/invoice/{invoice_id}", response_model=TransactionResponse)
async def get_transaction(invoice_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Transaction).where(Transaction.cryptobot_invoice_id == invoice_id))
    transaction = result.scalar_one_or_none()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    return transaction
    