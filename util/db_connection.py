import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession as AsyncSessionType
from typing import AsyncGenerator
from model import Base
from dotenv import load_dotenv

load_dotenv()

# Get the database connection details from environment variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_URL = os.getenv("DB_URL")

# Construct the DATABASE_URL for SQLAlchemy
DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@34.101.188.235/{DB_NAME}"

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
