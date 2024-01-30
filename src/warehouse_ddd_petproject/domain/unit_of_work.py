from typing import Self
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from warehouse_ddd_petproject.domain.repository import (
    SqlAlchemyRepository,
    FakeRepository,
)


class AbstractUnitOfWork(ABC):
    @abstractmethod
    def __enter__(self) -> Self:
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, **kw) -> None:
        raise NotImplementedError

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session: Session) -> None:
        self._session = session
        self.batches = SqlAlchemyRepository(self._session)

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args, **kwargs) -> None:
        self._session.rollback()

    def commit(self) -> None:
        self._session.commit()


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self, repository: FakeRepository) -> None:
        self.batches = repository
        self.committed = False

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args, **kwargs) -> None:
        self.committed = False

    def commit(self) -> None:
        self.committed = True
