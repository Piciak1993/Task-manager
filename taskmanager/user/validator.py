from typing import Optional
from sqlalchemy.orm import Session
from models import User
import httpx
from fastapi import HTTPException
import os

AUTH_SERVICE_URL = os.getenv('AUTH_SERVICE_URL', 'auth:8001')

async def verify_email_exist(email: str, db_session: Session) -> Optional[User]:
    return db_session.query(User).filter(User.email == email).first()

async def verify_token_via_auth_service(token: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(AUTH_SERVICE_URL, data={"token": token})
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Invalid token")
        return response.json()
