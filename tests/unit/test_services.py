import pytest

from warehouse_ddd_petproject import exceptions
from warehouse_ddd_petproject import model
from warehouse_ddd_petproject import repository
from warehouse_ddd_petproject import services


def test_returns_allocation_on_valid_sku(fake_session):
    line = model.OrderLine("table-001", "table", 20)
    batch = model.Batch("batch-001", "table", 30, None)
    repo = repository.FakeRepository([batch])
    session = fake_session()

    assert services.allocate(line, repo, session) == "batch-001"


def test_raises_error_on_invalid_sku(fake_session):
    line = model.OrderLine("table-001", "table", 20)
    batch = model.Batch("batch-001", "spoon", 30, None)
    repo = repository.FakeRepository([batch])
    session = fake_session()

    with pytest.raises(exceptions.InvalidSku):
        services.allocate(line, repo, session)


def test_raises_error_on_outofstock(fake_session):
    line = model.OrderLine("table-001", "table", 40)
    batch = model.Batch("batch-001", "table", 30, None)
    repo = repository.FakeRepository([batch])
    session = fake_session()

    with pytest.raises(exceptions.OutOfStock):
        services.allocate(line, repo, session)
