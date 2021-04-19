import pytest

from app import db, create_app
from app.models import Account
from app.controllers.account import create_qrcode
from tests.utils import login, logout
from tests.db_data import fill_test_data


@pytest.fixture
def client():
    app = create_app(environment="testing")
    app.config["TESTING"] = True

    with app.test_client() as client:
        app_ctx = app.app_context()
        app_ctx.push()
        db.drop_all()
        db.create_all()
        fill_test_data()
        yield client
        db.session.remove()
        db.drop_all()
        app_ctx.pop()


def test_qrcode(client):
    logout(client)
    login(client, "a", "a")
    acc = Account.query.get(1)
    qrcode = create_qrcode(acc)
    assert qrcode
    assert qrcode.size == (570, 570)
    response = client.get("/qrcode/1")
    assert response
    assert response.status_code == 200
    assert len(response.data) > 50000
    logout(client)
    login(client, "d2", "d2")
    response = client.get("/qrcode/1")
    assert response.status_code == 302
    assert (
        'You should be redirected automatically to target URL: <a href="/accounts">/accounts</a>'
        in response.data.decode()
    )
