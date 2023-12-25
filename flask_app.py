from flask import Flask, jsonify, request, render_template, redirect, flash
from flask_login import LoginManager, login_required, login_user, logout_user
from werkzeug.security import gen_salt
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

login_manager = LoginManager()
login_manager.login_view = "login"

app = Flask(__name__)
app.secret_key = gen_salt(20)

login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id: str):
    session = get_session()
    return session.get(model.User, int(user_id))


@app.route("/admin/batches", methods=["GET", "POST"])
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
    return render_template("batches.html", batches=batches)


@app.route("/admin")
@login_required
def admin_view():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    batches = repo.list()
    allocations = [b.allocations for b in batches]

    return render_template("admin.html", orderlines=allocations, batches=batches)


@app.route("/api/allocate", methods=["POST"])
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


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    login_field = request.form.get("email")
    password_field = request.form.get("password")

    session = get_session()
    user = session.query(model.User).where(model.User.username == login_field).first()

    if user and user.check_password(password_field):
        login_user(user)
        return redirect("/admin")

    flash("Invalid login or password. Try again", "error")
    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    login_field = request.form.get("email")
    password_field = request.form.get("password")

    session = get_session()
    user = session.query(model.User).where(model.User.username == login_field).first()

    if user:
        flash("Account already exists. Maybe you want to sign in?", "error")
        return render_template("signup.html")

    session.add(model.User(login_field, password_field))
    session.commit()

    return redirect("/login")


@app.route("/")
def index():
    return jsonify({"message": "Hello"})


app.run(debug=True)
