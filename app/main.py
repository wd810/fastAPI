
from turtle import pos
from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schema, utils
from .database import engine, get_db
from .routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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


app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
async def root():
    return {"message": "welcome to my API"}




