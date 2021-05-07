import pytest

from app import db, create_app
from app.controllers import SimPro
from tests.db_data import fill_test_data
from config import BaseConfig as conf


TEST_SIM_ICCID = 89882390000165618367


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


@pytest.mark.skipif(not conf.SIMPRO_BASE_URL, reason="SimPro URL not configured")
def test_simpro(client):
    conn = SimPro()
    assert conn
    sim_details = conn.sim_info(TEST_SIM_ICCID)
    assert sim_details
    solutions = conn.customer_solutions
    assert solutions
    sims = conn.sims
    assert sims
    sim = conn.check_sim(TEST_SIM_ICCID)
    assert sim
    activate_sim = conn.activate_sim(TEST_SIM_ICCID)
    assert activate_sim
    bar_sim = conn.bar_sim(TEST_SIM_ICCID)
    assert bar_sim
