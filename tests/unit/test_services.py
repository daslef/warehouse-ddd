import pytest

from warehouse_ddd_petproject.domain import exceptions
from warehouse_ddd_petproject.domain import model
from warehouse_ddd_petproject.domain import repository
from warehouse_ddd_petproject.domain import services
from warehouse_ddd_petproject.domain import unit_of_work


def test_returns_allocation_on_valid_sku():
    line = model.OrderLine("table-001", "table", 20)
    batch = model.Batch("batch-001", "table", 30, None)

    uow = unit_of_work.FakeUnitOfWork(repository.FakeRepository([batch]))

    assert services.allocate(line, uow) == "batch-001"


def test_raises_error_on_invalid_sku():
    line = model.OrderLine("table-001", "table", 20)
    batch = model.Batch("batch-001", "spoon", 30, None)

    uow = unit_of_work.FakeUnitOfWork(repository.FakeRepository([batch]))

    with pytest.raises(exceptions.InvalidSku):
        services.allocate(line, uow)


def test_raises_error_on_outofstock():
    line = model.OrderLine("table-001", "table", 40)
    batch = model.Batch("batch-001", "table", 30, None)

    uow = unit_of_work.FakeUnitOfWork(repository.FakeRepository([batch]))

    with pytest.raises(exceptions.OutOfStock):
        services.allocate(line, uow)
