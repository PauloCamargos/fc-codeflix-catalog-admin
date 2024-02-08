from unittest.mock import MagicMock, call
import pytest
from src.core.category.application.create_category import (
    CreateCategoryInput,
    CreateCategory,
)
from src.core.category.application.errors import InvalidCategoryData
from src.core.category.domain.category import Category
from src.core.category.gateway.category_gateway import AbstractCategoryRepository


class TestCreateCategory:
    def test_create_category_with_valid_data_success(self) -> None:
        mocked_repository = MagicMock(AbstractCategoryRepository)
        create_category = CreateCategory(repository=mocked_repository)

        create_category_input = CreateCategoryInput(
            name="Movie",
            description="Movie category",
            is_active=True,
        )

        create_category_output = create_category.execute(create_category_input)

        expected_call_args_list = [
            call(
                Category(
                    id=create_category_output.id,
                    name=create_category_input.name,
                    description=create_category_input.description,
                    is_active=create_category_input.is_active,
                )
            ),
        ]
        assert mocked_repository.save.call_args_list == expected_call_args_list

        assert create_category_output.id is not None, "category_id should not be None"

    def test_create_category_with_invalid_data_error(self) -> None:
        mocked_repository = MagicMock(AbstractCategoryRepository)
        create_category = CreateCategory(repository=mocked_repository)

        create_category_input = CreateCategoryInput(
            name="",
            description="Movie category",
            is_active=True,
        )

        with pytest.raises(InvalidCategoryData, match="'name' must not be empty"):
            create_category.execute(create_category_input)

        assert mocked_repository.save.call_args_list == []
