from dataclasses import asdict
from unittest.mock import MagicMock, create_autospec
from uuid import uuid4

import pytest

from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)
from src.core.genre.application.errors import (
    GenreNotFound,
    InvalidGenreData,
    RelatedCategoriesNotFound,
)
from src.core.genre.application.update_genre import UpdateGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")


@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")


@pytest.fixture
def sci_fi_genre(
    movie_category: Category,
    documentary_category: Category,
) -> Genre:
    return Genre(
        name="Sci-fi",
        categories=[movie_category.id, documentary_category.id],
    )


@pytest.fixture
def mocked_genre_repository(sci_fi_genre: Genre) -> MagicMock:
    return create_autospec(InMemoryGenreRepository)


@pytest.fixture
def mocked_category_repository(
    movie_category: Category,
    documentary_category: Category,
) -> MagicMock:
    mocked_repository = create_autospec(InMemoryCategoryRepository)
    mocked_repository.list.return_value = [
        movie_category,
        documentary_category,
    ]
    return mocked_repository


class TestUpdateGenre:

    def test_update_genre_does_not_exist_error(
        self,
        mocked_genre_repository: MagicMock,
        mocked_category_repository: MagicMock,
    ):
        mocked_genre_repository.get_by_id.return_value = None

        non_existent_id = uuid4()
        input = UpdateGenre.Input(
            id=non_existent_id,
            name="Science Fiction",
        )

        update_genre = UpdateGenre(
            repository=mocked_genre_repository,
            category_repository=mocked_category_repository,
        )

        with pytest.raises(GenreNotFound):
            update_genre.execute(input=input)

        mocked_genre_repository.get_by_id.assert_called_with(id=non_existent_id)
        mocked_genre_repository.update.assert_not_called()

    def test_update_genre_with_non_existing_categories_error(
        self,
        sci_fi_genre: Genre,
        mocked_genre_repository: MagicMock,
        mocked_category_repository: MagicMock,
    ):
        mocked_genre_repository.get_by_id.return_value = sci_fi_genre

        non_existing_category_id = uuid4()
        input = UpdateGenre.Input(
            id=sci_fi_genre.id, categories=[non_existing_category_id]
        )

        update_genre = UpdateGenre(
            repository=mocked_genre_repository,
            category_repository=mocked_category_repository,
        )

        original_sci_fi_categories = sci_fi_genre.categories

        with pytest.raises(RelatedCategoriesNotFound) as exc_info:
            update_genre.execute(input=input)

        mocked_genre_repository.get_by_id.assert_called_with(id=sci_fi_genre.id)
        mocked_category_repository.list.assert_called_once_with()
        mocked_genre_repository.update.assert_not_called()

        assert str(non_existing_category_id) in str(exc_info.value)
        assert sci_fi_genre.categories == original_sci_fi_categories

    def test_update_genre_with_invalid_name(
        self,
        sci_fi_genre: Genre,
        mocked_genre_repository: MagicMock,
        mocked_category_repository: MagicMock,
    ):
        mocked_genre_repository.get_by_id.return_value = sci_fi_genre

        input = UpdateGenre.Input(
            id=sci_fi_genre.id,
            name="",
        )

        update_genre = UpdateGenre(
            repository=mocked_genre_repository,
            category_repository=mocked_category_repository,
        )

        with pytest.raises(InvalidGenreData):
            update_genre.execute(input=input)

        mocked_genre_repository.get_by_id.assert_called_with(id=sci_fi_genre.id)
        mocked_genre_repository.update.assert_not_called()

    def test_update_genre_with_valid_data_success(
        self,
        sci_fi_genre: Genre,
        movie_category: Category,
        mocked_genre_repository: MagicMock,
        mocked_category_repository: MagicMock,
    ):
        mocked_genre_repository.get_by_id.return_value = sci_fi_genre

        input = UpdateGenre.Input(
            id=sci_fi_genre.id,
            name="Science Fiction",
            categories=[movie_category.id],
            is_active=not sci_fi_genre.is_active,
        )

        update_genre = UpdateGenre(
            repository=mocked_genre_repository,
            category_repository=mocked_category_repository,
        )

        update_genre.execute(input=input)

        mocked_genre_repository.get_by_id.assert_called_with(id=sci_fi_genre.id)
        mocked_category_repository.list.assert_called_with()
        mocked_genre_repository.update.assert_called_once_with(
            genre=Genre(**asdict(input))
        )
