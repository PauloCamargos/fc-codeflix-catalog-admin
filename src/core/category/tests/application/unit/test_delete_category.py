from unittest.mock import call, create_autospec
from uuid import uuid4

import pytest
from src.core.category.application.delete_category import (
    DeleteCategory,
    DeleteCategoryInput,
)
from src.core.category.application.errors import CategoryNotFound
from src.core.category.domain.category import Category
from src.core.category.gateway.category_gateway import AbstractCategoryRepository


class TestDeleteCategory:

    def test_delete_category_success(self):
        category = Category(
            name="Movie",
            description="Movie category",
            is_active=True,
        )

        mocked_repository = create_autospec(AbstractCategoryRepository)
        mocked_repository.get_by_id.return_value = category

        delete_category = DeleteCategory(repository=mocked_repository)

        input = DeleteCategoryInput(id=category.id)
        delete_category.execute(input=input)

        assert mocked_repository.get_by_id.call_args_list == [call(id=category.id)]
        assert mocked_repository.delete.call_args_list == [call(id=category.id)]

    def test_delete_category_does_not_exist_error(self):

        mocked_repository = create_autospec(AbstractCategoryRepository)
        mocked_repository.get_by_id.return_value = None

        delete_category = DeleteCategory(repository=mocked_repository)

        does_not_exist_id = uuid4()
        input = DeleteCategoryInput(id=does_not_exist_id)
        with pytest.raises(CategoryNotFound):
            delete_category.execute(input=input)

        assert mocked_repository.get_by_id.call_args_list == [
            call(id=does_not_exist_id)
        ]
        assert mocked_repository.delete.call_args_list == []
