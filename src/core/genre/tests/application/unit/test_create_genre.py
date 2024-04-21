import uuid
from unittest.mock import create_autospec

import pytest

from src.core.category.domain.category import Category
from src.core.category.gateway.category_gateway import AbstractCategoryRepository
from src.core.genre.application.create_genre import CreateGenre
from src.core.genre.application.errors import (
    InvalidGenreData,
    RelatedCategoriesNotFound,
)
from src.core.genre.domain.genre import Genre
from src.core.genre.gateway.genre_gateway import AbstractGenreRepository


@pytest.fixture
def mocked_genre_repository() -> AbstractGenreRepository:
    return create_autospec(AbstractGenreRepository)


@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")


@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")


@pytest.fixture
def mocked_category_repository_with_categories(
    movie_category,
    documentary_category,
) -> AbstractCategoryRepository:
    repository = create_autospec(AbstractCategoryRepository)
    repository.list_categories.return_value = [movie_category, documentary_category]
    return repository


@pytest.fixture
def mocked_empty_category_repository() -> AbstractCategoryRepository:
    repository = create_autospec(AbstractCategoryRepository)
    repository.list_categories.return_value = []
    return repository


class TestCreateGenre:
    def test_create_genre_with_non_existing_categories_error(
        self,
        mocked_empty_category_repository,
        mocked_genre_repository,
    ):
        use_case = CreateGenre(
            repository=mocked_genre_repository,
            category_repository=mocked_empty_category_repository,
        )

        with pytest.raises(
            RelatedCategoriesNotFound, match="Categories not found: "
        ) as exc:
            category_id = uuid.uuid4()
            use_case.execute(
                CreateGenre.Input(
                    name="Romance",
                    categories={category_id},
                )
            )

        mocked_empty_category_repository.list_categories.assert_called_once_with()
        mocked_genre_repository.save.assert_not_called()
        assert str(category_id) in str(exc.value)

    def test_when_created_genre_is_invalid_then_raise_invalid_genre(
        self,
        documentary_category,
        movie_category,
        mocked_category_repository_with_categories,
        mocked_genre_repository,
    ) -> None:
        use_case = CreateGenre(
            repository=mocked_genre_repository,
            category_repository=mocked_category_repository_with_categories,
        )

        with pytest.raises(InvalidGenreData, match="'name' must not be empty"):
            use_case.execute(
                CreateGenre.Input(
                    name="",
                    categories={documentary_category.id, movie_category.id},
                )
            )

        mocked_category_repository_with_categories.list_categories.assert_called_with()
        mocked_genre_repository.save.assert_not_called()

    def test_when_created_genre_is_valid_and_categories_exist_then_save_genre(
        self,
        documentary_category,
        movie_category,
        mocked_category_repository_with_categories,
        mocked_genre_repository,
    ):
        use_case = CreateGenre(
            repository=mocked_genre_repository,
            category_repository=mocked_category_repository_with_categories,
        )

        output = use_case.execute(
            CreateGenre.Input(
                name="Romance",
                categories={documentary_category.id, movie_category.id},
            )
        )

        assert output == CreateGenre.Output(id=output.id)
        mocked_category_repository_with_categories.list_categories.assert_called_with()
        mocked_genre_repository.save.assert_called_once_with(
            Genre(
                id=output.id,
                name="Romance",
                is_active=True,
                categories=[documentary_category.id, movie_category.id],
            )
        )

    def test_create_genre_without_categories(
        self,
        mocked_genre_repository,
        mocked_category_repository_with_categories,
    ):
        use_case = CreateGenre(
            repository=mocked_genre_repository,
            category_repository=mocked_category_repository_with_categories,
        )

        output = use_case.execute(
            CreateGenre.Input(
                name="Romance",
            )
        )

        mocked_category_repository_with_categories.list_categories.assert_called_with()

        assert output == CreateGenre.Output(id=output.id)
        mocked_genre_repository.save.assert_called_once_with(
            Genre(
                id=output.id,
                name="Romance",
                is_active=True,
                categories=list(),
            )
        )
