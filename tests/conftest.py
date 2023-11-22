# pytest: disable=redefined-outer-name
import time
from pathlib import Path

import pytest
import httpx
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.sql import text

from db_tables import metadata, start_mappers
from config import build_api_url, build_db_uri


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture(scope="session")
def postgres_db(db_uri):
    TIMEOUT = 10
    DELAY = 0.5

    engine = create_engine(db_uri)

    deadline = time.time() + TIMEOUT

    while time.time() < deadline:
        try:
            engine.connect()
        except exc.OperationalError:
            time.sleep(DELAY)
        else:
            metadata.create_all(engine)
            return engine

    pytest.fail("postgres could not start")


@pytest.fixture
def in_memory_session(in_memory_db):
    try:
        start_mappers()
    except exc.ArgumentError:
        pass

    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()


@pytest.fixture
def postgres_session(postgres_db):
    try:
        start_mappers()
    except exc.ArgumentError:
        pass

    yield sessionmaker(bind=postgres_db)()
    clear_mappers()


@pytest.fixture
def fake_session():
    class FakeSession:
        committed = False

        def commit(self):
            self.committed = True

    return FakeSession


@pytest.fixture(scope="session")
def db_uri():
    env_path = Path(__file__).parent / ".." / ".env"
    return build_db_uri(env_path)


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


@pytest.fixture
def add_stock(postgres_session):
    batches_added = set()
    skus_added = set()

    def _add_stock(lines):
        for ref, sku, qty, eta in lines:
            postgres_session.execute(
                text(
                    """INSERT INTO batches (reference, sku, initial_quantity, eta)
                 VALUES (:ref, :sku, :qty, :eta)"""
                ),
                dict(ref=ref, sku=sku, qty=qty, eta=eta),
            )
            [[batch_id]] = postgres_session.execute(
                text("SELECT id FROM batches WHERE reference=:ref AND sku=:sku"),
                dict(ref=ref, sku=sku),
            )
            batches_added.add(batch_id)
            skus_added.add(sku)
        postgres_session.commit()

    yield _add_stock

    for batch_id in batches_added:
        postgres_session.execute(
            text("DELETE FROM allocations WHERE batch_id=:batch_id"),
            dict(batch_id=batch_id),
        )
        postgres_session.execute(
            text("DELETE FROM batches WHERE id=:batch_id"),
            dict(batch_id=batch_id),
        )
    for sku in skus_added:
        postgres_session.execute(
            text("DELETE FROM order_lines WHERE sku=:sku"),
            dict(sku=sku),
        )
        postgres_session.commit()
