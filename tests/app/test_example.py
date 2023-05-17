from fastapi import status
from fastapi.testclient import TestClient

from tests.testutil import logger  # noqa: F401


def test_example(client: TestClient) -> None:
    res = client.get("/docs")
    assert res.status_code != status.HTTP_200_OK
