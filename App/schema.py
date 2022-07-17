from datetime import datetime
from pydantic import BaseModel


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

# Response


class Post(CreatePost):
    id: int
    # for the error that says its not dict

    class Config:
        orm_mode = True
