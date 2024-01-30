from typing import cast

from flask import Blueprint
from flask import jsonify
from flask import request
from flask import Response

from warehouse_ddd_petproject.infrastructure import (
    session,
)
from warehouse_ddd_petproject.domain import exceptions, model, services, unit_of_work


api = Blueprint("api", __name__)


@api.route("/allocate", methods=["POST"])
def allocate_endpoint() -> tuple[Response, int]:
    uow = unit_of_work.SqlAlchemyUnitOfWork(session.SessionManager())

    orderid = cast(str, request.json["orderid"])
    sku = cast(str, request.json["sku"])
    qty = cast(int, request.json["qty"])

    line = model.OrderLine(orderid, sku, qty)

    try:
        batchref = services.allocate(line, uow)
    except (exceptions.OutOfStock, exceptions.InvalidSku) as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"batchref": batchref}), 201
