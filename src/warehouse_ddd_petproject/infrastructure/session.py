from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from warehouse_ddd_petproject.infrastructure import config


class SessionManager:
    session = None

    def __new__(cls):
        if cls.session:
            return cls.session

        engine = create_engine(config.build_db_uri(".env"))
        cls.session = scoped_session(sessionmaker(bind=engine))

        return cls.session()
