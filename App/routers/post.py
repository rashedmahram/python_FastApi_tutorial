from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from ..database import get_db
from .. import models, schema
dp = Depends(get_db)

router = APIRouter(
    prefix="/post",
    tags=["posts"]
)


@router.get('/', response_model=List[schema.CreatePost])
def getPostList(db: Session = dp):
    post = db.query(models.Post).all()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post Was Not Found")
    return post


@router.get('/{id}', response_model=schema.CreatePost)
def getPost(id: int, db: Session = dp):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post Was Not Found")
    return post


@router.post('/', response_model=schema.CreatePost)
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


@router.put("/{id}", response_model=schema.Post)
def updatePost(id: int, updated_post: schema.UpdatePost, db: Session = dp, ):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post Was Not Found")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
# Create User
