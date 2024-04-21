from abc import ABC, abstractmethod
from uuid import UUID

from src.core.category.domain.category import Category


class AbstractCategoryRepository(ABC):
    @abstractmethod
    def save(self, category: Category) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: UUID) -> Category | None:
        raise NotImplementedError

    def list(self, order_by: str | None = None) -> list[Category]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, category: Category) -> None:
        raise NotImplementedError
