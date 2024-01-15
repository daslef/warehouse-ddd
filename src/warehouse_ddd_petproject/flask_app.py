from api.api import api
from auth.auth import auth
from config import build_db_uri
from db_tables import metadata
from db_tables import start_mappers
from flask import Flask
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import gen_salt

from warehouse_ddd_petproject import model
from warehouse_ddd_petproject.admin import admin


engine = create_engine(build_db_uri(".env"))
get_session = sessionmaker(bind=engine)

try:
    metadata.create_all(bind=engine)
    start_mappers()
except Exception:
    pass

login_manager = LoginManager()
login_manager.login_view = "auth.login"

app = Flask(__name__)
app.secret_key = gen_salt(20)

login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id: str):
    session = get_session()
    return session.get(model.User, int(user_id))


app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(api, url_prefix="/api")
