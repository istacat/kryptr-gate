import os
import pytest

from app import db, create_app
from app.controllers import MDM
from tests.db_data import fill_test_data


@pytest.fixture
def client():
    app = create_app(environment="testing")
    app.config["TESTING"] = True

    with app.test_client() as client:
        app_ctx = app.app_context()
        app_ctx.push()
        db.drop_all()
        db.create_all()
        fill_test_data()
        yield client
        db.session.remove()
        db.drop_all()
        app_ctx.pop()


TEST_DEVICE_ID = os.environ.get("TEST_DEVICE_ID", None)  # 3034


@pytest.mark.skipif(not TEST_DEVICE_ID, reason="Test device id doesnt set")
def test_main_endpoints(client):
    conn = MDM()

    groups = conn.groups
    assert(groups)
    assert len(groups) > 50

    devices = conn.devices
    assert devices
    assert len(devices)

    device = conn.get_device(TEST_DEVICE_ID)
    assert device

    users = conn.users
    assert users

    test_device = None
    for device in devices:
        assert device.actions
        if device.device_id == TEST_DEVICE_ID:
            test_device = device

    action = test_device.get_action("remote_alarm")
    assert action
    assert action.run() == 202
    status = action.status
    assert status
