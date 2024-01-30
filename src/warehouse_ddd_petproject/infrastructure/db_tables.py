from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
    Table,
    create_engine,
)
from sqlalchemy.orm import registry, relationship

import warehouse_ddd_petproject.auth.model  # FIXME

from warehouse_ddd_petproject.infrastructure import (
    config,
)
from warehouse_ddd_petproject.domain import model


mapper_registry = registry()
metadata = mapper_registry.metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("username", String(255)),
    Column("password_hash", String(255)),
)

order_lines = Table(
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("orderid", String(255)),
    Column("sku", String(255)),
    Column("qty", Integer, nullable=False),
)

batches = Table(
    "batches",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(255)),
    Column("sku", String(255)),
    Column("initial_quantity", Integer, nullable=False),
    Column("eta", Date, nullable=True),
)

allocations = Table(
    "allocations",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("orderline_id", ForeignKey("order_lines.id")),
    Column("batch_id", ForeignKey("batches.id")),
)


def start_mappers() -> None:
    lines_mapper = mapper_registry.map_imperatively(
        model.OrderLine, order_lines
    )
    mapper_registry.map_imperatively(
        model.Batch,
        batches,
        properties={
            "allocations": relationship(
                lines_mapper,
                secondary=allocations,
                collection_class=set,
            )
        },
    )
    mapper_registry.map_imperatively(
        warehouse_ddd_petproject.auth.model.User, users
    )


def create_tables():
    engine = create_engine(config.build_db_uri(".env"))

    try:
        metadata.create_all(bind=engine)
        start_mappers()
    except Exception:
        pass


if __name__ == "__main__":
    create_tables()
    start_mappers()
