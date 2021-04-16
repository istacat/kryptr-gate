import pytest
from app.controllers import generate_password
from app.models import Account

from app import db, create_app


@pytest.fixture
def client():
    app = create_app(environment="testing")
    app.config["TESTING"] = True

    with app.test_client() as client:
        app_ctx = app.app_context()
        app_ctx.push()
        db.drop_all()
        db.create_all()
        yield client
        db.session.remove()
        db.drop_all()
        app_ctx.pop()


def test_generators(client):
    password = generate_password()
    assert password
    assert len(password) == 8
    ecc_id = Account.gen_ecc_id()
    assert ecc_id
    assert len(ecc_id) == 7
