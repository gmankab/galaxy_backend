import pytest
from typing import Generator
from fastapi.testclient import TestClient
from tortoise.contrib.test import finalizer, initializer

from main import app

@pytest.fixture(scope="module", autouse=True)
def client() -> Generator:
    initializer(["main"], db_url="sqlite://:memory:", app_label="models")
    app.state.db_url = "sqlite://:memory:"
    with TestClient(app) as test_client:
        yield test_client
    finalizer()
