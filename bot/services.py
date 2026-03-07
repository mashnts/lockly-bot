import httpx
from bot.config import settings

async def create_author(telegram_id: int, username: str | None):
    headers = {"X-Internal-Token": settings.INTERNAL_API_TOKEN}
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{settings.BACKEND_URL}/authors/",
            json={"telegram_id": telegram_id, "username": username},
            headers=headers,
        )
        return resp.json()
    
async def create_channel(data: dict):
    headers = {"X-Internal-Token": settings.INTERNAL_API_TOKEN}
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{settings.BACKEND_URL}/channels/", json=data, headers=headers)
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
    headers = {"X-Internal-Token": settings.INTERNAL_API_TOKEN}
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{settings.BACKEND_URL}/transactions/", json=data, headers=headers)
        return resp.json()
    

async def get_my_subscriptions(telegram_id: int):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{settings.BACKEND_URL}/subscribers/{telegram_id}")
        return resp.json()
        
async def check_subscription(telegram_id: int, channel_id: int):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{settings.BACKEND_URL}/subscribers/check", params={"channel_id": channel_id, "telegram_id": telegram_id})
        if resp.status_code == 404 or not resp.content:
            return None
        resp.raise_for_status()
        return resp.json()