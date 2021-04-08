from flask.helpers import url_for
from flask_login import current_user
import pytest

from app import db, create_app
from app.models import User
from tests.utils import register, login, logout
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


def test_diff_user_role(client):
    logout(client)
    login(client, 'a', 'a')
    res = client.get(url_for("main.index"))
    assert res.status_code == 200
    assert url_for('user.index') in res.data.decode()
    res = client.get(url_for("account.index"))
    assert res.status_code == 200
    assert url_for('account.index') in res.data.decode()

    logout(client)
    login(client, 'r', 'r')
    res = client.get(url_for("main.index"))
    assert res.status_code == 200
    assert url_for('user.index') not in res.data.decode()

    res = client.get(url_for("sub_reseller.index"))
    assert res.status_code == 200
    assert url_for('sub_reseller.index') in res.data.decode()
    res = client.get(url_for("account.index"))
    assert res.status_code == 200
    assert url_for('account.index') in res.data.decode()

    logout(client)
    login(client, 'sr', 'sr')
    res = client.get(url_for("main.index"))
    assert res.status_code == 200
    assert url_for('user.index') not in res.data.decode()
    res = client.get(url_for("reseller.index"))
    assert res.status_code == 200
    assert url_for('reseller.index') not in res.data.decode()
    res = client.get(url_for("sub_reseller.index"))
    assert res.status_code == 200
    assert url_for('sub_reseller.index') not in res.data.decode()

    res = client.get(url_for("account.index"))
    assert res.status_code == 200
    assert url_for('account.index') in res.data.decode()

    logout(client)
    login(client, 's', 's')
    res = client.get(url_for("main.index"))
    assert res.status_code == 200
    assert url_for('user.index') not in res.data.decode()
    res = client.get(url_for("reseller.index"))
    assert res.status_code == 200
    assert url_for('reseller.index') not in res.data.decode()
    res = client.get(url_for("sub_reseller.index"))
    assert res.status_code == 200
    assert url_for('sub_reseller.index') not in res.data.decode()

    res = client.get(url_for("account.index"))
    assert res.status_code == 200
    assert url_for('account.index') in res.data.decode()
    res = client.get(url_for("product.index"))
    assert res.status_code == 200
    assert url_for('product.index') in res.data.decode()

    logout(client)
    login(client, 'd', 'd')
    res = client.get(url_for("main.index"))
    assert res.status_code == 200
    assert url_for('user.index') not in res.data.decode()
    res = client.get(url_for("account.index"))
    assert res.status_code == 200
    assert url_for('account.index') in res.data.decode()
    res = client.get(url_for("product.index"))
    assert res.status_code == 200
    assert url_for('product.index') not in res.data.decode()

    res = client.get(url_for("reseller.index"))
    assert res.status_code == 200
    assert url_for('reseller.index') in res.data.decode()
    res = client.get(url_for("sub_reseller.index"))
    assert res.status_code == 200
    assert url_for('sub_reseller.index') in res.data.decode()


def test_chief_subordinate(client):
    # Admin
    logout(client)
    login(client, 'a', 'a')
    dists = current_user.distributors
    assert dists
    resellers = current_user.resellers
    assert resellers
    subress = current_user.sub_resellers
    assert subress
    accs = current_user.accounts
    assert accs

    # Distributor # 1
    logout(client)
    login(client, 'd', 'd')
    dists = current_user.distributors
    assert not dists
    resellers = current_user.resellers
    assert resellers
    subress = current_user.sub_resellers
    assert subress
    accs = current_user.accounts
    assert accs

    # Distributor # 2
    logout(client)
    login(client, 'd2', 'd2')
    dists = current_user.distributors
    assert not dists
    resellers = current_user.resellers
    assert not resellers
    subress = current_user.sub_resellers
    assert not subress
    accs = current_user.accounts
    assert not accs

    # Reseller
    logout(client)
    login(client, 'r', 'r')
    dists = current_user.distributors
    assert not dists
    resellers = current_user.resellers
    assert not resellers
    subress = current_user.sub_resellers
    assert subress
    accs = current_user.accounts
    assert accs

    # Sub-reseller
    logout(client)
    login(client, 'sr', 'sr')
    dists = current_user.distributors
    assert not dists
    resellers = current_user.resellers
    assert not resellers
    subress = current_user.sub_resellers
    assert not subress
    accs = current_user.accounts
    assert accs
