from unittest.mock import MagicMock, create_autospec
from uuid import uuid4
import pytest

from src.core.category.domain.category import Category
from src.core.genre.application.delete_genre import DeleteGenre
from src.core.genre.application.errors import GenreNotFound
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")


@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")


@pytest.fixture
def romance_genre(
    movie_category: Category,
    documentary_category: Category,
) -> Genre:
    return Genre(
        name="Romance",
        categories={movie_category.id, documentary_category.id},
    )


@pytest.fixture
def horror_genre(
    movie_category: Category,
    documentary_category: Category,
) -> Genre:
    return Genre(
        name="Horror",
        categories={movie_category.id, documentary_category.id},
    )


@pytest.fixture
def mocked_genre_repository() -> MagicMock:
    mocked_repository = create_autospec(InMemoryGenreRepository)
    return mocked_repository


class TestDeleteGenre:
    def test_delete_genre_by_id_success(
        self,
        romance_genre: Genre,
        mocked_genre_repository: MagicMock,
    ):
        mocked_genre_repository.get_by_id.return_value = romance_genre

        input = DeleteGenre.Input(id=romance_genre.id)
        delete_genre = DeleteGenre(repository=mocked_genre_repository)

        delete_genre.execute(input=input)

        mocked_genre_repository.get_by_id.assert_called_once_with(id=romance_genre.id)
        mocked_genre_repository.delete.assert_called_once_with(id=romance_genre.id)

    def test_delete_genre_does_not_exist_error(
        self,
    ):
        mocked_genre_repository = create_autospec(InMemoryGenreRepository)
        mocked_genre_repository.get_by_id.return_value = None

        non_existing_id = uuid4()
        input = DeleteGenre.Input(id=non_existing_id)
        delete_genre = DeleteGenre(repository=mocked_genre_repository)

        with pytest.raises(GenreNotFound):
            delete_genre.execute(input=input)

        mocked_genre_repository.get_by_id.assert_called_once_with(id=non_existing_id)
        mocked_genre_repository.delete.assert_not_called()
