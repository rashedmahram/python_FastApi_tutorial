from fastapi import Depends, FastAPI, Response, status, HTTPException, Depends

# from requests import Session

from . import schema
from .models import Post
from .database import get_db
from sqlalchemy.orm import Session
app = FastAPI()

# Dependency

# https://fastapi.tiangolo.com/tutorial/sql-databases/


@app.get("/post/{id}")
def get_post_alchemy(id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post Was Not Found")
    return post


@app.post('/create')
def create_post(data=Post, db: Session = Depends(get_db)):
    db.execute(Post)
    return {"", ""}


@app.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is No Post with ID: {id}")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/update/{id}", response_model=schema.Post)
def update_post(post_data: schema.BaseModel, id: int, db: Session = Depends(get_db)):
    post_query = db.query(post_data).where(Post.id == id)
    data = post_query.first()
    if data == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is No Post with ID: {id}")
    post_query.update(post_data.dict(), synchronize_session=False)
    db.commit()
    return {"Data": post_query.first()}
