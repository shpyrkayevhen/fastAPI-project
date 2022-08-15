from turtle import st
from venv import create
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# DEFIND HERE WHICH DATA WE WANT TO RECIEVE AND SEND


# AS A FORM FROM FRONT END OR BODY FROM HTTP REQUEST
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


# INHERITING PostBase CLASS
class PostCreate(PostBase):
    pass


# REPRESENT OBJ HTTP RESPONSE (WITHHOUT DATA id AND published)
class Post(PostBase):
    # title: str             # INHERED THIS DATA
    # content: str           # INHERED THIS DATA
    created_at: datetime

    # ALWAYS DO THIS
    class Config():
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config():
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
