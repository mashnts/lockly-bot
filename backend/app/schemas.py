from pydantic import BaseModel
from datetime import datetime


class AuthorCreate(BaseModel):
    telegram_id: int
    username: str | None = None


class AuthorResponse(BaseModel):
    id: int
    telegram_id: int
    username: str | None
    balance: float
    created_at: datetime

    class Config:
        from_attributes = True


class ChannelCreate(BaseModel):
    telegram_chat_id: int
    author_telegram_id: int
    title: str
    description: str | None
    price: float
    period_days: int


class ChannelResponse(BaseModel):
    id: int
    author_id: int
    telegram_chat_id: int
    title: str
    description: str | None
    price: float
    period_days: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class SubscriberResponse(BaseModel):
    id: int
    channel_id: int
    telegram_id: int
    username: str | None
    expires_at: datetime
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class WithdrawalCreate(BaseModel):
    amount: float


class WithdrawalResponse(BaseModel):
    id: int
    author_id: int
    amount: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class CryptoBotWebhook(BaseModel):
    update_type: str
    payload: dict


class TransactionCreate(BaseModel):
    subscriber_telegram_id: int
    channel_id: int
    amount: int
    cryptobot_invoice_id: str


class TransactionResponse(BaseModel):
    id: int
    subscriber_telegram_id: int
    channel_id: int
    amount: float
    status: str
    cryptobot_invoice_id: str
    created_at: datetime

    class Config:
        from_attributes = True