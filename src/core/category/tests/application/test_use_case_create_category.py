from unittest.mock import MagicMock, call
import pytest
from src.core.category.application.create_category import (
    CreateCategoryInput,
    CreateCategoryUserCase,
)
from src.core.category.application.errors import InvalidCategoryData
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestUseCaseCreateCategory:
    def test_use_case_create_category_with_valid_data_success(self):
        mocked_repository = MagicMock(InMemoryCategoryRepository)
        create_category_use_case = CreateCategoryUserCase(repository=mocked_repository)

        create_category_input = CreateCategoryInput(
            name="Movie",
            description="Movie category",
            is_active=True,
        )

        category_id = create_category_use_case.execute(create_category_input)

        expected_call_args_list = [
            call(
                Category(
                    id=category_id,
                    name=create_category_input.name,
                    description=create_category_input.description,
                    is_active=create_category_input.is_active,
                )
            ),
        ]
        assert mocked_repository.save.call_args_list == expected_call_args_list

        assert category_id is not None, "category_id should not be None"

    def test_use_case_create_category_with_invalid_data_error(self):
        mocked_repository = MagicMock(InMemoryCategoryRepository)
        create_category_use_case = CreateCategoryUserCase(repository=mocked_repository)

        create_category_input = CreateCategoryInput(
            name="",
            description="Movie category",
            is_active=True,
        )

        with pytest.raises(InvalidCategoryData, match="'name' must not be empty"):
            create_category_use_case.execute(create_category_input)

        expected_call_args_list = []
        assert mocked_repository.save.call_args_list == expected_call_args_list
