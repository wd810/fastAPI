from datetime import date, datetime
from turtle import st
from pydantic import BaseModel, EmailStr
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

# define response data format for users
class Post(PostBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr # validate email
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None