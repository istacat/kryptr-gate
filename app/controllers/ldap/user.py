""" AD User """
import ldap3

from config import BaseConfig as config


class User(object):
    def __init__(self, ldap_entry):
        self.ldap_entry = ldap_entry
        pass

    @property
    def dn(self):
        return self.ldap_entry.entry_dn

    @property
    def mail(self):
        values = [v.decode() for v in self.ldap_entry.entry_raw_attributes['mail']]
        if values:
            return values[0]
        return None

    def delete(self):
        """ delete the AD user"""
        self.server = ldap3.Server(self.LDAP_URI, get_info=ldap3.ALL)
        with ldap3.Connection(self.server, user=config.LDAP_USER, password=config.LDAP_PASS) as connection:
            connection.delete(self.dn)

    def to_json(self):
        return self.ldap_entry.entry_to_json()
