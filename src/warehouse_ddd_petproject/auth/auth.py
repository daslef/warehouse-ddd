from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import Response
from flask_login import login_user, logout_user

from warehouse_ddd_petproject.infrastructure import session
from .model import User

auth = Blueprint(
    "auth", __name__, static_folder="static", template_folder="templates"
)


@auth.route("/login", methods=["GET", "POST"])
def login() -> str | Response:
    if request.method == "GET":
        return render_template("auth/login.html")

    login_field = request.form.get("email")
    password_field = request.form.get("password")

    user = (
        session.SessionManager()
        .query(User)
        .where(User.username == login_field)
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

    signup_session = session.SessionManager()

    user = (
        signup_session.query(User).where(User.username == email_field).first()
    )

    if user:
        flash("Account already exists. Maybe you want to sign in?", "error")
        return render_template("auth/signup.html")

    signup_session.add(User(email_field, password_field))
    signup_session.commit()

    return redirect("/auth/login")
