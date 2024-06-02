from fastapi import HTTPException, Request, Depends
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

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
REDIRECT_URI = os.getenv("REDIRECT_URI")
PROJECT_ID = os.getenv("PROJECT_ID")

SCOPES = ["https://www.googleapis.com/auth/calendar.events", "https://www.googleapis.com/auth/userinfo.profile", "openid"]

flow = Flow.from_client_config(
    {
        "web": {
            "client_id": CLIENT_ID,
            "project_id": PROJECT_ID,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": CLIENT_SECRET,
            "redirect_uris": [REDIRECT_URI]
        }
    },
    scopes=SCOPES
)

async def oauth():
    authorization_url, _ = flow.authorization_url(
        access_type='offline',
        prompt='consent',
        redirect_uri=REDIRECT_URI
    )
    return JSONResponse(content={"url": authorization_url})

async def redirectOauth(code: str):
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not found")

    try:
        # Exchange authorization code for tokens
        flow.fetch_token(code=code)

        # Extract credentials
        credentials = flow.credentials

        # Get user data
        user_data = getUserData(credentials.token)

        # Return user data as JSON
        return JSONResponse(content={"user_data": user_data, "token": credentials.token})

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

def generate_token(credentials):
    payload = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
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