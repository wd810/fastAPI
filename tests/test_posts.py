import pytest
from app import schema

def test_get_all_posts(authorized_client, get_test_posts):
    res = authorized_client.get('/posts/')

    def validate(post):
        return schema.PostOut(**post)
    
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    assert len(res.json()) == len(get_test_posts)
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client, get_test_posts):
    res = client.get('/posts')
    assert res.status_code == 401

def test_unauthorized_user_get_one_posts(client, get_test_posts):
    res = client.get(f'/posts/{get_test_posts[0].id}')
    assert res.status_code == 401

def test_get_post_not_exist(authorized_client):
    res = authorized_client.get("/posts/9999")
    assert res.status_code == 404

def test_get_one_post(authorized_client, get_test_posts):
    res = authorized_client.get(f'/posts/{get_test_posts[0].id}')
    print(res.json())

    post = schema.PostOut(**res.json())
    assert post.Post.id == get_test_posts[0].id


@pytest.mark.parametrize("title, content, published", [
    ("i love ca", "i love busan", True),
    ("i love ca", "i love busan", False),
    ("i love ca", "i love busan", True),
])
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post('/posts/', json={"title": title, "content": content, "published": published})

    created_post = schema.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


def test_create_post_default_published_true(authorized_client, test_user):
    res = authorized_client.post('/posts/',
                                json={"title": "new title", "content": "new content"})

    created_post = schema.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == "new title"
    assert created_post.content == "new content"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']


def test_unauthorized_user_create_post(client, test_user, get_test_posts):
    res = client.post("/posts/",
                     json={"title": "arbitrary title", "content": "arbitrary content"})
    assert res.status_code == 401


def test_unauthorzied_user_delete_post(client, test_user, get_test_posts):
    res = client.delete(f"/posts/{get_test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_user, get_test_posts):
    res = authorized_client.delete(f"/posts/{get_test_posts[0].id}")
    assert res.status_code == 204


def test_delete_post_not_exist(authorized_client, test_user, get_test_posts):
    res = authorized_client.delete("/posts/999999")
    assert res.status_code == 404

