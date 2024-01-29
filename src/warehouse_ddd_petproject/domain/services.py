from warehouse_ddd_petproject.domain import exceptions
from warehouse_ddd_petproject.domain import model
from warehouse_ddd_petproject.domain import unit_of_work


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
