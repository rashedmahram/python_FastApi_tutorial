from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, status
from ..database import engine, get_db
from .. import models, schema, utils
dp = Depends(get_db)
app = FastAPI()


@app.get("/user/{id}", response_model=schema.UserCreateRE)
def get_user(id: int, db: Session = dp):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status=status.HTTP_404_NOT_FOUND,
                            detail=f"User With id {id} does not exict")
    return user
