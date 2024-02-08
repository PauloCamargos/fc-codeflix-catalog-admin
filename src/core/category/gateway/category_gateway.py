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
