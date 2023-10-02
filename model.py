from datetime import date
from typing import Optional


class OrderLine:
    def __init__(self, orderid: str, sku: str, qty: int):
        self.orderid = orderid
        self.sku = sku
        self.qty = qty


class Batch:
    def __init__(self, reference: str, sku: str, qty: int, eta: Optional[date]):
        self.reference = reference
        self.sku = sku
        self.available_quantity = qty
        self.eta = eta

    def allocate(self, line: OrderLine) -> None:
        self.available_quantity -= line.qty
