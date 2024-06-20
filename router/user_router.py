from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import HTTPBearer

from schemas.user_schema import User as UserSchema, user_model_to_dict
from util.db_connection import AsyncSession, get_async_session
from controller.user_controller import *
from schemas.pagination_schema import Page

security = HTTPBearer()

async def get_token(token: str = Depends(security)):
    return token

router = APIRouter()

@router.get("/me")
async def getUserInfo(
    credentials: str = Depends(get_token),
    session = Depends(get_async_session)
):
    user = await getUserInfo(credentials.credentials, session)
    user_dict = user_model_to_dict(user)
    return user_dict