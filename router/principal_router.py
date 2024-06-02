from fastapi import APIRouter, Depends, Request, Response
from util.db_connection import AsyncSession, get_async_session
from controller.principal import oauth, redirectOauth, getUserData

router = APIRouter()

@router.post("/google-oauth")
async def oauth_with_google(response: Response):
    return await oauth(response)

@router.get("/oauth-redirect")
async def google_oauth_redirect(request: Request):
    code = request.query_params.get("code")
    return await redirectOauth(code)