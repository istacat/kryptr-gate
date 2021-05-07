import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


class BaseConfig(object):
    """Base configuration."""

    APP_NAME = os.environ.get("APP_NAME", "Flask App")
    JSON_SORT_KEYS = False
    DEBUG_TB_ENABLED = False
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "Ensure you set a secret key, this is important!"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

    LDAP_USER = os.environ.get("LDAP_USER", None)
    LDAP_PASS = os.environ.get("LDAP_PASS", None)
    LDAP_SERVER = os.environ.get("LDAP_SERVER", None)
    AD_NAME = os.environ.get("AD_NAME", "DC=kryptr,DC=li")

    REMOTE_SHELL_SERVER = os.environ.get("REMOTE_SHELL_SERVER", None)
    REMOTE_SHELL_USER = os.environ.get("REMOTE_SHELL_USER", None)
    REMOTE_SHELL_PASS = os.environ.get("REMOTE_SHELL_PASS", None)
    REMOTE_SHELL_PORT = int(os.environ.get("REMOTE_SHELL_PORT", 0))

    MATRIX_SERVER_HOST_NAME = os.environ.get("MATRIX_SERVER_HOST_NAME", None)
    MATRIX_SERVER_USER_NAME = os.environ.get("MATRIX_SERVER_USER_NAME", None)

    BASE_MDM_API_URL = os.environ.get("BASE_MDM_API_URL", None)
    MDM_API_KEY = os.environ.get("MDM_API_KEY", None)

    STARTING_PAGE = os.environ.get('STARTING_PAGE', 1)
    ITEMS_PER_PAGE = os.environ.get('ITEMS_PER_PAGE', 20)

    SIMPRO_BASE_URL = os.environ.get('SIMPRO_BASE_URL', None)
    SIMPRO_USERNAME = os.environ.get('SIMPRO_USERNAME', None)
    SIMPRO_PASSWORD = os.environ.get('SIMPRO_PASSWORD', None)

    @staticmethod
    def configure(app):
        # Implement this method to do further configuration on your app.
        pass


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEVEL_DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "database-devel.sqlite3"),
    )


class TestingConfig(BaseConfig):
    """Testing configuration."""

    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "database-test.sqlite3"),
    )


class ProductionConfig(BaseConfig):
    """Production configuration."""

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "database.sqlite3")
    )
    WTF_CSRF_ENABLED = True


config = dict(
    development=DevelopmentConfig, testing=TestingConfig, production=ProductionConfig
)
