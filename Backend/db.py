from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Uuid, DateTime, func
from datetime import datetime
import os
import uuid

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://user_cafe:password_cafe@db:5432/cafe_database",
)

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

async def get_db():
    async with async_session() as session:
        yield session