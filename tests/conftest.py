import logging
from typing import Generator

from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy.orm.session import close_all_sessions

from app import config
from app.auth import get_current_user
from app.database import Base, SessionLocal, engine
from app.main import app
from app.models import User
from tests.testutil import logger  # noqa: F401
from tests.testutil import create_test_user

logging.basicConfig()
logging.getLogger("asyncio").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


def override_dependency() -> User:
    return User(email="mg.atd.1107@gmail.com")


app.dependency_overrides[get_current_user] = override_dependency


@fixture(scope="function")
def client() -> Generator[TestClient, None, None]:
    assert config.ENV == "test"
    create_test_user()

    # テスト実行
    yield TestClient(app)

    SessionLocal.execute("set foreign_key_checks = 0")

    for name in Base.metadata.tables.keys():
        SessionLocal.execute(f"TRUNCATE TABLE `{name}`")

    SessionLocal.execute("set foreign_key_checks = 1")

    close_all_sessions()
    engine.dispose()
