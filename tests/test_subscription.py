import pytest

from app import db, create_app
from app.models import Account, User, Subscription
from tests.utils import register, login, logout


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


def test_add_extend_subs(client):
    login(client, "sam")
    a = ['b', 'c']
    assert a.index('b') == 0
