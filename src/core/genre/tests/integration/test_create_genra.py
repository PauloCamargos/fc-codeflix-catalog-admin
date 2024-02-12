from uuid import UUID

import pytest

from core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from core.genre.application.create_genre import CreateGenre
from core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository
from django_project.category_app.models import Category


@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")


@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")


@pytest.fixture
def category_repository(
    movie_category: Category,
    documentary_category: Category,
) -> InMemoryCategoryRepository:
    return InMemoryCategoryRepository(
        categories=[movie_category, documentary_category]
    )


class TestCreateGenreIntegration:

    def test_create_category_with_valid_data_success(
        self,
        movie_category: Category,
        documentary_category: Category,
        category_repository: InMemoryCategoryRepository,
    ) -> None:
        repository = InMemoryGenreRepository()
        create_genre = CreateGenre(
            repository=repository,
            category_repository=category_repository,
        )

        create_genre_input = CreateGenre.Input(
            name="Sci-fi",
            categories={movie_category.id, documentary_category.id},
        )

        created_genre_output = create_genre.execute(create_genre_input)

        assert isinstance(created_genre_output.id, UUID)
        saved_genre = repository.get_by_id(created_genre_output.id)
        assert saved_genre is not None
        assert saved_genre.name == create_genre_input.name
        assert saved_genre.is_active == create_genre_input.is_active
        assert saved_genre.categories == {movie_category.id, documentary_category.id}
