from .database import client, session
from app import schema


def test_root(client):
    res = client.get("/")
    print(res.json)
    assert res.json().get('message') == 'welcome to my API'
    assert res.status_code == 200



def test_creat_user(client):
    res = client.post("/users/", json={"email": "hello@456.com", "password": "pass1123"})
    
    test_user = schema.UserOut(**res.json())
    assert test_user.email == "hello@456.com"
    assert res.status_code == 201