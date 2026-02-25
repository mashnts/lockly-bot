from sqlalchemy import Column, BigInteger, DateTime, Numeric, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from enum import Enum

class TransactionStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    EXPIRED = "expired"

class WithdrawalStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String, nullable=True)
    balance = Column(Numeric, default=0)
    created_at = Column(DateTime, server_default=func.now())

    channels = relationship("Channel", back_populates="author")
    withdrawals = relationship("Withdrawal", back_populates="author")

class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    telegram_chat_id = Column(BigInteger, unique=True, nullable=False)
    title = Column(String)
    description = Column(String, nullable=True)
    price = Column(Numeric)
    period_days = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    author = relationship("Author", back_populates="channels")
    subscribers = relationship("Subscriber", back_populates="channel")
    transactions = relationship("Transaction", back_populates="channel")

class Subscriber(Base):
    __tablename__ = "subscribers"

    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, ForeignKey("channels.id"), nullable=False)
    telegram_id = Column(BigInteger, nullable=False)
    username = Column(String, nullable=True)
    expires_at = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    channel = relationship("Channel", back_populates="subscribers")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, ForeignKey("channels.id"), nullable=False)
    subscriber_telegram_id = Column(BigInteger, nullable=False)
    amount = Column(Numeric)
    cryptobot_invoice_id = Column(String, unique=True)
    status = Column(String, default=TransactionStatus.PENDING.value)
    created_at = Column(DateTime, server_default=func.now())

    channel = relationship("Channel", back_populates="transactions")

class Withdrawal(Base):
    __tablename__ = "withdrawals"

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    amount = Column(Numeric)
    status = Column(String, default=WithdrawalStatus.PENDING.value)
    created_at = Column(DateTime, server_default=func.now())


    author = relationship("Author", back_populates="withdrawals")