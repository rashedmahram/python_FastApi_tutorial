from os import access
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from .. import schema, models, utils, Oauth2
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from App.database import get_db
router = APIRouter(
    prefix="/auth",
    tags=["Authentications"]
)


@router.post('/login', response_model=schema.Token)
async def loginFun(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(
        models.User.email == user_credential.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="No Valid Data NO Users")

    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="invalid Credentials not verifyed")

    access_token = Oauth2.create_access_token(
        data={"user_id": user.id}
    )
    return {"access_token": access_token, "token_type": "bearer"}
