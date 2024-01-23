from warehouse_ddd_petproject import exceptions
from warehouse_ddd_petproject import model
from warehouse_ddd_petproject import repository

from sqlalchemy.orm import Session


def allocate(
    line: model.OrderLine, repo: repository.AbstractRepository, session: Session
) -> str:
    batches = repo.list()

    if not any(line.sku == batch.sku for batch in batches):
        raise exceptions.InvalidSku(f"Invalid sku {line.sku}")

    try:
        batchref = model.allocate(line, batches)
    except exceptions.OutOfStock:
        raise

    session.commit()

    return batchref
