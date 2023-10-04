import pytest

# import model
# import repository
# import helpers


@pytest.mark.skip(reason="repository is not implemented yet")
def test_repository_can_save_a_batch(session):
    """
    arrange: получить фикстуру сессии, создать экземпляр класса батч
    act: инициализировать репозиторий Sql, добавить батч в репозиторий, сделать коммит
    assert: выполнить селект-запрос к сессии, сравнить список строк с ожидаемым
    """
    pytest.fail("todo")


@pytest.mark.skip(reason="repository is not implemented yet")
def test_repository_can_retrieve_a_batch_with_allocations(session):
    """
    arrange: получить фикстуру сессии, добавить товарную позицию, батч и размещение в БД
    act: инициализировать репозиторий Sql, получить добавленный батч по идентификатору
    assert: сравнить полученный из репозитория батч с правильным ("batch1", "GENERIC-SOFA", 100, eta=None)
    по __eq__, сравнить их sku, _purchased_quantity и _allocations
    """
    pytest.fail("todo")


@pytest.mark.skip(reason="repository is not implemented yet")
def test_updating_a_batch(session):
    """
    arrange: получить фикстуру сессии, создать два заказа (две товарные позиции) и один батч,
             разместить в нем первый заказ; инициализировать репозиторий Sql, добавить в него батч,
             сделать коммит;
    act: разместить в батче второй заказ, добавить в репозиторий, сделать коммит;
    assert: проверить (c помощью get_allocations), что были размещены обе товарные позиции (оба заказа);
    """
    pytest.fail("todo")
