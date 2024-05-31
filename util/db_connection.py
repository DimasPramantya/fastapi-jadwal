from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession as AsyncSessionType
from typing import AsyncGenerator
from model import Base

DATABASE_URL = "mysql+aiomysql://root:root@localhost:3306/skripsi_thesya"

engine = create_async_engine(DATABASE_URL, echo=True)

# Configure the session maker
AsyncSessionLocal = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSessionType
)

async def get_async_session() -> AsyncGenerator[AsyncSessionType, None]:
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) 
