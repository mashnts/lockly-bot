from aiocryptopay import AioCryptoPay, Networks
from bot.config import settings

crypto = AioCryptoPay(token=settings.CRYPTOBOT_TOKEN, network=Networks.TEST_NET)

async def create_invoice(asset: str, amount: float, description: str, payload: str, expires_in: str):
    invoice = await crypto.create_invoice(
        asset = asset,
        amount = amount,
        description = description, 
        payload = payload, 
        expires_in = expires_in
    )

    return invoice