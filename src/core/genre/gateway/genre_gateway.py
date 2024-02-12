from abc import ABC, abstractmethod
from uuid import UUID

from core.genre.domain.genre import Genre


class AbstractGenreRepository(ABC):
    @abstractmethod
    def save(self, genre: Genre) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: UUID) -> Genre | None:
        raise NotImplementedError

    def list_genres(self) -> list[Genre]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, genre: Genre) -> None:
        raise NotImplementedError
