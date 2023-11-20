import model
import repository
from exceptions import InvalidSku


def allocate(
    line: model.OrderLine, repo: repository.AbstractRepository, session
) -> str:
    batches = repo.list()

    if not any(line.sku == batch.sku for batch in batches):
        raise InvalidSku(f"Invalid sku {line.sku}")

    batchref = model.allocate(line, batches)
    session.commit()

    return batchref
