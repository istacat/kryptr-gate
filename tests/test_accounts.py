import pytest

from app import db, create_app
from app.models import Account, User
from tests.utils import register, login, logout
from config import BaseConfig as config
from app.controllers.ldap import LDAP


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
        register("sam", role=User.RoleType.distributor)
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


@pytest.mark.skipif(not config.LDAP_SERVER, reason="LDAP not configured")
def test_add_delete_account(client):
    # test login required
    logout(client)
    response = client.get('/add_account')
    assert 400 > response.status_code >= 300
    login(client, "sam")
    response = client.get('/add_account')
    assert response.status_code == 200
    res = User.query.get(1)
    response = client.post('/add_account', data=dict(
        ad_password="password",
        sim="12345678901",
        ad_login=' TES345@kryptr.li',
        email='TES345@kryptr.li',
        ecc_id='TES345',
        comment="",
        reseller=res.username
    ), follow_redirects=True
    )
    assert b'Account creation successful' in response.data
    ldap = LDAP()
    users = ldap.users
    acc = Account.query.filter(Account.ecc_id == 'TES345').first()
    assert acc
    acc_mail = acc.ecc_id + "@kryptr.li"
    ldap_account = None
    for user in users:
        if user.mail == (acc_mail):
            ldap_account = user.mail
    assert ldap_account
    response = client.get("/delete_account?id=1", follow_redirects=True)
    acc = Account.query.filter(Account.ecc_id == 'TES345').first()
    ldap_account = None
    ldap = LDAP()
    users = ldap.users
    for user in users:
        if user.mail == (acc_mail):
            ldap_account = user.mail
    assert not ldap_account
    assert b'Account deletion successful' in response.data
