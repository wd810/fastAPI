from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine
from .routers import post, user, auth

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
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "welcome to my API"}




