from turtle import title
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models



SQLALCHEMY_DATEBASE_URL = 'postgresql://postgres:123456@localhost:5432/fastapi_test'
#SQLALCHEMY_DATEBASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# engine: connect to the database
engine = create_engine(SQLALCHEMY_DATEBASE_URL)
# use a session to talk
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def overrid_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = overrid_get_db
    yield TestClient(app)


'''
make every test function independently
'''
@pytest.fixture
def test_user(client):
    user_data = {"email": "test_login@123.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({'user_id': test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def get_test_posts(test_user, session):
    posts_data = [
        {
            "title": "1st post",
            "content": "I love CA",
            "owner_id": test_user['id']
        },
        {
            "title": "2nd post",
            "content": "I love Busan",
            "owner_id": test_user['id']
        },
        {
            "title": "3rd post",
            "content": "I love So",
            "owner_id": test_user['id']
        },
    ]


    def create_post_model(post):
        return models.Post(**post)

    posts_map = map(create_post_model, posts_data)
    # convert map to list
    posts = list(posts_map)

    # add all posts to db
    session.add_all(posts)
    # session.add_all([models.Post(title="1 post", content="i love ca", owner_id=test_user['id']),
    #                 models.Post(title="2 post", content="i love busan", owner_id=test_user['id']),
    #                 models.Post(title="3 post", content="i love sl", owner_id=test_user['id'])])

    session.commit()
    return session.query(models.Post).all()