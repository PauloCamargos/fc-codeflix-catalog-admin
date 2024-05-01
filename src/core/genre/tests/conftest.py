import pytest

from src.core.category.domain.category import Category
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
        categories=[movie_category.id, documentary_category.id],
    )


@pytest.fixture
def drama_genre(
    movie_category: Category,
) -> Genre:
    return Genre(
        name="Drama",
        categories=[movie_category.id],
    )


@pytest.fixture
def genre_repository() -> InMemoryGenreRepository:
    return InMemoryGenreRepository()
