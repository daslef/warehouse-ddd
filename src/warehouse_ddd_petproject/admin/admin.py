from datetime import date
from flask import Blueprint
from flask import render_template
from flask import request
from flask_login import login_required


from warehouse_ddd_petproject import model, session, unit_of_work


admin = Blueprint("admin", __name__, template_folder="templates")


@admin.route("/batches", methods=["GET", "POST"])
@login_required
def admin_batches_view() -> str:
    uow = unit_of_work.SqlAlchemyUnitOfWork(session.SessionManager())

    if request.method == "POST":
        reference = request.form.get("reference")
        sku = request.form.get("sku")
        qty = int(request.form.get("qty"))
        eta = request.form.get("eta")

        assert isinstance(reference, str)
        assert isinstance(sku, str)

        if eta:
            eta = date(eta)

        with uow:
            uow.batches.add(model.Batch(reference, sku, qty, eta))
            uow.commit()

    batches = uow.batches.list()
    return render_template("admin/batches.html", batches=batches)


@admin.route("/")
@login_required
def admin_view() -> str:
    uow = unit_of_work.SqlAlchemyUnitOfWork(session.SessionManager())
    batches = uow.batches.list()
    allocations = [b.allocations for b in batches]

    return render_template(
        "admin/admin.html", orderlines=allocations, batches=batches
    )
