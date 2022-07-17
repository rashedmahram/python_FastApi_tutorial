from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from ..database import get_db
from .. import models, schema, utils

router = APIRouter(
    prefix="/user",
    tags=["users"]
)


@router.post("/", response_model=schema.UserCreateRE)
def addUser(user: schema.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schema.UserCreateRE)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status=status.HTTP_404_NOT_FOUND,
                            detail=f"User With id {id} does not exict")
    return user
