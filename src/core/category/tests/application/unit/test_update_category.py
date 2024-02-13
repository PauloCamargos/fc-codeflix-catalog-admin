from unittest.mock import call, create_autospec

import pytest

from src.core.category.application.errors import InvalidCategoryData
from src.core.category.application.update_category import (
    UpdateCategory,
    UpdateCategoryInput,
)
from src.core.category.domain.category import Category
from src.core.category.gateway.category_gateway import AbstractCategoryRepository


class TestUpdateCategory:
    def test_update_category_success(self):
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
            description="",
        )
        update_category.execute(input=update_category_input)

        assert mocked_repository.get_by_id.call_args_list == [
            call(id=category.id),
        ]
        assert mocked_repository.update.call_args_list == [
            call(category=category),
        ]

        assert category.name == update_category_input.name
        assert category.description == update_category_input.description
        assert category.is_active == original_category_attrs["is_active"]

    def test_update_category_invalid_data_error(self):
        category = Category(
            name="Movie",
            description="Movie description",
            is_active=False,
        )

        mocked_repository = create_autospec(AbstractCategoryRepository)
        mocked_repository.get_by_id.return_value = category

        update_category = UpdateCategory(repository=mocked_repository)

        update_category_input = UpdateCategoryInput(
            id=category.id,
            name="",
        )
        with pytest.raises(InvalidCategoryData, match="'name' must not be empty"):
            update_category.execute(input=update_category_input)

        assert mocked_repository.get_by_id.call_args_list == [
            call(id=category.id),
        ]
        assert mocked_repository.update.call_args_list == []

    def test_can_activate_category_success(self):
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

    def test_can_deactivate_category_success(self):
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
