from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator
from contextlib import asynccontextmanager

DATABASE_URL = ""

engine = create_async_engine(DATABASE_URL, echo=True)

Session_loacal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
) 

class Base(DeclarativeBase):
    pass

async def get_db()->AsyncGenerator[AsyncSession, None]:
    async with Session_loacal() as session:
        yield session


        