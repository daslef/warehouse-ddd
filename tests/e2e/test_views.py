from flask_login import FlaskLoginClient
from warehouse_ddd_petproject import model


def test_admin_dashboard(test_app, postgres_session):
    admin_user = (
        postgres_session.query(model.User)
        .where(model.User.username == "test@gmail.com")
        .first()
    )

    test_app.test_client_class = FlaskLoginClient

    with test_app.test_client(
        user=admin_user, fresh_login=False
    ) as test_client:
        response = test_client.get(
            "/admin",
            follow_redirects=True,
        )

    assert response.request.path == "/admin/"


def test_admin_batches_get(test_app, postgres_session):
    admin_user = (
        postgres_session.query(model.User)
        .where(model.User.username == "test@gmail.com")
        .first()
    )

    test_app.test_client_class = FlaskLoginClient

    with test_app.test_client(
        user=admin_user, fresh_login=False
    ) as test_client:
        response = test_client.get(
            "/admin/batches",
            follow_redirects=True,
        )

    assert response.request.path == "/admin/batches"


def test_admin_batches_post(test_app, postgres_session):
    admin_user = (
        postgres_session.query(model.User)
        .where(model.User.username == "test@gmail.com")
        .first()
    )

    test_app.test_client_class = FlaskLoginClient

    with test_app.test_client(
        user=admin_user, fresh_login=False
    ) as test_client:
        response = test_client.post(
            "/admin/batches",
            data={
                "reference": "batch-test",
                "sku": "table-test",
                "qty": 10,
                "eta": None,
            },
            follow_redirects=True,
        )

        assert b"Batches" in response.data
        assert b"batch-test" in response.data
        assert b"table-test" in response.data
        assert b"10" in response.data


def test_auth_login_get(test_app):
    test_client = test_app.test_client()
    response = test_client.get("/auth/login")

    assert b"Login" in response.data


def test_auth_login_success_for_existing_user(test_app):
    test_client = test_app.test_client()
    response = test_client.post(
        "/auth/login",
        data={"email": "test@gmail.com", "password": "testpassword"},
        follow_redirects=True,
    )

    assert response.request.path == "/admin/"


def test_auth_login_error_for_unknown_user(test_app):
    test_client = test_app.test_client()
    response = test_client.post(
        "/auth/login",
        data={"email": "unknown@gmail.com", "password": "testpassword"},
    )

    assert b"Invalid login or password. Try again" in response.data
