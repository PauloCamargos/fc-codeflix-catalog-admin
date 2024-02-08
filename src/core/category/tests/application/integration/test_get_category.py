import pytest
from src.core.category.application.get_category import (
    GetCategoryInput,
    GetCategoryUserCase,
)
from src.core.category.application.errors import InvalidCategoryData
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestGetCategoryIntegration:

    def test_get_category_with_valid_data_success(self) -> None:
        repository = InMemoryCategoryRepository()
        get_category = GetCategoryUserCase(repository=repository)

        get_category_input = GetCategoryInput(
            name="Movie",
            description="Movie category",
            is_active=True,
        )

        get_category_output = get_category.execute(get_category_input)

        assert get_category_output.id is not None, "category_id should not be None"
        assert len(repository.categories) == 1
        [saved_category] = repository.categories
        assert saved_category.id == get_category_output.id
        assert saved_category.name == get_category_input.name
        assert saved_category.description == get_category_input.description
        assert saved_category.is_active == get_category_input.is_active

    def test_get_category_with_invalid_data_error(self) -> None:
        repository = InMemoryCategoryRepository()
        get_category = GetCategoryUserCase(repository=repository)

        get_category_input = GetCategoryInput(
            name="",
            description="Movie category",
            is_active=True,
        )

        with pytest.raises(InvalidCategoryData, match="'name' must not be empty"):
            get_category.execute(get_category_input)

        assert len(repository.categories) == 0
