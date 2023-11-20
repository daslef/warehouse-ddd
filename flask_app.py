from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import repository
import model
import services
import exceptions
from config import build_db_uri
from db_tables import start_mappers, metadata


engine = create_engine(build_db_uri(".env"))
get_session = sessionmaker(bind=engine)

try:
    metadata.create_all(bind=engine)
    start_mappers()
except Exception:
    pass


app = Flask(__name__)


@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    line = model.OrderLine(
        request.json["orderid"], request.json["sku"], request.json["qty"]
    )

    try:
        batchref = services.allocate(line, repo, session)
    except (exceptions.OutOfStock, exceptions.InvalidSku) as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"batchref": batchref}), 201


@app.route("/")
def index():
    return jsonify({"message": "Hello"})


app.run(debug=True)
