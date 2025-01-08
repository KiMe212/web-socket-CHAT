from contextlib import asynccontextmanager
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from typing import AsyncGenerator

from app.config import config

# Создание асинхронного движка и сессии
engine: AsyncEngine = create_async_engine(config.db.url)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        try:
            yield session
        except SQLAlchemyError as exc:
            await session.rollback()
            raise exc

# Функция для зависимости сессии
async def db_session_dependency() -> AsyncGenerator[AsyncSession, None]:
    async with get_session() as session:
        yield session

Base = declarative_base()