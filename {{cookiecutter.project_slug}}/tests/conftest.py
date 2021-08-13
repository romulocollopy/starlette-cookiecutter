import os

import pytest  # type: ignore
from starlette.config import environ
from starlette.testclient import TestClient

os.environ["PYTHONASYNCIODEBUG"] = "1"
os.environ["PYTHONTRACEMALLOC"] = "1"
os.environ["TESTING"] = "True"

environ["TESTING"] = "TRUE"


@pytest.fixture(autouse=True)
def setup_test_database():
    """
    Create a clean test database every time the tests are run.
    """
    from infra.db import teardown_db, run_migrations, init_db

    init_db()
    run_migrations()

    yield  # Run the tests.
    teardown_db()


@pytest.fixture()
def client():
    """
    Make a 'client' fixture available to test cases.
    """
    # Our fixture is created within a context manager. This ensures that
    # application startup and shutdown run for every test case.
    #
    # Because we've configured the DatabaseMiddleware with `rollback_on_shutdown`
    # we'll get a complete rollback to the initial state after each test case runs.
    from app import webapp

    with TestClient(webapp) as test_client:
        yield test_client
