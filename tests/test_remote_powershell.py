import pytest
from app.controllers import RemoteShell
from config import BaseConfig as conf


@pytest.mark.skipif(not conf.REMOTE_SHELL_SERVER, reason="Remote Shell not configured")
def test_simple_ps_commands():
    sh = RemoteShell()
    res = sh.send_command("1+1")
    assert res
    assert "2" == res
