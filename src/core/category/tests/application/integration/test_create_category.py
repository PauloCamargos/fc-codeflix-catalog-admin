import pytest
from src.core.category.application.create_category import (
    CreateCategoryInput,
    CreateCategory,
)
from src.core.category.application.errors import InvalidCategoryData
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestCreateCategoryIntegration:

    def test_create_category_with_valid_data_success(self) -> None:
        repository = InMemoryCategoryRepository()
        create_category = CreateCategory(repository=repository)

        create_category_input = CreateCategoryInput(
            name="Movie",
            description="Movie category",
            is_active=True,
        )

        create_category_output = create_category.execute(create_category_input)

        assert create_category_output.id is not None, "category_id should not be None"
        assert len(repository.categories) == 1
        [saved_category] = repository.categories
        assert saved_category.id == create_category_output.id
        assert saved_category.name == create_category_input.name
        assert saved_category.description == create_category_input.description
        assert saved_category.is_active == create_category_input.is_active

    def test_create_category_with_invalid_data_error(self) -> None:
        repository = InMemoryCategoryRepository()
        create_category = CreateCategory(repository=repository)

        create_category_input = CreateCategoryInput(
            name="",
            description="Movie category",
            is_active=True,
        )

        with pytest.raises(InvalidCategoryData, match="'name' must not be empty"):
            create_category.execute(create_category_input)

        assert len(repository.categories) == 0
