from tests.helpers import random_batchref
from tests.helpers import random_orderid
from tests.helpers import random_sku


def test_returns_allocation_on_valid_sku(add_stock, api_url, test_app):
    sku1 = random_sku("spoons")
    sku2 = random_sku("other")

    early_batchref = random_batchref(1)
    later_batchref = random_batchref(2)
    other_batchref = random_batchref(3)

    order_id = random_orderid("spoons")

    add_stock([
        (early_batchref, sku1, 20, "2024-01-02"),
        (later_batchref, sku1, 20, "2024-02-02"),
        (other_batchref, sku2, 20, None),
    ])

    client = test_app.test_client()

    response = client.post(
        "/api/allocate",
        json={"orderid": order_id, "sku": sku1, "qty": 15},
    )

    assert response.status_code == 201
    assert response.json["batchref"] == early_batchref


def test_invalid_sku_returns_400_with_message(api_url, test_app):
    unknown_sku = random_sku("table")
    orderid = random_orderid("spoon")

    client = test_app.test_client()
    response = client.post(
        "/api/allocate",
        json={"orderid": orderid, "sku": unknown_sku, "qty": 100},
    )

    assert response.status_code == 400
    assert response.json["message"] == f"Invalid sku {unknown_sku}"


def test_outofstock_returns_400_with_message(api_url, add_stock, test_app):
    sku = random_sku("table-small")
    small_batchref = random_batchref("table-small")
    large_order_id = random_orderid(1)
    add_stock([(small_batchref, sku, 10, None)])

    client = test_app.test_client()
    response = client.post(
        "/api/allocate",
        json={"orderid": large_order_id, "sku": sku, "qty": 100},
    )

    assert response.status_code == 400
    assert response.json["message"] == f"Sku {sku} is out of stock"
