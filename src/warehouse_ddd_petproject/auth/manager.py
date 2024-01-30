from flask_login import LoginManager

from warehouse_ddd_petproject.infrastructure import session
from .model import User


def create_manager() -> LoginManager:
    def _load_user(user_id: str) -> User | int:
        return session.SessionManager().get(User, int(user_id))

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.user_loader(_load_user)

    return login_manager
