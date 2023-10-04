from datetime import date, timedelta
import pytest


@pytest.mark.skip(reason="allocate service is not implemented yet")
def test_prefers_warehouse_batches_to_shipments():
    """
    arrange: создать батч, доступный на складе, и батч находящийся в пути; создать товарную позицию;
    act: запросить сервис allocate;
    assert: убедиться, что размещение произошло в складском батче (уменьшилось доступное количество),
            а батч в пути не изменился;
    """
    pytest.fail("todo")


@pytest.mark.skip(reason="allocate service is not implemented yet")
def test_prefers_earlier_batches():
    """
    arrange: создать батчи, доступные сегодня, завтра и через неделю;
    act: запросить сервис allocate
    assert: убедиться, что размещение произошло в сегодняшнем батче;
    """
    pytest.fail("todo")


@pytest.mark.skip(reason="allocate service is not implemented yet")
def test_returns_allocated_batch_ref():
    """
    arrange: создать два батча и товарную позицию;
    act: запросить сервис allocate
    assert: убедиться, что сервис allocate вернул значение,
            эквивалентное референсу выбранного батча
    """
    pytest.fail("todo")


@pytest.mark.skip(reason="allocate service is not implemented yet")
def test_raises_out_of_stock_exception_if_cannot_allocate():
    """
    arrange: создать батч и разместить в нем заказ на весь объем;
    act: запросить дополнительное размещение в том же батче;
    assert: убедиться, что сервис allocate выбросил ошибку OutOfStock
    """
    pytest.fail("todo")
