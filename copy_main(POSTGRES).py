from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body, Depends
from pydantic import BaseModel, dataclasses
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

##sql alchemy imports
from .database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
from . import models

models.Base.metadata.create_all(bind=engine)




while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='12345', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database connection successful")
        break
    except Exception as error:
        print("connection to database failed")
        print("error: ", error)
        time.sleep(2)


class post(BaseModel):
    title: str
    content: str
    published: bool = True #default value to True

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, 
            {"title": "ninja hattori", "content":"smacks kenechi's girlfriend", "id":2}]

def find_post(id):
    for i in my_posts:
        if i["id"] == id:
            return i
            break

def return_index(id):
    for i, post in enumerate(my_posts):
        if post["id"] == id:
            return i
    return None

app = FastAPI() ##app instance


@app.get("/sqlalchemy")
def sql_test(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    return {"details" : post}

@app.get("/")
def root():
    return {"social features": """/docs to get all the features
    """}

@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts;")
    posts = cursor.fetchall()
    return {"posts:": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: post): #dict = Body(...) --> if you're passing through the postman body 
    #print(post)
    #print((post.dict())) #to convert the basemodel schema into dictionary
    #as we're not using database, so for now we'll use random numbers
    #post_dict = post.dict()
    #post_dict['id'] = randrange(0,1000000000)
    #my_posts.append(post_dict)
    cursor.execute("""INSERT INTO posts (title, content, is_published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    new_post = cursor.fetchall()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/latest")
def get_latest_post():
    cursor.execute("""SELECT * FROM posts ORDER BY id DESC LIMIT 1;""")
    #latest_post = my_posts[len(my_posts) - 1]
    latest_post = cursor.fetchone()
    return {"latest post": latest_post}



@app.get("/posts/{id}")
def get_post(id: int, Response: Response):
    cursor.execute("""Select * From Posts WHERE id = %s ;""", (str(id),)) #this comma sometimes solves weird argumental errors
    post_one = cursor.fetchone()
    if not post_one:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"404: post with id {id} not found")  
    return {"the post": post_one}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", ((str(id)),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"404: post with id {id} not found")
    
    #return {"after deletion": "post succesfuly deleted"} #when we send a 204 request we should not return any data
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, is_published = %s WHERE id = %s RETURNING *""", 
                    ((post.title, post.content, post.published, str(id))))
    
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"404: post with id {id} not found")

    return {"updated data": updated_post}

    