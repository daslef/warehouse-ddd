from datetime import date
from typing import Optional, Self


class OrderLine:
    """Товарная позиция"""

    def __init__(self, orderid: str, sku: str, qty: int):
        self.orderid = orderid
        self.sku = sku
        self.qty = qty


class Batch:
    """Партия"""

    def __init__(self, reference: str, sku: str, qty: int, eta: Optional[date] = None):
        self.reference = reference
        self.sku = sku
        self.initial_quantity = qty
        self.eta = eta
        self.allocations = set()

    def __gt__(self, other: Self) -> bool:
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

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
