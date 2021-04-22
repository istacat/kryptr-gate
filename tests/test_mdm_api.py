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


TEST_DEVICE_ID = os.environ.get("TEST_DEVICE_ID", "3025")


@pytest.mark.skipif(not TEST_DEVICE_ID, reason="Test device id doesnt set")
def test_main_endpoints(client):
    # acc = Account.query.get(1)
    conn = MDM()
    groups = conn.groups
    assert(groups)
    assert len(groups) > 50
    devices = conn.devices
    assert devices
    assert len(devices)
    test_device = None
    for device in devices:
        assert device.actions
        if device.device_id == TEST_DEVICE_ID:
            test_device = device

    test_device.status_action('scan')
    action = test_device.get_action("scan")
    assert action
    action.run()
    status = action.status
    assert status
    action.cancel()


def old_test():
    conn = MDM()
    actions = conn.get_available_actions()
    assert actions
    complete_wipe = conn.get_action_status('complete_wipe')  # Complete Wipe
    scan = conn.get_action_status('scan')  # Scan Now
    lock = conn.get_action_status('lock')  # Remote Lock
    remote_alarm = conn.get_action_status('remote_alarm')  # Remote Alarm
    corporate_wipe = conn.get_action_status('corporate_wipe')  # Corporate Wipe
    clear_passcode = conn.get_action_status('clear_passcode')  # Clear Passcode
    reset_passcode = conn.get_action_status('reset_passcode')  # Reset Passcode
    fetch_location = conn.get_action_status('fetch_location')  # Locate device
    enable_lost_mode = conn.get_action_status('enable_lost_mode')  # Enable Lost Mode
    restart = conn.get_action_status('restart')  # Restart Device
    remote_debug = conn.get_action_status('remote_debug')  # Request Bug Report
