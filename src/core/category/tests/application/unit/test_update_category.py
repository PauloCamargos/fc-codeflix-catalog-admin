from unittest.mock import call, create_autospec
from src.core.category.application.update_category import (
    UpdateCategory,
    UpdateCategoryInput,
)
from src.core.category.domain.category import Category

from src.core.category.gateway.category_gateway import AbstractCategoryRepository


class TestUpdateCategory:
    def test_update_category(self):
        category_description = "Movie description"
        category_is_active = False
        category = Category(
            name="Movie",
            description=category_description,
            is_active=category_is_active,
        )

        mocked_repository = create_autospec(AbstractCategoryRepository)
        mocked_repository.get_by_id.return_value = category
        mocked_repository.update.return_value = category

        update_category = UpdateCategory(repository=mocked_repository)

        update_category_input = UpdateCategoryInput(
            id=category.id,
            name="Serie",
        )
        update_category.execute(input=update_category_input)

        assert mocked_repository.update.call_args_list == [
            call(category=category),
        ]

        assert category.name == update_category_input.name
        assert category.description == category_description
        assert category.is_active == category_is_active
