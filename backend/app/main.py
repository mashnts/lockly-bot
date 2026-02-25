from fastapi import FastAPI
from app.routers import authors, channels, webhook, transactions

app = FastAPI(title="Lockly")

app.include_router(authors.router)
app.include_router(channels.router)
app.include_router(webhook.router)
app.include_router(transactions.router)