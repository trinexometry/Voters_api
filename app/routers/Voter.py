from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from .. import utils, models, schemas, oauth2
from ..database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
from ..database import SessionLocal, engine, get_db
import time


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='12345', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database connection successful for voter")
        break
    except Exception as error:
        print("connection to database failed")
        print("error: ", error)
        time.sleep(2)


router = APIRouter(
    prefix="/voter",
    tags=['voter']
)
############################# GET POSTS ########################################
@router.post("/get_Data")
async def get_voters(epic : schemas.epic , db: Session = Depends(get_db)):
    """cursor.execute("SELECT * FROM posts;")
    posts = cursor.fetchall()"""
    posts = db.query(models.votes).filter(models.votes.epic_no == epic.epic_no)
    if not posts:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"invalid credentials") 
    return posts.all()

############################## CREATE POST ###############################
@router.post("/post",status_code=status.HTTP_201_CREATED)
def create_voter(voter: schemas.voter, db: Session = Depends(get_db), auth: int = Depends(oauth2.get_current_user)): 
    cursor.execute (""" INSERT INTO  "voters" (epic_no, name, age, father_name, husband_name, sex, house_no, poll_booth, district, state) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;""", (voter.Epic_no, voter.name, voter.age, voter.father_name, voter.husband_name, voter.sex, voter.house_no, voter.poll_booth, voter.district, voter.state))
    new_post = cursor.fetchall()
    conn.commit()
    return new_post

######################## LATEST POST BY POSTGRES ###########################
"""@app.get("/posts/latest")
def get_latest_post():
    cursor.execute(""""SELECT * FROM posts ORDER BY id DESC LIMIT 1;"""") #use 3 quotes here
    #latest_post = my_posts[len(my_posts) - 1]
    latest_post = cursor.fetchone()
    return latest_post"""


############################### DELETE POST ########################################
@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(epic: schemas.epic, db: Session = Depends(get_db),auth: int = Depends(oauth2.get_current_user) ):
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", ((str(id)),))
    #deleted_post = cursor.fetchone()
    #conn.commit()

    deleted_post = db.query(models.votes).filter(models.votes.epic_no == epic.epic_no)
    if deleted_post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"404: voter not found")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

