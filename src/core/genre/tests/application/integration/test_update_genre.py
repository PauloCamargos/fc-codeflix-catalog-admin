import pytest

from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
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
def genre_repository(sci_fi_genre: Genre) -> InMemoryGenreRepository:
    return InMemoryGenreRepository(genres=[sci_fi_genre])


@pytest.fixture
def category_repository(
    movie_category: Category,
    documentary_category: Category,
) -> InMemoryCategoryRepository:
    return InMemoryCategoryRepository(categories=[movie_category, documentary_category])


class TestUpdateGenre:
    def test_update_genre_with_valid_data_success(
        self,
        sci_fi_genre: Genre,
        movie_category: Category,
        genre_repository: InMemoryGenreRepository,
        category_repository: InMemoryCategoryRepository,
    ):
        input = UpdateGenre.Input(
            id=sci_fi_genre.id,
            name="Science Fiction",
            categories=[movie_category.id],
            is_active=not sci_fi_genre.is_active,
        )

        update_genre = UpdateGenre(
            repository=genre_repository,
            category_repository=category_repository,
        )

        update_genre.execute(input=input)

        updated_genre = genre_repository.get_by_id(id=sci_fi_genre.id)

        assert updated_genre is not None

        assert updated_genre.name == input.name
        assert updated_genre.is_active == input.is_active
        assert updated_genre.categories == input.categories
