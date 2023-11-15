from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import repository
import model
from config import build_db_uri
from db_tables import start_mappers
from allocate import allocate

try:
    start_mappers()
except Exception:
    pass

engine = create_engine(build_db_uri(".env"))
get_session = sessionmaker(bind=engine)

app = Flask(__name__)


@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)

    line = model.OrderLine(
        request.json["orderid"], request.json["sku"], request.json["qty"]
    )

    print(line)

    batches = repo.list()
    batchref = allocate(line, batches)

    return jsonify({"batchref": batchref}), 201


@app.route("/")
def index():
    return jsonify({"message": "Hello"})


app.run(debug=True)
