from fastapi import HTTPException, Request, Depends, Response
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from googleapiclient.discovery import build
import os
import jwt  
import time  
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
import requests
from sqlalchemy.ext.asyncio import AsyncSession
from model.user_model import User as UserModel
from .user_controller import getUserByEmail

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
REDIRECT_URI = os.getenv("REDIRECT_URI")
PROJECT_ID = os.getenv("PROJECT_ID")
CLIENT_SECRET_FILE = os.getenv("CLIENT_SECRET_FILE")

SCOPES = ["https://www.googleapis.com/auth/calendar.events", "https://www.googleapis.com/auth/userinfo.profile", "openid", "https://www.googleapis.com/auth/userinfo.email"]


flow = Flow.from_client_secrets_file(CLIENT_SECRET_FILE, scopes=SCOPES,  redirect_uri=REDIRECT_URI)


async def oauth(response: Response):
    # Set headers
    response.headers["Access-Control-Allow-Origin"] = '*'
    response.headers["Access-Control-Allow-Credentials"] = 'true'
    response.headers["Referrer-Policy"] = "no-referrer-when-downgrade"
    authorization_url, _ = flow.authorization_url(
        access_type='offline',
        prompt='consent'
    )
    return JSONResponse(content={"url": authorization_url})

async def redirectOauth(code: str, session: AsyncSession):
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not found")
    print('test')
    try:
        # Exchange authorization code for tokens
        flow.fetch_token(code=code)

        # Extract credentials
        credentials = flow.credentials

        # Get user data
        user_data = getUserData(credentials.token)

        print("get user email")
        #get user by email
        currentUserDb = await getUserByEmail(user_data['email'], session)
        print(currentUserDb)

        if not currentUserDb:
            user = UserModel(
                username = user_data['given_name'],
                email = user_data['email'],
                image_picture = user_data['picture'],
                role = "ADMIN",
                fullname = user_data['name']
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)

        # Return user data as JSON
        token = generate_token_oauth(credentials, user_data['given_name'], user_data['email'], user_data['picture']);
        return JSONResponse(content={"user_data": user_data, "token": token})

    except Exception as e:
        print(f"Error logging in with OAuth2 user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def getUserData(access_token: str):
    """Fetch user data using the access token"""
    try:
        response = requests.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching user data: {e}")
        return None

def generate_token_oauth(credentials, username, userId, profile_picture):
    payload = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "scopes": credentials.scopes,
        "username": username,
        "userId": userId,
        "profile_picture": profile_picture,
        "exp": int(time.time()) + 12000
    }
    encoded_jwt = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None