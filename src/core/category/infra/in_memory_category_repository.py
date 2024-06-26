from copy import deepcopy
from math import ceil
from uuid import UUID

from src.core.category.domain.category import Category
from src.core.category.gateway.category_gateway import AbstractCategoryRepository
from src.core.shared import settings as core_settings
from src.core.shared.application.errors import InvalidPageRequested


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

    def list(
        self,
        order_by: str | None = None,
        page: int | None = None,
    ) -> list[Category]:
        sorted_categories = [
            deepcopy(category)
            for category in self.categories
        ]

        if order_by is not None:
            sorted_categories = sorted(
                sorted_categories,
                key=lambda category: getattr(category, order_by.strip("-")),
                reverse=order_by.startswith("-"),
            )

        if page is not None:
            page_size = core_settings.REPOSITORY["page_size"]
            page_offset = (page - 1) * page_size

            num_elements = max(1, self.count())
            if page > ceil(num_elements / page_size):
                raise InvalidPageRequested(page=page)

            return sorted_categories[page_offset:page_offset + page_size]

        return list(sorted_categories)

    def count(self) -> int:
        return len(self.categories)

    def delete(self, id: UUID) -> None:
        category = self.get_by_id(id)
        if category:
            self.categories.remove(category)

    def update(self, category: Category) -> None:
        old_category = self.get_by_id(category.id)
        if old_category:
            self.categories.remove(old_category)
            self.categories.append(category)
