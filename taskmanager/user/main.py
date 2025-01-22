from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from typing import List
from fastapi import APIRouter, Depends, status, Response, HTTPException
from httpx import Request
from sqlalchemy.orm import Session
import schema
import services
import validator
from fastapi.security import OAuth2PasswordBearer
import os
import db

AUTH_SERVICE_URL = os.getenv('AUTH_SERVICE_URL', 'auth:8001')

app = FastAPI(title="Task Management System", description="A simple API", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://auth:8001","http://localhost:8001","http://user:8000","http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


router = APIRouter(
    tags=['Users'],
    prefix='/user'
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"http://{AUTH_SERVICE_URL}/auth/login")
@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(request: schema.UserCreate, database: Session = Depends(db.get_db)):

    user = await validator.verify_email_exist(request.email, database)
    if user:
        raise HTTPException(
            status_code=400,
            detail="User already exists.",
        )

    new_user = await services.create_user(request, database)
    return new_user


@router.get('/', response_model=List[schema.UserResponse])
async def get_users(database: Session = Depends(db.get_db),
                    token: str = Depends(oauth2_scheme)):
    return await services.get_users(database)


@router.get('/{user_id}', response_model=schema.UserResponse)
async def get_user_by_id(user_id: int, database: Session = Depends(db.get_db),
                         token: str = Depends(oauth2_scheme)):
    return await services.get_user_by_id(user_id, database)


app.include_router(router)

