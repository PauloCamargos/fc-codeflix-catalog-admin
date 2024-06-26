from unittest.mock import call, create_autospec

from src.core.category.application.list_categories import ListCategories
from src.core.category.domain.category import Category
from src.core.category.gateway.category_gateway import AbstractCategoryRepository


class TestListCategoryIntegration:

    def test_list_categories_empty_success(self) -> None:
        repository = create_autospec(AbstractCategoryRepository)
        repository.list.return_value = []

        list_categories = ListCategories(repository=repository)

        input = ListCategories.Input()
        list_categories_output = list_categories.execute(input=input)

        assert repository.list.call_args_list == [
            call(
                order_by=ListCategories.default_order_by_field,
                page=1,
            ),
        ]

        assert len(list_categories_output.data) == 0

    def test_list_categories_success(self) -> None:
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
        repository = create_autospec(AbstractCategoryRepository)
        repository.list.return_value = [movie_category, serie_category]

        list_categories = ListCategories(repository=repository)

        input = ListCategories.Input()
        list_categories_output = list_categories.execute(input=input)

        assert repository.list.call_args_list == [
            call(
                order_by=ListCategories.default_order_by_field,
                page=1,
            ),
        ]

        assert len(list_categories_output.data) == 2
        (
            found_movie_category_output,
            found_serie_category_output,
        ) = list_categories_output.data

        assert found_movie_category_output.id == movie_category.id
        assert found_movie_category_output.name == movie_category.name
        assert found_movie_category_output.description == movie_category.description
        assert found_movie_category_output.is_active == movie_category.is_active

        assert found_serie_category_output.name == serie_category.name
        assert found_serie_category_output.id == serie_category.id
        assert found_serie_category_output.description == serie_category.description
        assert found_serie_category_output.is_active == serie_category.is_active
