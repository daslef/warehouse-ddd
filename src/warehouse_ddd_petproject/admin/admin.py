from flask import Blueprint
from flask import render_template
from flask import request
from flask_login import login_required
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from warehouse_ddd_petproject import config, model, repository


admin = Blueprint("admin", __name__, template_folder="templates")

engine = create_engine(config.build_db_uri(".env"))
get_session = sessionmaker(bind=engine)


@admin.route("/batches", methods=["GET", "POST"])
@login_required
def admin_batches_view():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)

    if request.method == "POST":
        reference = request.form.get("reference")
        sku = request.form.get("sku")
        qty = request.form.get("qty")
        eta = request.form.get("eta")

        repo.add(model.Batch(reference, sku, qty, eta))
        session.commit()

    batches = repo.list()
    return render_template("admin/batches.html", batches=batches)


@admin.route("/")
@login_required
def admin_view():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    batches = repo.list()
    allocations = [b.allocations for b in batches]

    return render_template(
        "admin/admin.html", orderlines=allocations, batches=batches
    )
