from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from model.user_model import User as UserModel


async def get_user_by_email(email: str, session: AsyncSession):
    # Query the user by email
    result = await session.execute(select(UserModel).filter(UserModel.email == email))
    user = result.scalars().first()
    return user