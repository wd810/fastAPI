from turtle import title
from typing import Optional
from fastapi import Depends, Response, status, HTTPException, FastAPI
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# postgre db connection
while True:
    # keep connection until success
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                password='123456', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("db connection was successful")
        break
    except Exception as error:
        print("fail at connection to postgre")
        print("Error: ", error)
        # if fails, retry after 2 seconds
        time.sleep(2)


my_posts = [{"title": "title of post 1", 'content': 'content of post 1', 'id': 1},
            {'title': 'like my post', 'content': 'like pizza', 'id': 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
async def root():
    return {"message": "welcome to my API"}

@app.get('/sqltest')
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"status": posts}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """,
                    (str(id)))
    post = cursor.fetchone()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post {id} was not found")

    return {"post detail": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):

    '''
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    '''
    # create id for post by generating a random number
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
    #              (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # save post into the db, from stage to 
    # conn.commit()
    new_post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"added": new_post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # to find the post index
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    del_post = cursor.fetchone()
    conn.commit()
    
    if not del_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %sRETURNING *""",
                    (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post {id} cannot be found for update")

    return {"data": updated_post}