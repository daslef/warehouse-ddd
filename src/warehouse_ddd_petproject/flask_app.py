from flask import Flask
from sqlalchemy import create_engine
from werkzeug.security import gen_salt

from warehouse_ddd_petproject import config, db_tables
from warehouse_ddd_petproject.admin.admin import admin
from warehouse_ddd_petproject.api.api import api
from warehouse_ddd_petproject.auth.auth import auth
from warehouse_ddd_petproject.auth.manager import create_manager


def create_app(test_config: bool = False) -> Flask:
    engine = create_engine(config.build_db_uri(".env"))

    try:
        db_tables.metadata.create_all(bind=engine)
        db_tables.start_mappers()
    except Exception:
        pass

    app = Flask(__name__)
    app.secret_key = gen_salt(20)

    login_manager = create_manager()
    login_manager.init_app(app)

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(admin, url_prefix="/admin")
    app.register_blueprint(api, url_prefix="/api")

    return app
