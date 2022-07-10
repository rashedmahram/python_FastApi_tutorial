from random import randrange
from sqlite3 import Cursor
import time
from fastapi import Depends, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from requests import Session
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency

# https://fastapi.tiangolo.com/tutorial/sql-databases/


class Post(BaseModel):
    id: int = randrange(0, 1000)
    title: str
    content: str
    published: bool = True


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="15426341",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("DATABASE connetion was succesfull!")
        break
    except Exception as error:
        print("Faild connetion to database")
        print("Error ", error)
        time.sleep(2)

post_dict = [
    {
        "id": 0,
        "title": "how to start working",
        "content": "just do it fast"
    },
    {
        "id": 1,
        "title": "how to start working",
        "content": "just do it fast"
    }
]


def find_post(id):
    for item in post_dict:
        if item["id"] == id:
            return item


def find_post_index(index):
    for i, p in enumerate(post_dict):
        if p['id'] == index:
            return i


@app.get("/")
def get_posts():
    cursor.execute('''SELECT * FROM public."Post"''')
    posts = cursor.fetchall()
    print(posts)
    return posts


@app.get("/post/{id}")
def get_posts(id: int):
    cursor.execute(
        '''select * from public."Post" where id =%s''', (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post Was Not Found")
    return post


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post Was Not Found")
    #     response.status_code=status.HTTP_404_NOT_FOUND
    #     return {"message":"Post Not Found"}

    return post


@app.post("/post/create", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    # cursor.execute('''INSERT INTO public."Post"(title, content, published) VALUES (%s, %s, %s) RETURNING *;''',
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(
        title=post.title,
        content=post.content,
        published=post.published,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.delete("/post/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(
        '''DELETE FROM public."Post" WHERE id=%s returning *''', (str(id),))
    delete_post = cursor.fetchone()

    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is No Post with ID: {id}")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/post/update/{id}")
def update_post(id: int, post: Post):
    cursor.execute(''' UPDATE public."Post"
	SET  title=%s, content=%s WHERE id=%s returning *''', (post.title, post.content, str(id),))
    updated_post = cursor.fetchone()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is No Post with ID: {id}")
    conn.commit()
    return {"Data": updated_post}


@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"status": posts}


@app.get("/sqlalchemy/posts")
def get_posts_alchemy(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"status": posts}


@app.post("/alchemyslq/post")
def add_post_alchemy(posted_data: Post, db: Session = Depends(get_db)):
    # new_post = models.Post(
    #     title=posted_data.title,
    #     content=posted_data.content,
    # )
    new_post = models.Post(**posted_data.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/alchemyslq/post/{id}")
def get_post_alchemy(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post Was Not Found")
    return post


@app.delete("/alchemyslq/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is No Post with ID: {id}")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/alchemyslq/update/{id}")
def update_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(''' UPDATE public."Post"
    # SET  title=%s, content=%s WHERE id=%s returning *''', (post.title, post.content, str(id),))
    # updated_post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is No Post with ID: {id}")
    conn.commit()
    return {"Data": post}
