from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
import model


class AbstractRepository(ABC):
    @abstractmethod
    def add(self, batch: model.Batch):
        raise NotImplementedError

    @abstractmethod
    def get(self, reference: str):
        raise NotImplementedError

    @abstractmethod
    def list(self):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.__session = session

    def add(self, batch: model.Batch):
        self.__session.add(batch)

    def get(self, reference: str):
        batches = self.__session.query(model.Batch)
        return batches.filter_by(reference=reference).one()

    def list(self):
        return self.__session.query(model.Batch).all()


class FakeRepository(AbstractRepository):
    def __init__(self, batches: list[model.Batch] = []):
        self.__batches = set(batches)

    def add(self, batch: model.Batch):
        self.__batches.add(batch)

    def get(self, reference: str):
        return [b for b in self.__batches if b.reference == reference][0]

    def list(self):
        return list(self.__batches)
