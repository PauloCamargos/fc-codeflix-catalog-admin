from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestInMemoryCategoryRepository:
    def test_can_save_entity_category(self):
        repository = InMemoryCategoryRepository()

        category = Category(
            name="Dummy",
            description="Dummy description",
            is_active=True,
        )

        repository.save(category=category)

        assert category in repository.categories
        assert len(repository.categories) == 1
