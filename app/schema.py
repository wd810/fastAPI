from datetime import date, datetime
from turtle import st
from pydantic import BaseModel, EmailStr, conint
from typing import Optional

# define response data format for users
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


'''
posts
'''
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
class PostCreate(PostBase):
    pass
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int
    class Config:
        orm_mode = True
'''
token
'''
class Token(BaseModel):
    access_token: str
    token_type: str
    class Config:
        orm_mode = True

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)  # 1: vote; 0: delete