from datetime import datetime, timedelta
from fastapi import FastAPI

from fastapi.security import OAuth2PasswordBearer
import jwt
from fastapi.middleware.cors import CORSMiddleware
import schema

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import db
import hash
from models import User


SECRET_KEY = "costamaadadadwadwa"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schema.TokenData(email=email)
        return token_data
    except jwt.PyJWTError:
        raise credentials_exception


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(data, credentials_exception)

app = FastAPI(title="Task Management System", description="A simple API", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://user:8000","http://localhost:8000","http://task:8003",
                   "http://localhost:8003","http://auth:8001","http://localhost:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


router = APIRouter(
    tags=['auth'],
    prefix='/auth'
)


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), database: Session = Depends(db.get_db)):
    user = database.query(User).filter(User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Credentials')
    if not hash.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid Password')

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/verify-token")
def verify_token_endpoint(token: str, credentials_exception: HTTPException = Depends()):
    try:
        return verify_token(token, credentials_exception)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid or expired")

app.include_router(router)