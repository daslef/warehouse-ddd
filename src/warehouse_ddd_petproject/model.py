from datetime import date
from typing import Self

from flask_login import UserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from .exceptions import OutOfStock


class User(UserMixin):
    def __init__(self, username: str, password: str):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)


class OrderLine:
    """Товарная позиция."""

    def __init__(self, orderid: str, sku: str, qty: int) -> None:
        self.orderid = orderid
        self.sku = sku
        self.qty = qty

    def __hash__(self):
        return hash((self.orderid, self.sku, self.qty))

    def __eq__(self, other_order_line) -> bool:
        return hash(self) == hash(other_order_line)


class Batch:
    """Партия."""

    def __init__(self, reference: str, sku: str, qty: int, eta: date | None = None):
        self.reference = reference
        self.sku = sku
        self.initial_quantity = qty
        self.eta = eta
        self.allocations = set()

    def __eq__(self, other_batch) -> bool:
        return self.reference == other_batch.reference

    def __hash__(self) -> int:
        return hash(self.reference)

    def __gt__(self, other_batch: Self) -> bool:
        if self.eta is None:
            return False
        if other_batch.eta is None:
            return True
        return self.eta > other_batch.eta

    @property
    def allocated_quantity(self):
        return sum(line.qty for line in self.allocations)

    @property
    def available_quantity(self):
        return self.initial_quantity - self.allocated_quantity

    def allocate(self, line: OrderLine) -> None:
        self.allocations.add(line)

    def deallocate(self, line: OrderLine) -> None:
        if line in self.allocations:
            self.allocations.remove(line)

    def can_allocate(self, line: OrderLine) -> bool:
        if line in self.allocations:
            return False
        if self.sku != line.sku:
            return False
        return self.available_quantity >= line.qty


def allocate(line: OrderLine, batches: list[Batch]) -> str:
    sorted_suitable_batches = sorted(
        batch for batch in batches if batch.can_allocate(line)
    )

    if len(sorted_suitable_batches) == 0:
        raise OutOfStock(f"Sku {line.sku} is out of stock")

    selected_batch = sorted_suitable_batches[0]
    selected_batch.allocate(line)

    return selected_batch.reference
