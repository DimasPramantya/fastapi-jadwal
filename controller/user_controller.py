from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from model.user_model import User as UserModel
from dotenv import load_dotenv
from exceptions.bad_request_exception import BadRequestException
import os
import jwt

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

async def getUserByEmail(email: str, session: AsyncSession):
    # Query the user by email
    result = await session.execute(select(UserModel).filter(UserModel.email == email))
    user = result.scalars().first()
    return user

async def getUserInfo(token: str, session: AsyncSession):
    payload = verify_token(token)
    if payload:
        user = await getUserByEmail(payload.get("userId"), session)
        return user
    raise BadRequestException("Invalid token")

def verify_token(token):
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    return payload
