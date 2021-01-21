import datetime
import ldap3
from ldap3 import (
    HASHED_SALTED_SHA, MODIFY_REPLACE
)
from ldap3.utils.hashed import hashed
from ldap3.extend.microsoft.addMembersToGroups import ad_add_members_to_groups as addUsersInGroups
from ldap3.extend.microsoft.unlockAccount import ad_unlock_account

from config import BaseConfig as config
from app.logger import log
from .user import User


class LDAP(object):
    FORMAT_USER_DN = "CN=Account {0},CN=Users,DC=kryptr,DC=li"

    def __init__(self):
        self.LDAP_URI = f'ldap://{config.LDAP_SERVER}'
        self.search_filter = "(&(objectClass=*)(sAMAccountName=*)(sn=*))"
        self.attrs = ['*']
        self.server = ldap3.Server(self.LDAP_URI, get_info=ldap3.ALL)
        # self.connection = ldap3.Connection(self.server, user=config.LDAP_USER, password=config.LDAP_PASS)

    @property
    def users(self):
        with ldap3.Connection(self.server, user=config.LDAP_USER, password=config.LDAP_PASS) as connection:
            connection.search(config.AD_NAME, self.search_filter, attributes=self.attrs)
            return [User(entry) for entry in connection.entries]

    def add_user(self, name, passwd, product="Gold"):
        user_dn = self.FORMAT_USER_DN.format(name)
        group_dn = f"CN=Kryptr_{product},DC=kryptr,DC=li"
        with ldap3.Connection(self.server, user=config.LDAP_USER, password=config.LDAP_PASS) as connection:
            # perform the Add operation
            success = connection.add(
                dn=user_dn,
                object_class=[
                    "top",
                    "person",
                    "organizationalPerson",
                    "user"
                ],
                attributes={
                    'sn': name,
                    'givenName': 'Account',
                    'mail': f'{name}@kryptr.li',
                    "name": f"Account {name}",
                    "userPrincipalName": f'{name}@kryptr.li',
                    "sAMAccountName": name,
                    "accountExpires": datetime.datetime(2222, 1, 1),
                    "displayName": f"Account {name}",
                }
            )

            if not success:
                log(log.ERROR, 'Cannot add user [%s]', user_dn)
                log(log.ERROR, "%s", connection.result)
                return None

            success = ad_unlock_account(connection, user_dn)
            if not success:
                log(log.ERROR, 'Cannot unlock [%s]', user_dn)
                log(log.ERROR, "%s", connection.result)
                return None

            # Set password
            hashed_password = hashed(HASHED_SALTED_SHA, passwd)
            changes = {
                'userPassword': [(MODIFY_REPLACE, [hashed_password])],
                'userAccountControl': [(MODIFY_REPLACE, '66080')],
            }
            success = connection.modify(user_dn, changes=changes)
            if not success:
                log(log.ERROR, 'Unable to change password for [%s]', user_dn)
                log(log.ERROR, "%s", connection.result)
                return None

            success = addUsersInGroups(connection, user_dn, group_dn)
            if not success:
                log(log.ERROR, 'Cannot add user [%s] into group [%s]', user_dn, group_dn)
                log(log.ERROR, "%s", connection.result)
                return None

        for user in self.users:
            if user.dn == user_dn:
                return user
        log(log.ERROR, 'Non found [%s]', user_dn)
        return None

    def delete_user(self, name):
        user_dn = self.FORMAT_USER_DN.format(name)
        with ldap3.Connection(self.server, user=config.LDAP_USER, password=config.LDAP_PASS) as connection:
            success = connection.delete(user_dn)
            if not success:
                log(log.ERROR, 'Cannot delete user [%s]', user_dn)
                log(log.ERROR, "%s", connection.result)
                return False
        return True
