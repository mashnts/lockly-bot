import httpx
from bot.config import settings

async def create_author(telegram_id: int, username: str | None):
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{settings.BACKEND_URL}/authors/", json={
            "telegram_id": telegram_id,
            "username": username
        })
        return resp.json()
    

async def create_channel(data: dict):
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{settings.BACKEND_URL}/channels/", json=data)
        return resp.json()
    

async def get_author(telegram_id: int):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{settings.BACKEND_URL}/authors/{telegram_id}")
        return resp.json()
    

async def get_channel(channel_id: int):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{settings.BACKEND_URL}/channels/{channel_id}")
        return resp.json()
    
async def create_transaction(data: dict):
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{settings.BACKEND_URL}/transactions/", json=data)
        return resp.json()