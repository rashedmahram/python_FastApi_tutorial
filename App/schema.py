from datetime import datetime
from typing import Union
from pydantic import BaseModel, EmailStr


class CreatePost(BaseModel):
    title: str
    content: str
    published: bool

    class Config:
        orm_mode = True


class UpdatePost(BaseModel):
    title: str
    content: str
    published: bool

    class Config:
        orm_mode = True


class Post(CreatePost):
    id: int
    # for the error that says its not dict

    class Config:
        orm_mode = True
# USER ACOUNTS


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    # hashed_password: str


class UserCreateRE(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Hashing
        """_summary_
        
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class UserInDB(UserCreate):
    hashed_password: str


class USER(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime
"""
