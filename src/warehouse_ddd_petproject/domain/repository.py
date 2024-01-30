from abc import ABC
from abc import abstractmethod

from sqlalchemy.orm import Session

from warehouse_ddd_petproject.domain import model


class AbstractRepository(ABC):
    @abstractmethod
    def add(self, batch: model.Batch) -> None:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def get(self, reference: str) -> model.Batch:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[model.Batch]:  # pragma: no cover
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session: Session) -> None:
        self.__session = session

    def add(self, batch: model.Batch) -> None:
        self.__session.add(batch)

    def get(self, reference: str) -> model.Batch:
        batches = self.__session.query(model.Batch)
        return batches.filter_by(reference=reference).first()

    def list(self) -> list[model.Batch]:
        return self.__session.query(model.Batch).all()


class FakeRepository(AbstractRepository):
    def __init__(self, batches: list[model.Batch]) -> None:
        self.__batches = set(batches)

    def add(self, batch: model.Batch) -> None:
        self.__batches.add(batch)

    def get(self, reference: str) -> model.Batch:
        return [b for b in self.__batches if b.reference == reference][0]

    def list(self) -> list[model.Batch]:
        return list(self.__batches)
