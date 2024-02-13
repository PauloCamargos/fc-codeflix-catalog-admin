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
def genre_repository(
    romance_genre: Genre,
    horror_genre: Genre,
) -> InMemoryGenreRepository:
    return InMemoryGenreRepository(genres=[romance_genre, horror_genre])


class TestDeleteGenre:
    def test_delete_genre_by_id_success(
        self,
        romance_genre: Genre,
        horror_genre: Genre,
        genre_repository: InMemoryGenreRepository,
    ):

        input = DeleteGenre.Input(id=romance_genre.id)
        delete_genre = DeleteGenre(repository=genre_repository)

        delete_genre.execute(input=input)

        assert len(genre_repository.list_genres()) == 1
        assert horror_genre in genre_repository.list_genres()

    def test_delete_genre_does_not_exist_error(
        self,
        romance_genre: Genre,
        horror_genre: Genre,
        genre_repository: InMemoryGenreRepository,
    ):

        input = DeleteGenre.Input(id=uuid4())
        delete_genre = DeleteGenre(repository=genre_repository)

        with pytest.raises(GenreNotFound):
            delete_genre.execute(input=input)

        exising_genres = genre_repository.list_genres()
        assert len(exising_genres) == 2
        assert romance_genre in exising_genres
        assert horror_genre in exising_genres
