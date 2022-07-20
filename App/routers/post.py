from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status, Response
from ..database import get_db
from .. import models, schema, Oauth2
dp = Depends(get_db)

router = APIRouter(
    prefix="/post",
    tags=["Posts"]
)


@router.get('/', response_model=List[schema.Posts])
def getPostList(db: Session = dp, limit: int = 2, skip: int = 2, search: Optional[str] = ""):
    post = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post Was Not Found")
    return post


@router.get('/myPosts')
def myPosts(db: Session = dp, current_user: int = Depends(Oauth2.get_current_user)):
    print(current_user.id)
    post = db.query(models.Post).filter(
        models.Post.owner_id == current_user.id).all()
    return post


@router.get('/{id}', response_model=schema.CreatePost)
def getPost(id: int, db: Session = dp, current_user: int = Depends(Oauth2.get_current_user), limit: int = 1):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Ther is No Post Found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not allowed To See")
    return post


@router.post('/create', response_model=schema.Post)
def addPost(data: schema.CreatePost, db: Session = dp, current_user: int = Depends(Oauth2.get_current_user)):
    print(current_user.id, end="\n \n \n")
    db_post = models.Post(
        owner_id=current_user.id,
        **data.dict()
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.put("/update/{id}", response_model=schema.Post,)
def updatePost(
        id: int,
        updated_post: schema.UpdatePost,
        db: Session = dp,
        current_user: int = Depends(Oauth2.get_current_user)
):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post Was Not Found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"cant update post with id:{id} not allowed")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


@router.delete("/delete/{id}")
def deletePost(id: int, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"post with id:{id} Does not exits")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"current user:{id} Does not exits")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
