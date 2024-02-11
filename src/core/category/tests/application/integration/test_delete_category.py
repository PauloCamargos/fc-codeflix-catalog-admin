from uuid import uuid4

import pytest
from core.category.application.delete_category import (
    DeleteCategory,
    DeleteCategoryInput,
)
from core.category.application.errors import CategoryNotFound
from core.category.domain.category import Category
from core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestDeleteCategory:
    def test_delete_category_by_id_success(self) -> None:
        movie_category = Category(
            name="Movie",
            description="Movie category",
            is_active=True,
        )
        serie_category = Category(
            name="Serie",
            description="Serie category",
            is_active=True,
        )
        repository = InMemoryCategoryRepository(
            categories=[
                movie_category,
                serie_category,
            ]
        )

        delete_category_input = DeleteCategoryInput(id=movie_category.id)
        delete_category = DeleteCategory(repository=repository)

        delete_category.execute(input=delete_category_input)

        assert repository.categories == [serie_category]

    def test_get_category_by_id_does_not_exist_error(self) -> None:
        movie_category = Category(
            name="Movie",
            description="Movie category",
            is_active=True,
        )
        serie_category = Category(
            name="Serie",
            description="Serie category",
            is_active=True,
        )
        repository = InMemoryCategoryRepository(
            categories=[
                movie_category,
                serie_category,
            ]
        )

        delete_category_input = DeleteCategoryInput(id=uuid4())
        detele_category = DeleteCategory(repository=repository)

        with pytest.raises(CategoryNotFound):
            detele_category.execute(delete_category_input)
