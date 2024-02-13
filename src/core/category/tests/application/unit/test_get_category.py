from unittest.mock import MagicMock, call, create_autospec
from uuid import uuid4

import pytest
from src.core.category.application.errors import CategoryNotFound
from src.core.category.application.get_category import (
    GetCategoryInput,
    GetCategoryOutput,
    GetCategory,
)
from src.core.category.domain.category import Category
from src.core.category.gateway.category_gateway import AbstractCategoryRepository


class TestGetCategoryIntegration:

    def test_get_category_by_id_success(self) -> None:
        movie_category = Category(
            name="Movie",
            description="Movie category",
            is_active=True,
        )
        repository = create_autospec(AbstractCategoryRepository)
        repository.get_by_id.return_value = movie_category

        get_category_input = GetCategoryInput(id=movie_category.id)
        get_category = GetCategory(repository=repository)

        get_category_output = get_category.execute(get_category_input)

        assert repository.get_by_id.call_args_list == [
            call(id=movie_category.id),
        ]

        assert get_category_output == GetCategoryOutput(
            id=movie_category.id,
            name=movie_category.name,
            description=movie_category.description,
            is_active=movie_category.is_active,
        )

    def test_get_category_by_id_does_not_exist_error(self) -> None:
        repository = MagicMock(AbstractCategoryRepository)
        repository.get_by_id.return_value = None

        does_not_exist_id = uuid4()
        get_category_input = GetCategoryInput(id=does_not_exist_id)
        get_category = GetCategory(repository=repository)
        with pytest.raises(CategoryNotFound):
            get_category.execute(get_category_input)

        assert repository.get_by_id.call_args_list == [
            call(id=does_not_exist_id),
        ]
