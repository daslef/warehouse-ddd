from warehouse_ddd_petproject import exceptions
from warehouse_ddd_petproject import model
from warehouse_ddd_petproject import unit_of_work

# from sqlalchemy.orm import Session


def allocate(
    line: model.OrderLine, uow: unit_of_work.AbstractUnitOfWork
) -> str:
    with uow:
        batches = uow.batches.list()

        if not any(line.sku == batch.sku for batch in batches):
            raise exceptions.InvalidSku(f"Invalid sku {line.sku}")

        try:
            batchref = model.allocate(line, batches)
            uow.commit()
        except exceptions.OutOfStock:
            raise
        else:
            return batchref
