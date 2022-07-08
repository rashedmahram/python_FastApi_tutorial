from random import randrange
from turtle import pos
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel


app = FastAPI()


class Post(BaseModel):
    id: int = randrange(0, 1000)
    title: str
    content: str
    auther: Optional[str] = "Tashil"


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
    return post_dict


@app.get("/posts")
def get_posts():
    return post_dict


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
def create_post(post: Post):
    new_post = post.dict()
    post_dict.append(new_post)
    return post_dict


@app.delete("/post/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # remove form array
    index = find_post_index(index=id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is No Post with ID: {id}")

    post_dict.pop()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/post/update/{id}")
def update_post(id: int, post: Post):
    index = find_post_index(index=id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is No Post with ID: {id}")
    update_data = post.dict()
    update_data["id"] = id
    post_dict[index] = update_data
    return {"Data": update_data}
