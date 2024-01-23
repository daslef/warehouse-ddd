from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import Response
from flask_login import login_user
from flask_login import logout_user
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from warehouse_ddd_petproject import config, model


auth = Blueprint(
    "auth", __name__, static_folder="static", template_folder="templates"
)

engine = create_engine(config.build_db_uri(".env"))
get_session = sessionmaker(bind=engine)


@auth.route("/login", methods=["GET", "POST"])
def login() -> str | Response:
    if request.method == "GET":
        return render_template("auth/login.html")

    login_field = request.form.get("email")
    password_field = request.form.get("password")

    session = get_session()
    user = (
        session.query(model.User)
        .where(model.User.username == login_field)
        .first()
    )

    if user and user.check_password(password_field):
        login_user(user)
        return redirect("/admin")

    flash("Invalid login or password. Try again", "error")
    return render_template("auth/login.html")


@auth.route("/logout")
def logout() -> Response:
    logout_user()
    return redirect("/auth/login")


@auth.route("/signup", methods=["GET", "POST"])
def signup() -> str | Response:
    if request.method == "GET":
        return render_template("auth/signup.html")

    email_field = request.form.get("email", "")
    password_field = request.form.get("password", "")

    session = get_session()
    user = (
        session.query(model.User)
        .where(model.User.username == email_field)
        .first()
    )

    if user:
        flash("Account already exists. Maybe you want to sign in?", "error")
        return render_template("auth/signup.html")

    session.add(model.User(email_field, password_field))
    session.commit()

    return redirect("/auth/login")
