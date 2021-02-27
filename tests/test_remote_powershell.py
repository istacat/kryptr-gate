import pytest
from app.controllers import RemoteShell
from config import BaseConfig as conf


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
