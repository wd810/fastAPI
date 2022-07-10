from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# specify database connection string
# string format: postgresql://<username>:<password>@<ip_address/hostname>/<database_name>
SQLALCHEMY_DATEBASE_URL = 'postgresql://postgres:123456@localhost/fastapi'

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