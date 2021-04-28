import pytest
from datetime import datetime

from app import db, create_app
from app.models import Account, User, Subscription
from tests.utils import register, login, logout
from config import BaseConfig as config
from app.controllers.ldap import LDAP


TEST_ACC_NAME = "Test Account 01"
TEST_ACC_LOGIN = "TES345@kryptr.li"


@pytest.fixture
def client():
    app = create_app(environment="testing")
    app.config["TESTING"] = True

    with app.test_client() as client:
        app_ctx = app.app_context()
        app_ctx.push()
        db.drop_all()
        db.create_all()
        register("sam", role=User.RoleType.admin)
        yield client
        db.session.remove()
        db.drop_all()
        app_ctx.pop()


def test_accounts(client):
    response = client.get("/accounts")
    assert 400 > response.status_code >= 300
    login(client, "sam")
    response = client.get("/accounts")
    assert response.status_code == 200


def test_add_delete_account(client):
    # test login required
    logout(client)
    response = client.get("/add_account")
    assert 400 > response.status_code >= 300
    login(client, "sam")
    response = client.get("/add_account")
    assert response.status_code == 200
    reseller = User.query.first()
    ECC_ID = "TES1478"

    response = client.post(
        "/add_account",
        data=dict(
            ad_password="Simple2B123",
            license_key="lis_key_value",
            sim="12345678901",
            imei="",
            ad_login=ECC_ID,
            email=f"{ECC_ID}@kryptr.li",
            ecc_id=ECC_ID,
            ecc_password="Testing321",
            comment="",
            reseller=reseller.username,
        ),
        follow_redirects=True,
    )
    assert b"Account creation successful" in response.data
    acc = Account.query.filter(Account.ecc_id == ECC_ID).first()
    assert acc
    acc_mail = acc.ecc_id + "@kryptr.li"
    if config.LDAP_SERVER:
        AD_user_mails = [u.mail for u in LDAP().users]
        assert acc_mail in AD_user_mails

    response = client.get("/delete_account/1", follow_redirects=True)
    assert b"Account deletion successful" in response.data
    acc = Account.query.filter(Account.ecc_id == ECC_ID).first()
    assert acc
    assert acc.deleted

    if config.LDAP_SERVER:
        AD_user_mails = [u.mail for u in LDAP().users]
        assert acc_mail not in AD_user_mails


@pytest.mark.skipif(not config.LDAP_SERVER, reason="LDAP not configured")
def test_edit_account(client):
    # test get method
    login(client, "sam")
    TEST_EMAIL = "TST001@kryptr.li"
    TEST_PASS = "ZAQ!xsw2"
    TEST_USER_NAME = "TST0001"
    reseller = User.query.filter(User.username == "sam").first()
    assert reseller
    acc = Account(
        ecc_id=TEST_USER_NAME,
        ecc_password=TEST_PASS,
        ad_login=TEST_USER_NAME,
        ad_password=TEST_PASS,
        license_key="",
        email=TEST_EMAIL,
        reseller=reseller,
    )
    acc.save()
    Subscription(
        activation_date=datetime.now(),
        type='new',
        months=6,
        account_id=acc.id
    ).save()
    ACC_ID = acc.id
    response = client.get(f"/edit_account/{ACC_ID}")
    assert response.status_code == 200

    # send post request for change password
    NEW_PASS = "XSW@cde3"
    # NEW_PASS = TEST_PASS
    data = {
        "id": ACC_ID,
        "ecc_id": acc.ecc_id,
        "email": acc.email,
        "ad_login": acc.ad_login,
        "ad_password": NEW_PASS,
        "sim": acc.sim,
        "comment": acc.comment,
        "reseller": reseller.username,
        "ecc_password": NEW_PASS
    }
    response = client.post(f"/edit_account/{ACC_ID}", data=data)
    assert response.status_code == 302
    acc = Account.query.get(ACC_ID)
    assert acc.ecc_password == NEW_PASS
