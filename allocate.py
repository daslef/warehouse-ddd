from model import OrderLine, Batch
from exceptions import OutOfStock


def allocate(line: OrderLine, batches: list[Batch]) -> str:
    sorted_suitable_batches = sorted(
        batch for batch in batches if batch.can_allocate(line)
    )

    if len(sorted_suitable_batches) == 0:
        raise OutOfStock

    selected_batch = sorted_suitable_batches[0]
    selected_batch.allocate(line)

    return selected_batch.reference
