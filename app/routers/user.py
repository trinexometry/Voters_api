from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from .. import utils, models, schemas
from ..database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix= "/users",
    tags=['USERS']
) 

########CREATE USER#################
@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.userresponse)
def user(user: schemas.userlogin, db: Session = Depends(get_db)):
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = models.user(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
 
    return new_user


#################### GET USER BY ID ##################################
@router.get("/{id}", response_model=schemas.userresponse)
def get_user(id: int, Response: Response, db: Session = Depends(get_db)):
    user = db.query(models.user).filter(models.user.id == id).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"404: post with id {id} not found")  
    return  user