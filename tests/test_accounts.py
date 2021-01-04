import pytest

from app import db, create_app
from app.models import Account
from tests.utils import register, login, logout

TEST_ACC_NAME = "Test Account 01"


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


def test_accounts(client):
    response = client.get('/accounts')
    assert 400 > response.status_code >= 300
    login(client, "sam")
    response = client.get('/accounts')
    assert response.status_code == 200


def test_add_account(client):
    # test login required
    logout(client)
    response = client.get('/add_account')
    assert 400 > response.status_code >= 300
    login(client, "sam")
    response = client.get('/add_account')
    assert response.status_code == 200
    response = client.post('/add_account', data=dict(
        name=TEST_ACC_NAME,
        ecc_id="ECC001",
        ad_login="test01@kryptr.li",
        ad_password="password",
        license_key="lis_key_value",
        email="test01@kryptr.li",
        sim="12345678901",
        imei="",
        comment=""
    ), follow_redirects=True)

    assert b'Account creation successful' in response.data
    acc = Account.query.filter(Account.name == TEST_ACC_NAME).first()
    assert acc
