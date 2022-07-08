from typing import Optional
from fastapi import Response, status, HTTPException, FastAPI
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

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

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM post""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post {id} was not found")

    return {"post detail": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # create id for post by generating a random number
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"added": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # to find the post index
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post {id} does not exist")

    my_posts.pop(index)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post {id} cannot be found for update")

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict

    return {"data": post_dict}