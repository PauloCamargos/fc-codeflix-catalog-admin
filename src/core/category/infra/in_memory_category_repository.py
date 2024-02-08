from src.core.category.domain.category import Category


class InMemoryCategoryRepository:
    def __init__(self, categories: list[Category] = None):
        self.categories = categories or []

    def save(self, category: Category):
        self.categories.append(category)
