from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, schemas, models, utils, oauth2
from . import user
from sqlalchemy.orm import Session
from ..database import SessionLocal, engine, get_db

router = APIRouter(tags=['Authentication'])

""""def Pass(db: Session = Depends(get_db), id = 1):
    hash = db.query(models.user.password).filter(models.user.email == "dev@gmail.com")
    admin = verify("dev@787", hash)
    return admin"""

@router.post("/login") #OAuth2PasswordRequestForm is a dependency which just makes the input validation in the request forms instead of raw data
def login( user_credentials : schemas.adminlogin, db:session = Depends(database.get_db)): #user_credentials : schemas.userlogin we can use this to pass through raw data

    user = db.query(models.user).filter(user_credentials.email == models.user.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"invalid credentials") 

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"invalid credentials")

    access_token = oauth2.Access_tokens(data= {"user_id": user.id})
    
    return {"access_token":access_token, "token_type": "bearer"}