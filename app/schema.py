from datetime import datetime
from turtle import st
from pydantic import BaseModel, EmailStr

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