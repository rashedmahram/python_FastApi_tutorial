from turtle import title
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, status
from .database import engine, get_db
from . import models, schema


models.Base.metadata.create_all(bind=engine)
dp = Depends(get_db)
app = FastAPI()
# Model[X]
# [X]databse

# Schema

# Functions
# []get data
# []add,update,delete


# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()


@app.get('/', response_model=List[schema.CreatePost])
def getPostList(db: Session = dp):
    post = db.query(models.Post).all()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post Was Not Found")
    return post


@app.get('/{id}', response_model=schema.CreatePost)
def getPost(id: int, db: Session = dp):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post Was Not Found")
    return post


@app.post('/', response_model=schema.CreatePost)
def addPost(data: schema.CreatePost, db: Session = dp):
    db_post = models.Post(
        title=data.title,
        content=data.content,
        published=data.published
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@app.put("/{id}", response_model=schema.Post)
def updatePost(id: int, updated_post: schema.UpdatePost, db: Session = dp, ):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post Was Not Found")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
