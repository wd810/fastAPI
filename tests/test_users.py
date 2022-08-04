import pytest
from jose import jwt
from app import schema
from app.config import settings


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



def test_creat_user(client):
    res = client.post("/users/", json={"email": "hello@456.com", "password": "pass1123"})
    
    test_user = schema.UserOut(**res.json())
    assert test_user.email == "hello@456.com"
    assert res.status_code == 201



def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schema.Token(**res.json())
    payload = jwt.decode(login_res.access_token, 
                         settings.secret_key, 
                         algorithms=[settings.algorithm])
    id: str = payload.get("user_id")
    assert res.status_code == 200
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemial@123.com', 'password123', 403),
    ('wrongemial@123.com', 'wrongpassword', 403),
    ('hello@456.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('hello@456.com', None, 422),
])
def test_incorrect_login(client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})

    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid credentials.'