import pytest

from src.core.category.application.list_categories import ListCategories
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)
from src.core.shared.application.errors import InvalidOrderByRequested


@pytest.fixture
def movie_category() -> Category:
    return Category(
        name="Movie",
        description="Movie category",
        is_active=True,
    )


@pytest.fixture
def serie_category() -> Category:
    return Category(
        name="Serie",
        description="Serie category",
        is_active=True,
    )


@pytest.fixture
def category_repository(
    movie_category: Category,
) -> InMemoryCategoryRepository:
    return InMemoryCategoryRepository(
        categories=[movie_category]
    )


class TestListCategoryIntegration:
    def test_list_categories_empty_success(self) -> None:
        repository = InMemoryCategoryRepository(categories=[])

        list_categories = ListCategories(repository=repository)

        input = ListCategories.Input()
        list_categories_output = list_categories.execute(input=input)

        assert len(list_categories_output.data) == 0

    def test_list_categories_no_order_by_success(
        self,
        movie_category: Category,
        category_repository: InMemoryCategoryRepository,
    ) -> None:
        input = ListCategories.Input()

        use_case = ListCategories(repository=category_repository)

        output = use_case.execute(input=input)

        assert len(output.data) == 1
        [found_movie_category_output] = output.data
        assert found_movie_category_output.id == movie_category.id
        assert found_movie_category_output.name == movie_category.name
        assert found_movie_category_output.description == movie_category.description
        assert found_movie_category_output.is_active == movie_category.is_active

    @pytest.mark.parametrize(
            "order_by",
            ["name", "-name", "description", "-description"]
    )
    def test_list_categories_order_by_success(
        self,
        order_by: str,
        movie_category: Category,
        serie_category: Category,
        category_repository: InMemoryCategoryRepository,
    ):
        category_repository.save(category=serie_category)

        input = ListCategories.Input(order_by=order_by)

        use_case = ListCategories(repository=category_repository)

        output = use_case.execute(input=input)

        expected_categories = sorted(
            [
                movie_category,
                serie_category,
            ],
            key=lambda category: getattr(category, order_by.strip("-")),
            reverse=order_by.startswith("-"),
        )

        expected_output = ListCategories.Output(
            data=[
                ListCategories.CategoryOutput(
                    id=category.id,
                    name=category.name,
                    description=category.description,
                    is_active=category.is_active,
                )
                for category in expected_categories
            ]
        )

        assert expected_output == output

    def test_list_categories_invalid_order_by_error(self):
        order_by = "potato"
        valid_order_by_attrs = ", ".join(
            repr(attr)
            for attr in ListCategories.Input.get_valid_order_by_attributes()
        )

        with pytest.raises(
            InvalidOrderByRequested,
            match=(
                f"Provided ordering {repr(order_by)} "
                f"is not one of: {valid_order_by_attrs}"
            ),
        ):
            ListCategories.Input(order_by=order_by)
