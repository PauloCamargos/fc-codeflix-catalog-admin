from src.core.category.application.update_category import (
    UpdateCategory,
    UpdateCategoryInput,
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestUpdateCategoryIntegration:
    def test_update_category(self):
        category_description = "Movie description"
        category_is_active = False
        category = Category(
            name="Movie",
            description=category_description,
            is_active=category_is_active,
        )

        repository = InMemoryCategoryRepository(categories=[category])

        update_category = UpdateCategory(repository=repository)

        update_category_input = UpdateCategoryInput(
            id=category.id,
            name="Serie",
        )
        update_category.execute(input=update_category_input)

        assert category.name == update_category_input.name
        assert category.description == category_description
        assert category.is_active == category_is_active
