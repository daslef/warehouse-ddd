# pytest: disable=redefined-outer-name
import time
from pathlib import Path

import pytest
import httpx
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker, clear_mappers

from db_tables import metadata, start_mappers
from config import build_api_url


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    try:
        start_mappers()
    except exc.ArgumentError:
        pass

    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()


@pytest.fixture
def api_url():
    env_path = Path(__file__).parent / ".." / ".env"
    return build_api_url(env_path)


@pytest.fixture
def restart_api(api_url):
    TIMEOUT = 10
    DELAY = 0.5

    deadline = time.time() + TIMEOUT

    while time.time() < deadline:
        try:
            return httpx.get(api_url)
        except (httpx.ConnectTimeout, httpx.ConnectError):
            time.sleep(DELAY)

    pytest.fail("api could not start")
