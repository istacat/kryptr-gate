""" AD User """
import ldap3

from app.controllers import RemoteShell
from config import BaseConfig as config


class User(object):
    def __init__(self, ldap_entry):
        self.LDAP_URI = f"ldap://{config.LDAP_SERVER}"
        self.ldap_entry = ldap_entry
        pass

    @property
    def dn(self):
        return self.ldap_entry.entry_dn

    @property
    def mail(self):
        values = [v.decode() for v in self.ldap_entry.entry_raw_attributes["mail"]]
        if values:
            return values[0]
        return None

    def delete(self):
        """ delete the AD user"""
        self.server = ldap3.Server(self.LDAP_URI, get_info=ldap3.ALL)
        with ldap3.Connection(
            self.server, user=config.LDAP_USER, password=config.LDAP_PASS
        ) as connection:
            connection.delete(self.dn)

    def to_json(self):
        return self.ldap_entry.entry_to_json()

    def reset_password(self, new_pass: str):
        """reset user password

        Args:
            new_pass (str): the new password

        Returns:
            bool: True if operation succeeded
        """
        # flake8: noqa E501
        # posh: Set-ADAccountPassword -Identity "CN=Account CYF787,CN=Users,DC=kryptr,DC=li" -Reset -NewPassword (ConvertTo-SecureString -AsPlainText "Simple2B123" -Force)
        sh = RemoteShell()
        res = sh.send_command(
            " ".join(
                [
                    "Set-ADAccountPassword",
                    f"-Identity '{self.dn}'",
                    "-Reset",
                    "-NewPassword",
                    f"(ConvertTo-SecureString -AsPlainText '{new_pass}' -Force)",
                ]
            )
        )
        recognise_error_message = res.split("Set-ADAccountPassword :")
        if len(recognise_error_message) > 1:
            message_parts = recognise_error_message[1].split("\x1b")
            return message_parts[0].strip(" \n\r\t")
        return ""
