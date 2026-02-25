from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Author
from app.schemas import AuthorCreate, AuthorResponse

router = APIRouter(prefix="/authors", tags=["authors"])

@router.post("/", response_model=AuthorResponse)
async def create_author(data: AuthorCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Author).where(Author.telegram_id == data.telegram_id))
    author = result.scalar_one_or_none()

    if author:
        return author
    
    author = Author(telegram_id=data.telegram_id, username=data.username)
    db.add(author)
    await db.commit()
    await db.refresh(author)
    return author

@router.get("/{telegram_id}", response_model = AuthorResponse)
async def get_author(telegram_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Author).where(Author.telegram_id == telegram_id))
    author = result.scalar_one_or_none()

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    return author