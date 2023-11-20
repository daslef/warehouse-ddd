import pytest
import httpx

from helpers import random_sku, random_orderid


@pytest.mark.usefixtures("restart_api")
def test_invalid_sku_returns_400_with_message(api_url):
    unknown_sku = random_sku("table")
    orderid = random_orderid("spoon")

    response = httpx.post(
        f"{api_url}/allocate", json={"orderid": orderid, "sku": unknown_sku, "qty": 100}
    )

    assert response.status_code == 400
    assert response.json()["message"] == f"Invalid sku {unknown_sku}"
