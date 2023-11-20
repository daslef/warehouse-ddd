from datetime import date, timedelta
import pytest

from model import Batch, OrderLine, allocate
from exceptions import OutOfStock


def test_prefers_warehouse_batches_to_shipments():
    """
    arrange: создать батч, доступный на складе, и батч находящийся в пути; создать товарную позицию;
    act: запросить сервис allocate;
    assert: убедиться, что размещение произошло в складском батче (уменьшилось доступное количество),
            а батч в пути не изменился;
    """

    warehouse_batch = Batch("warehouse-001", "PRETTY_CHAIR", 20)
    shipping_batch = Batch("shipping-001", "PRETTY_CHAIR", 20, eta=date.today())
    line = OrderLine("chairs-001", "PRETTY_CHAIR", 10)

    allocate(line, [shipping_batch, warehouse_batch])

    assert warehouse_batch.available_quantity == 10
    assert shipping_batch.available_quantity == 20


def test_prefers_earlier_batches():
    """
    arrange: создать батчи, доступные сегодня, завтра и через неделю;
    act: запросить сервис allocate
    assert: убедиться, что размещение произошло в сегодняшнем батче;
    """

    today_batch = Batch("shipping-001", "PRETTY_CHAIR", 20, eta=date.today())
    tomorrow_batch = Batch(
        "shipping-002", "PRETTY_CHAIR", 20, eta=date.today() + timedelta(days=1)
    )
    week_batch = Batch(
        "shipping-003", "PRETTY_CHAIR", 20, eta=date.today() + timedelta(days=7)
    )
    line = OrderLine("chairs-001", "PRETTY_CHAIR", 10)

    allocate(line, [tomorrow_batch, week_batch, today_batch])

    assert today_batch.available_quantity == 10


def test_returns_allocated_batch_ref():
    """
    arrange: создать батч и товарную позицию;
    act: запросить сервис allocate
    assert: убедиться, что сервис allocate вернул значение,
            эквивалентное референсу батча
    """

    batch = Batch("shipping-001", "PRETTY_CHAIR", 20, eta=date.today())
    line = OrderLine("chairs-001", "PRETTY_CHAIR", 10)

    assert allocate(line, [batch]) == batch.reference


def test_raises_out_of_stock_exception_if_cannot_allocate():
    """
    arrange: создать батч и товарную позицию;
    act: разместить в батче заказ на больший объем;
    assert: убедиться, что сервис allocate выбросил ошибку OutOfStock
    """

    batch = Batch("shipping-001", "PRETTY_CHAIR", 20, eta=date.today())
    line = OrderLine("chairs-001", "PRETTY_CHAIR", 30)

    with pytest.raises(OutOfStock):
        allocate(line, [batch])
