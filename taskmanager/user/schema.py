from pydantic import BaseModel, constr, EmailStr

class UserCreate(BaseModel):
    name: constr(min_length=2, max_length=50)
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True