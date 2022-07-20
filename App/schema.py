from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool

    class Config:
        orm_mode = True


class CreatePost(PostBase):
    pass


class UpdatePost(PostBase):
    pass


class Post(PostBase):
    owner_id: int


class UserCreateRE(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class Posts(PostBase):
    id: int
    owner_id: int
    owner: UserCreateRE


# USER ACOUNTS
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    # hashed_password: str

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: str
    password: str

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


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
