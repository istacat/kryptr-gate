import pytest
from config import BaseConfig as config
from app.controllers.ldap import LDAP


@pytest.mark.skipif(not config.LDAP_SERVER, reason="LDAP not configured")
def test_ldap_add_delete_user():
    ldap = LDAP()
    TEST_USER_NAME = "TST001"
    ldap.delete_user(TEST_USER_NAME)
    user = ldap.add_user(TEST_USER_NAME)
    assert user
    res = ldap.delete_user(TEST_USER_NAME)
    assert res
    users = ldap.users
    assert users


@pytest.mark.skipif(not config.LDAP_SERVER, reason="LDAP not configured")
@pytest.mark.skipif(
    not config.REMOTE_SHELL_SERVER, reason="Remote Shell not configured"
)
def test_change_user_password():
    ldap = LDAP()
    TEST_USER_NAME = "TST001"
    ldap.delete_user(TEST_USER_NAME)
    user = ldap.add_user(TEST_USER_NAME)
    assert user
    error_message = user.reset_password("Simple2B123")
    assert not error_message
    error_message = user.reset_password("bubu")
    assert error_message
