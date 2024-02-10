from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.core.category.domain.category import Category


class AbstractCategoryRepository(ABC):
    @abstractmethod
    def save(self, category: Category) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[Category]:
        raise NotImplementedError

    def list_categories(self) -> list[Category]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, category: Category) -> None:
        raise NotImplementedError
