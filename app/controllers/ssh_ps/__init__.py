# cSpell:ignore paramiko
from paramiko import SSHClient, AutoAddPolicy
from config import BaseConfig as conf

from app.logger import log


class RemoteShell:
    class Error(Exception):
        def __init__(self, message: str):
            self.message = message

    def __init__(self):
        if conf.REMOTE_SHELL_SERVER:
            self.client = SSHClient()
            self.client.set_missing_host_key_policy(AutoAddPolicy())
            self.client.connect(
                conf.REMOTE_SHELL_SERVER,
                port=conf.REMOTE_SHELL_PORT,
                username=conf.REMOTE_SHELL_USER,
                password=conf.REMOTE_SHELL_PASS,
            )
        else:
            log(log.WARNING, "RemoteShell: please define REMOTE_SHELL_SERVER")
            self.client = None

    def send_command(self, cmd: str):
        log(log.DEBUG, "RemoteShell: command [%s]", cmd)
        if not self.client:
            return None
        stdin, stdout, stderr = self.client.exec_command(cmd)
        error_lines = stderr.readlines()
        if error_lines:
            log(log.ERROR, "RemoteShell: error exec command [%s]", cmd)
            error_message = "\n".join([line.strip("\n\r") for line in error_lines])
            raise RemoteShell.Error(error_message)
        result = "\n".join([line.strip("\n\r") for line in stdout.readlines()])
        log(log.DEBUG, "RemoteShell: result [%s]", result)
        return result
