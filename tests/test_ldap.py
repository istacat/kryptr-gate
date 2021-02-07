import pytest
from config import BaseConfig as config
from app.controllers.ldap import LDAP


@pytest.mark.skipif(not config.LDAP_SERVER, reason="LDAP not configured")
def test_ldap_add_delete_user():
    ldap = LDAP()
    TEST_USER_NAME = "TST001"
    ldap.delete_user(TEST_USER_NAME)
    user = ldap.add_user(TEST_USER_NAME, "ZAQ!xsw2")
    assert user
    res = ldap.delete_user(TEST_USER_NAME)
    assert res
    users = ldap.users
    assert users
