from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import model
import services
from repository import SqlAlchemyRepository
from config import build_db_uri
from db_tables import start_mappers, metadata

engine = create_engine(build_db_uri(".env"))
get_session = sessionmaker(bind=engine)

try:
    metadata.create_all(bind=engine)
    start_mappers()
except Exception:
    pass


def seed_db():
    session = get_session()
    repo = SqlAlchemyRepository(session)

    lines = (
        model.OrderLine("table-001", "table", 10),
        model.OrderLine("table-001", "table", 30),
        model.OrderLine("table-001", "table", 20),
        model.OrderLine("chair-005", "chair", 5),
        model.OrderLine("chair-005", "chair", 3),
    )

    batch_tables = model.Batch("batch-001", "table", 100, None)
    batch_chairs = model.Batch("batch-002", "chair", 20, None)

    repo.add(batch_tables)
    repo.add(batch_chairs)

    session.add(model.User("test@gmail.com", "testpassword"))

    session.commit()

    for line in lines:
        services.allocate(line, repo, session)


seed_db()
