import pytest

from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)
from src.core.genre.application.list_genres import ListGenres
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
def genre_repository(
    romance_genre: Genre,
) -> InMemoryGenreRepository:
    return InMemoryGenreRepository(genres=[romance_genre])


class TestListGenre:
    def test_list_genre_with_categories(
        self,
        romance_genre: Genre,
        genre_repository: InMemoryGenreRepository,
        movie_category: Category,
        documentary_category: Category,
    ) -> None:
        category_repository = InMemoryCategoryRepository(
            categories=[movie_category, documentary_category],
        )
        list_genre = ListGenres(repository=genre_repository)

        input = ListGenres.Input()

        output = list_genre.execute(input=input)

        assert len(output.data) == 1

        [genre_data] = output.data

        assert romance_genre.id == genre_data.id
        assert romance_genre.name == genre_data.name
        assert romance_genre.is_active == genre_data.is_active
        assert romance_genre.categories == {
            category.id
            for category in category_repository.list_categories()
        }
