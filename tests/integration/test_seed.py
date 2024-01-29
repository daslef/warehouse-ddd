from warehouse_ddd_petproject.infrastructure import seed
from warehouse_ddd_petproject.domain import model, repository


def test_seed(postgres_session):
    expected = [
        model.Batch("batch-001", "table", 100, None),
        model.Batch("batch-002", "chair", 20, None),
    ]

    seed.seed_db(postgres_session)

    repo = repository.SqlAlchemyRepository(postgres_session)
    batches = repo.list()

    assert all(batch in batches for batch in expected)
