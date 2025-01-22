from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from schema import Notification
from services import task_notifications_store, consumer
from typing import List
from fastapi import APIRouter

app = FastAPI(title="Task Management System", description="A simple API", version="1.0")

router = APIRouter(
    tags=['Notifications'],
    prefix='/notification'
)

@router.get('/task', response_model=List[Notification])
async def get_task_notifications():
    return task_notifications_store


@router.on_event("shutdown")
def shutdown_event():
    consumer.close()

app.include_router(router)

