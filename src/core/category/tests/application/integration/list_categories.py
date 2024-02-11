from core.category.application.list_categories import (
    ListCategories,
    ListCategoryInput,
)
from core.category.domain.category import Category
from core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestListCategoryIntegration:
    def test_list_categories_empty_success(self) -> None:
        repository = InMemoryCategoryRepository(categories=[])

        list_categories = ListCategories(repository=repository)

        input = ListCategoryInput()
        list_categories_output = list_categories.execute(input=input)

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
        repository = InMemoryCategoryRepository(
            categories=[movie_category, serie_category]
        )

        list_categories = ListCategories(repository=repository)

        input = ListCategoryInput()
        list_categories_output = list_categories.execute(input=input)

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
