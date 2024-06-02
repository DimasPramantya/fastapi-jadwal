from fastapi import APIRouter, Depends, Request
from util.db_connection import AsyncSession, get_async_session
from controller.principal import oauth, redirectOauth, getUserData

router = APIRouter()

@router.post("/google-oauth")
async def oauth_with_google():
    return await oauth()

@router.get("/oauth-redirect")
async def google_oauth_redirect(request: Request):
    code = request.query_params.get("code")
    return await redirectOauth(code)