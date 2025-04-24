import pytest

from fastapi.testclient import TestClient

#@pytest.fixture()

def func(a):
    return a*a

def test_answer():
    assert func(3) == 9