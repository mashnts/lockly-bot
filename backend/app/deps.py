from fastapi import Request, HTTPException, status
from app.config import settings

async def verify_internal_token(request: Request):
    token = request.headers.get("X-Internal-Token")
    
    if token != settings.INTERNAL_API_TOKEN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden",)