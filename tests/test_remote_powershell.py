import pytest
import random
from app import db, create_app
from tests.db_data import fill_test_data
from app.controllers.ssh_ps import RemoteShell, RemoteMatrix
from app.models import Account
from config import BaseConfig as conf


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


@pytest.mark.skipif(not conf.REMOTE_SHELL_SERVER, reason="Remote Shell not configured")
def test_simple_ps_commands():
    sh = RemoteShell()
    res = sh.exec_command("1+1")
    assert res
    assert "2" == res


@pytest.mark.skipif(not conf.REMOTE_SHELL_SERVER, reason="Remote Shell not configured")
def test_change_user_password():
    sh = RemoteShell()
    DN = "CN=Account CYF787,CN=Users,DC=kryptr,DC=li"
    PASSWD = "Simple2B123"
    res = sh.send_command(
        " ".join(
            [
                "Set-ADAccountPassword",
                f"-Identity '{DN}'",
                "-Reset",
                "-NewPassword",
                f"(ConvertTo-SecureString -AsPlainText '{PASSWD}' -Force)",
            ]
        )
    )
    assert res

    # bad password
    PASSWD = "pass"
    res = sh.send_command(
        " ".join(
            [
                "Set-ADAccountPassword",
                f"-Identity '{DN}'",
                "-Reset",
                "-NewPassword",
                f"(ConvertTo-SecureString -AsPlainText '{PASSWD}' -Force)",
            ]
        )
    )
    assert res


@pytest.mark.skipif(not conf.MATRIX_SERVER_HOST_NAME, reason="Remote Shell not configured")
def test_simple_bash_commands(client):
    number = random.randint(111, 999)
    acc = Account(
        ecc_id=f'SAD{number}',
        ad_login='acc2',
        ad_password='123abc',
        email='testing1@gmail.com',
        reseller_id=3
    ).save()
    bash = RemoteMatrix()
    res1 = bash.add_user(acc)
    assert res1
    res2 = bash.add_user(acc)
    assert not res2
