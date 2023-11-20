import uuid
from sqlalchemy.sql import text


def random_suffix():
    return uuid.uuid4()


def random_sku(name):
    return f"sku-{name}-{random_suffix()}"


def random_batchref(name):
    return f"batch-{name}-{random_suffix()}"


def random_orderid(name):
    return f"order-{name}-{random_suffix()}"


def insert_order_line(session):
    session.execute(
        text(
            "INSERT INTO order_lines (orderid, sku, qty)"
            ' VALUES ("order1", "GENERIC-SOFA", 12)'
        )
    )
    [[orderline_id]] = session.execute(
        text("SELECT id FROM order_lines WHERE orderid=:orderid AND sku=:sku"),
        dict(orderid="order1", sku="GENERIC-SOFA"),
    )
    return orderline_id


def insert_batch(session, batch_id):
    session.execute(
        text(
            "INSERT INTO batches (reference, sku, initial_quantity, eta)"
            ' VALUES (:batch_id, "GENERIC-SOFA", 100, null)'
        ),
        dict(batch_id=batch_id),
    )
    [[batch_id]] = session.execute(
        text('SELECT id FROM batches WHERE reference=:batch_id AND sku="GENERIC-SOFA"'),
        dict(batch_id=batch_id),
    )
    return batch_id


def insert_allocation(session, orderline_id, batch_id):
    session.execute(
        text(
            "INSERT INTO allocations (orderline_id, batch_id)"
            " VALUES (:orderline_id, :batch_id)"
        ),
        dict(orderline_id=orderline_id, batch_id=batch_id),
    )


def get_allocations(session, batchid):
    rows = list(
        session.execute(
            text(
                "SELECT orderid"
                " FROM allocations"
                " JOIN order_lines ON allocations.orderline_id = order_lines.id"
                " JOIN batches ON allocations.batch_id = batches.id"
                " WHERE batches.reference = :batchid"
            ),
            dict(batchid=batchid),
        )
    )
    return {row[0] for row in rows}
