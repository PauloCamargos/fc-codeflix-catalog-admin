from copy import deepcopy
from uuid import UUID

from src.core.category.domain.category import Category
from src.core.category.gateway.category_gateway import AbstractCategoryRepository


class InMemoryCategoryRepository(AbstractCategoryRepository):
    def __init__(self, categories: list[Category] | None = None) -> None:
        if categories is None:
            self.categories = []
        else:
            self.categories = categories

    def save(self, category: Category) -> None:
        self.categories.append(category)

    def get_by_id(self, id: UUID) -> Category | None:
        return next(
            (
                deepcopy(category)
                for category in self.categories
                if category.id == id
            ),
            None,
        )

    def list(self, order_by: str | None = None) -> list[Category]:
        categories = (
            deepcopy(category)
            for category in self.categories
        )

        if order_by is not None:
            return list(
                sorted(
                    categories,
                    key=lambda category: getattr(category, order_by.strip("-")),
                    reverse=order_by.startswith("-"),
                )
            )

        return list(self.categories)

    def delete(self, id: UUID) -> None:
        category = self.get_by_id(id)
        if category:
            self.categories.remove(category)

    def update(self, category: Category) -> None:
        old_category = self.get_by_id(category.id)
        if old_category:
            self.categories.remove(old_category)
            self.categories.append(category)
