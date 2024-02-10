from unittest.mock import call, create_autospec
from src.core.category.application.update_category import (
    UpdateCategory,
    UpdateCategoryInput,
)
from src.core.category.domain.category import Category

from src.core.category.gateway.category_gateway import AbstractCategoryRepository


class TestUpdateCategory:
    def test_update_category(self):
        original_category_attrs = dict(
            name="Movie",
            description="Movie description",
            is_active=False,
        )
        category = Category(**original_category_attrs)

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
        assert category.description == original_category_attrs["description"]
        assert category.is_active == original_category_attrs["is_active"]

    def test_can_activate_category(self):
        original_category_attrs = dict(
            name="Movie",
            description="Movie description",
            is_active=False,
        )
        category = Category(**original_category_attrs)

        mocked_repository = create_autospec(AbstractCategoryRepository)
        mocked_repository.get_by_id.return_value = category
        mocked_repository.update.return_value = category

        update_category = UpdateCategory(repository=mocked_repository)

        update_category_input = UpdateCategoryInput(
            id=category.id,
            is_active=True,
        )
        update_category.execute(input=update_category_input)

        assert mocked_repository.update.call_args_list == [
            call(category=category),
        ]

        assert category.name == original_category_attrs["name"]
        assert category.description == original_category_attrs["description"]
        assert category.is_active == update_category_input.is_active

    def test_can_deactivate_category(self):
        original_category_attrs = dict(
            name="Movie",
            description="Movie description",
            is_active=True,
        )
        category = Category(**original_category_attrs)

        mocked_repository = create_autospec(AbstractCategoryRepository)
        mocked_repository.get_by_id.return_value = category
        mocked_repository.update.return_value = category

        update_category = UpdateCategory(repository=mocked_repository)

        update_category_input = UpdateCategoryInput(
            id=category.id,
            is_active=False,
        )
        update_category.execute(input=update_category_input)

        assert mocked_repository.update.call_args_list == [
            call(category=category),
        ]

        assert category.name == original_category_attrs["name"]
        assert category.description == original_category_attrs["description"]
        assert category.is_active == update_category_input.is_active
