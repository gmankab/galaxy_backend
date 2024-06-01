import pytest
from typing import Generator
from fastapi.testclient import TestClient
from tortoise.contrib.test import finalizer, initializer

from main import app

@pytest.fixture(scope="module", autouse=True)
def client() -> Generator:
    initializer(["main"])  # Ensure 'main' matches the module where your models are defined
    with TestClient(app) as test_client:
        yield test_client
    finalizer()
