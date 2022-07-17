from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

# specify database connection string
# string format: postgresql://<username>:<password>@<ip_address/hostname>/<database_name>
SQLALCHEMY_DATEBASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# engine: connect to the database
engine = create_engine(SQLALCHEMY_DATEBASE_URL)
# use a session to talk
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# base class / model
Base = declarative_base()

# dependency: create session to db every time call
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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