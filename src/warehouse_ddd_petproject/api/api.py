from typing import cast

from flask import Blueprint
from flask import jsonify
from flask import request
from flask import Response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from warehouse_ddd_petproject import config
from warehouse_ddd_petproject import exceptions
from warehouse_ddd_petproject import model
from warehouse_ddd_petproject import repository
from warehouse_ddd_petproject import services


engine = create_engine(config.build_db_uri(".env"))
get_session = sessionmaker(bind=engine)

api = Blueprint("api", __name__)


@api.route("/allocate", methods=["POST"])
def allocate_endpoint() -> tuple[Response, int]:
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)

    orderid = cast(str, request.json["orderid"])
    sku = cast(str, request.json["sku"])
    qty = cast(int, request.json["qty"])

    line = model.OrderLine(orderid, sku, qty)

    try:
        batchref = services.allocate(line, repo, session)
    except (exceptions.OutOfStock, exceptions.InvalidSku) as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"batchref": batchref}), 201
