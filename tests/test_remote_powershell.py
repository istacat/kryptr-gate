from app.controllers import RemoteShell


def test_simple_ps_commands():
    sh = RemoteShell()
    res = sh.send_command("1+1")
    assert res
    assert "2" == res
