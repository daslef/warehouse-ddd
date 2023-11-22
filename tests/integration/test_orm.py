from datetime import date

from sqlalchemy.sql import text

import model


def test_orderline_mapper_loads_lines(in_memory_session):
    expected = [
        model.OrderLine("order1", "red-chair", 12),
        model.OrderLine("order2", "red-table", 13),
        model.OrderLine("order3", "blue-lipstick", 14),
    ]

    query = text(
        """insert into order_lines (
            orderid, sku, qty
        ) values 
            ('order1', 'red-chair', 12), ('order2', 'red-table', 13), ('order3', 'blue-lipstick', 14)"""
    )

    in_memory_session.execute(query)

    assert in_memory_session.query(model.OrderLine).all() == expected


def test_orderline_mapper_save_lines(in_memory_session):
    expected = [("order1", "blue-velvet", 5)]

    new_line = model.OrderLine("order1", "blue-velvet", 5)
    in_memory_session.add(new_line)
    in_memory_session.commit()

    query = text("""select orderid, sku, qty from order_lines""")
    assert list(in_memory_session.execute(query)) == expected


def test_batches_mapper_loads_lines(in_memory_session):
    expected = [
        model.Batch("batch-001", "SMALL-TABLE", qty=20),
        model.Batch("batch-002", "UNCOMFORTABLE-CHAIR", 100, eta=date.today()),
    ]

    query = text(
        """insert into batches (
            reference, sku, initial_quantity, eta
        ) values 
            ('batch-001', 'SMALL-TABLE', 10, NULL), 
            ('batch-002', 'UNCOMFORTABLE-CHAIR', 100, DATE('now'))"""
    )

    in_memory_session.execute(query)

    assert in_memory_session.query(model.Batch).all() == expected


def test_batches_mapper_save_lines(in_memory_session):
    expected = [
        ("batch-001", "SMALL-TABLE", 20, None),
        ("batch-002", "UNCOMFORTABLE-CHAIR", 100, date.today().strftime("%Y-%m-%d")),
    ]

    batch1 = model.Batch("batch-001", "SMALL-TABLE", qty=20)
    batch2 = model.Batch("batch-002", "UNCOMFORTABLE-CHAIR", 100, eta=date.today())

    in_memory_session.add(batch1)
    in_memory_session.add(batch2)
    in_memory_session.commit()

    query = text("""select reference, sku, initial_quantity, eta from batches""")
    assert list(in_memory_session.execute(query)) == expected


def test_allocations_mapper_loads_lines(in_memory_session):
    expected = set(
        [
            model.OrderLine("order1", "red-chair", 12),
            model.OrderLine("order2", "red-table", 13),
        ]
    )

    query_batch = text(
        """insert into batches (
            reference, sku, initial_quantity, eta
        ) values 
            ('batch-001', 'SMALL-TABLE', 10, NULL)"""
    )

    query_orderline = text(
        """insert into order_lines (
            orderid, sku, qty
        ) values 
            ('order1', 'red-chair', 12), 
            ('order2', 'red-table', 13)"""
    )

    query_allocation = text(
        """insert into allocations (orderline_id, batch_id) 
        values (1, 1), (2, 1)"""
    )

    in_memory_session.execute(query_batch)
    in_memory_session.execute(query_orderline)
    in_memory_session.execute(query_allocation)
    in_memory_session.commit()

    batch = in_memory_session.query(model.Batch).one()
    batch_allocations = batch.allocations

    assert batch_allocations == expected


def test_allocations_mapper_save_lines(in_memory_session):
    expected = [
        (1, 1),
        (2, 1),
    ]

    batch = model.Batch("batch-001", "red-chair", qty=20)
    orderline1 = model.OrderLine("order1", "red-chair", 5)
    orderline2 = model.OrderLine("order2", "red-chair", 10)

    batch.allocate(orderline1)
    batch.allocate(orderline2)

    in_memory_session.add(batch)
    in_memory_session.commit()

    query = text("""select orderline_id, batch_id from allocations""")
    assert list(in_memory_session.execute(query)) == expected
