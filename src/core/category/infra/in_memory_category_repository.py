from typing import Optional
from uuid import UUID
from src.core.category.domain.category import Category
from src.core.category.gateway.category_gateway import (
    AbstractCategoryRepository,
)


class InMemoryCategoryRepository(AbstractCategoryRepository):
    def __init__(self, categories: list[Category] | None = None) -> None:
        if categories is None:
            self._categories: dict[UUID, Category] = {}
        else:
            self._categories = {
                category.id: category
                for category in categories
            }

    @property
    def categories(self) -> list[Category]:
        return list(self._categories.values())

    def save(self, category: Category) -> None:
        self._categories[category.id] = category

    def get_by_id(self, id: UUID) -> Optional[Category]:
        return self._categories.get(id)

    def delete(self, id: UUID) -> None:
        if id in self._categories:
            del self._categories[id]
