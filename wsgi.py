#!/user/bin/env python
import os

import click

from app import create_app, db, models, forms
from app.models import User
from tests.db_data import fill_test_data

app = create_app()

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin")


def add_admin():
    User(
        username=ADMIN_USERNAME,
        password=ADMIN_PASSWORD,
        activated=User.StatusType.active,
        role=User.RoleType.admin
    ).save()


def _init_db():
    db.create_all()
    add_admin()


# flask cli context setup
@app.shell_context_processor
def get_context():
    """Objects exposed here will be automatically available from the shell."""
    return dict(app=app, db=db, m=models, forms=forms)


@app.cli.command()
@click.confirmation_option(prompt="Delete all data from database tables?")
@click.option('--test_data', default=False, help='Populate DB by testing data.')
def reset_db(test_data):
    """Reset the current database."""
    db.drop_all()
    _init_db()
    if test_data:
        fill_test_data()


@app.cli.command()
@click.option('--test_data', default=False, help='Populate DB by testing data.')
def create_db(test_data):
    """Create the configured database."""
    _init_db()
    if test_data:
        fill_test_data()


@app.cli.command()
@click.confirmation_option(prompt='Drop all database tables?')
def drop_db():
    """Drop the current database."""
    db.drop_all()


if __name__ == '__main__':
    app.run()
