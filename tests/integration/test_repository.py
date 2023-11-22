from sqlalchemy.sql import text

import model
import repository
import helpers


def test_repository_can_save_a_batch(in_memory_session):
    """
    arrange: получить фикстуру сессии, создать экземпляр класса батч
    act: инициализировать репозиторий Sql, добавить батч в репозиторий, сделать коммит
    assert: выполнить селект-запрос к сессии, сравнить список строк с ожидаемым
    """
    expected = [("batch-001", "small-watches", 200, None)]
    batch = model.Batch("batch-001", "small-watches", 200)

    repo = repository.SqlAlchemyRepository(in_memory_session)
    repo.add(batch)
    in_memory_session.commit()

    select_query = text("select reference, sku, initial_quantity, eta from batches")
    assert list(in_memory_session.execute(select_query)) == expected


def test_repository_can_retrieve_a_batch_with_allocations(in_memory_session):
    """
    arrange: получить фикстуру сессии, добавить товарную позицию, батч и размещение в БД
    act: инициализировать репозиторий Sql, получить добавленный батч по идентификатору
    assert: сравнить полученный из репозитория батч с правильным ("batch1", "GENERIC-SOFA", 100, eta=None)
    по __eq__, сравнить их sku, initial_quantity и _allocations
    """
    expected = model.Batch("batch-001", "GENERIC-SOFA", 100, None)

    line = helpers.insert_order_line(in_memory_session)
    batch = helpers.insert_batch(in_memory_session, "batch-001")
    helpers.insert_allocation(in_memory_session, line, batch)

    repo = repository.SqlAlchemyRepository(in_memory_session)
    retrieved_batch = repo.get("batch-001")

    assert retrieved_batch == expected
    assert retrieved_batch.sku == expected.sku
    assert retrieved_batch.initial_quantity == expected.initial_quantity
    assert retrieved_batch.allocations == {
        model.OrderLine("order1", "GENERIC-SOFA", 12)
    }


def test_repository_can_retrieve_batches_list(in_memory_session):
    expected = [
        model.Batch("batch-001", "GENERIC-SOFA", 100, None),
        model.Batch("batch-002", "GENERIC-SOFA", 100, None),
    ]

    helpers.insert_batch(in_memory_session, "batch-001")
    helpers.insert_batch(in_memory_session, "batch-002")

    repo = repository.SqlAlchemyRepository(in_memory_session)
    assert repo.list() == expected


def test_updating_a_batch(in_memory_session):
    """
    arrange: получить фикстуру сессии, создать два заказа (две товарные позиции) и один батч,
             разместить в нем первый заказ; инициализировать репозиторий Sql, добавить в него батч,
             сделать коммит;
    act: разместить в батче второй заказ, добавить в репозиторий, сделать коммит;
    assert: проверить (c помощью get_allocations), что были размещены обе товарные позиции (оба заказа);
    """

    batch = model.Batch("batch-001", "GENERIC-SOFA", 100, None)
    line1 = model.OrderLine("order1", "GENERIC-SOFA", 10)
    line2 = model.OrderLine("order2", "GENERIC-SOFA", 40)
    expected = {line1.orderid, line2.orderid}
    model.allocate(line1, [batch])

    repo = repository.SqlAlchemyRepository(in_memory_session)
    repo.add(batch)
    in_memory_session.commit()

    model.allocate(line2, [batch])
    repo.add(batch)
    in_memory_session.commit()

    assert helpers.get_allocations(in_memory_session, "batch-001") == expected
