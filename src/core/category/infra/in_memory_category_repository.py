from src.core.category.domain.category import Category
from src.core.category.gateway.category_gateway import (
    AbstractCategoryRepository,
)


class InMemoryCategoryRepository(AbstractCategoryRepository):
    def __init__(self, categories: list[Category] = None) -> None:
        self.categories = categories or []

    def save(self, category: Category) -> None:
        self.categories.append(category)
