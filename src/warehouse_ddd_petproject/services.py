import model
import repository
from exceptions import InvalidSku, OutOfStock


def allocate(
    line: model.OrderLine, repo: repository.AbstractRepository, session
) -> str:
    batches = repo.list()

    if not any(line.sku == batch.sku for batch in batches):
        raise InvalidSku(f"Invalid sku {line.sku}")

    try:
        batchref = model.allocate(line, batches)
    except OutOfStock:
        raise

    session.commit()

    return batchref
