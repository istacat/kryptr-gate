import pytest

from app import db, create_app
from app.models import User
from tests.utils import register, login, logout


@pytest.fixture
def client():
    app = create_app(environment="testing")
    app.config["TESTING"] = True

    with app.test_client() as client:
        app_ctx = app.app_context()
        app_ctx.push()
        db.drop_all()
        db.create_all()
        register("sam")
        yield client
        db.session.remove()
        db.drop_all()
        app_ctx.pop()


def test_users(client):
    response = client.get('/users')
    assert 400 > response.status_code >= 300
    login(client, "sam")
    response = client.get('/users')
    assert response.status_code == 200


def test_add_user(client):
    # test login required
    logout(client)
    response = client.get('/add_user')
    assert 400 > response.status_code >= 300
    login(client, "sam")
    response = client.get('/add_user')
    assert response.status_code == 200
    response = client.post('/add_user', data=dict(
        username="man",
        email="man@email.com",
        password="password",
        activated=User.StatusType.active.name,
        role=User.RoleType.admin.name
    ), follow_redirects=True)

    assert b'User creation successful' in response.data
