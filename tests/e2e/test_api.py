import pytest
import httpx

from helpers import random_sku, random_orderid, random_batchref


@pytest.mark.usefixtures("restart_api")
def test_returns_allocation_on_valid_sku(add_stock, api_url):
    sku1 = random_sku("spoons")
    sku2 = random_sku("other")

    early_batchref = random_batchref(1)
    later_batchref = random_batchref(2)
    other_batchref = random_batchref(3)

    order_id = random_orderid("spoons")

    add_stock(
        [
            (early_batchref, sku1, 20, "2024-01-02"),
            (later_batchref, sku1, 20, "2024-02-02"),
            (other_batchref, sku2, 20, None),
        ]
    )

    response = httpx.post(
        f"{api_url}/allocate", json={"orderid": order_id, "sku": sku1, "qty": 15}
    )

    assert response.status_code == 201
    assert response.json()["batchref"] == early_batchref


@pytest.mark.usefixtures("restart_api")
def test_invalid_sku_returns_400_with_message(api_url):
    unknown_sku = random_sku("table")
    orderid = random_orderid("spoon")

    response = httpx.post(
        f"{api_url}/allocate", json={"orderid": orderid, "sku": unknown_sku, "qty": 100}
    )

    assert response.status_code == 400
    assert response.json()["message"] == f"Invalid sku {unknown_sku}"


@pytest.mark.usefixtures("restart_api")
def test_outofstock_returns_400_with_message(api_url, add_stock):
    sku = random_sku("table-small")
    small_batchref = random_batchref("table-small")
    large_order_id = random_orderid(1)
    add_stock([(small_batchref, sku, 10, None)])

    response = httpx.post(
        f"{api_url}/allocate", json={"orderid": large_order_id, "sku": sku, "qty": 100}
    )

    assert response.status_code == 400
    assert response.json()["message"] == f"Sku {sku} is out of stock"
