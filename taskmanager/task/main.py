from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from celery import Celery
import db
from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import schema
import services
import validator
import os


AUTH_SERVICE_URL = os.getenv('AUTH_SERVICE_URL', 'auth:8001')
app = FastAPI(title="Task Management System", description="A simple API", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://auth:8001","http://localhost:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
celery = Celery(
    __name__,
    broker='redis://valkey:6379/0',
    backend='redis://valkey:6379/0',
)

celery.conf.imports = [
    'tasks',
]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"http://{AUTH_SERVICE_URL}/auth/login")
router = APIRouter(
    tags=['Tasks'],
    prefix='/task'
)

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_task(request: schema.TaskCreate, database: Session = Depends(db.get_db),
                      token: str = Depends(oauth2_scheme)):
    await validator.verify_user_exists(request.user_id, token)

    new_task = await services.create_task(request, database)

    return new_task


@router.put('/{task_id}', response_model=schema.TaskResponse)
async def update_task(task_id: int, request: schema.TaskCreate,
                               database: Session = Depends(db.get_db),
                               token: str = Depends(oauth2_scheme)):
    await validator.verify_user_exists(request.user_id, token)
    updated_task = await services.update_task(request, database, task_id)
    return updated_task


@router.get('/', response_model=List[schema.TaskResponse])
async def get_tasks(database: Session = Depends(db.get_db),
                    token: str = Depends(oauth2_scheme)):


    return await services.get_tasks(database)


@router.get('/{user_id}', response_model=schema.TaskResponse)
async def get_task_by_id(task_id: int, database: Session = Depends(db.get_db),
                         token: str = Depends(oauth2_scheme)):

    return await services.get_task_by_id(task_id, database)

app.include_router(router)

