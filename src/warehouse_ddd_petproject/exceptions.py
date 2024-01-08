class OutOfStock(Exception):
    """
    OrderLine cannot be allocated
    """

    pass


class InvalidSku(Exception):
    """
    Batch with this sku cannot be found
    """

    pass
