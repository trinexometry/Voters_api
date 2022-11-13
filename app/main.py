from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
import time
from random import randrange
from typing import List

import psycopg2
from fastapi.params import Body, Depends
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel, dataclasses
from sqlalchemy import update
from .database import SessionLocal, engine, get_db

from . import models, schemas

from .routers import Voter, user, auth
import json
    #cursor.execute("""INSERT INTO posts (title, content, is_published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    #new_post = cursor.fetchall()
    #conn.commit()
j = open("data.json")

data = json.load(j)



##sql alchemy imports



models.Base.metadata.create_all(bind=engine)



while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='12345', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database connection successful for main")
        break
    except Exception as error:
        print("connection to database failed")
        print("error: ", error)
        time.sleep(2)

app = FastAPI() ##app instance
@app.get("/loaddata", status_code=status.HTTP_201_CREATED)
def load_data():
    for v in data.values():
        print(type(v))
        for i in v:
            cursor.execute (""" INSERT INTO  "voters" (epic_no, name, age, father_name, husband_name, sex, house_no, poll_booth, district, state) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;""", (i["Epic_no"], i["Name"], str(i["age"]), i["father_name"], i["husband_name"], i["sex"],  i["house_no"], i["poll_booth"], i["district"], i["state"]))
            new_entry = cursor.fetchone()
            conn.commit()
        

    j.close()




    
app.include_router(Voter.router)
app.include_router(user.router)
app.include_router(auth.router)