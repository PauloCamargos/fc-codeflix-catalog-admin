import pytest
from src.core.category.application.create_category import create_category_use_case
from src.core.category.application.errors import InvalidCategoryData


class TestUseCaseCreateCategory:
    def test_use_case_create_category_with_valid_data_success(self):
        input = dict(
            name="Movie",
            description="Movie category",
            is_active=True,
        )

        category_id = create_category_use_case(**input)

        assert category_id is not None, "category_id should not be None"

    def test_use_case_create_category_with_invalid_data_error(self):
        input = dict(
            name="",
            description="Movie category",
            is_active=True,
        )

        with pytest.raises(InvalidCategoryData, match="'name' must not be empty"):
            create_category_use_case(**input)
