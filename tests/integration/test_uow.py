from tests import helpers
from warehouse_ddd_petproject.domain import repository
from warehouse_ddd_petproject.domain import model, services, unit_of_work


def test_uow_can_retrieve_a_batch_and_allocate_to_it(postgres_session):
    helpers.insert_batch_uow(
        postgres_session, "batch-uow", "HIPSTER-WORKBENCH", 100, None
    )

    postgres_session.commit()
    uow = unit_of_work.SqlAlchemyUnitOfWork(postgres_session)

    with uow:
        batch = uow.batches.get(reference="batch-uow")
        line = model.OrderLine("o-uow", "HIPSTER-WORKBENCH", 10)
        batch.allocate(line)
        uow.commit()

    batchref = helpers.get_allocated_batch_ref(
        postgres_session, "o-uow", "HIPSTER-WORKBENCH"
    )

    assert batchref == "batch-uow"


def test_add_batch():
    uow = unit_of_work.FakeUnitOfWork(repository.FakeRepository([]))
    uow.batches.add(model.Batch("b1", "CRUNCHY-ARMCHAIR", 100, None))
    uow.commit()

    assert uow.batches.get("b1") is not None
    assert uow.committed


def test_allocate_returns_allocation():
    uow = unit_of_work.FakeUnitOfWork(repository.FakeRepository([]))
    uow.batches.add(model.Batch("b1", "CRUNCHY-ARMCHAIR", 100, None))

    result = services.allocate(
        model.OrderLine("o1", "CRUNCHY-ARMCHAIR", 10), uow
    )
    assert result == "b1"
