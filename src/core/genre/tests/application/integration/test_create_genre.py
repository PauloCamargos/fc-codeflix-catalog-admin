from uuid import UUID, uuid4

import pytest

from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)
from src.core.genre.application.create_genre import CreateGenre
from src.core.genre.application.errors import RelatedCategoriesNotFound
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


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

    def test_create_genre_with_valid_data_success(
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
            categories=[movie_category.id, documentary_category.id],
        )

        created_genre_output = create_genre.execute(create_genre_input)

        assert isinstance(created_genre_output.id, UUID)
        saved_genre = repository.get_by_id(created_genre_output.id)
        assert saved_genre is not None
        assert saved_genre.name == create_genre_input.name
        assert saved_genre.is_active == create_genre_input.is_active
        assert saved_genre.categories == {movie_category.id, documentary_category.id}

    def test_create_genre_with_non_existent_categories(
        self,
        category_repository: InMemoryCategoryRepository,
    ):
        repository = InMemoryGenreRepository()
        create_genre = CreateGenre(
            repository=repository,
            category_repository=category_repository,
        )

        non_existent_category_ids = [uuid4(), uuid4()]
        create_genre_input = CreateGenre.Input(
            name="Romance",
            categories=non_existent_category_ids,
        )

        with pytest.raises(
            RelatedCategoriesNotFound, match="Categories not found: "
        ) as exc:
            create_genre.execute(create_genre_input)

        for category_id in non_existent_category_ids:
            assert str(category_id) in str(exc.value)

    def test_create_genre_without_categories(
        self,
        category_repository: InMemoryCategoryRepository,
    ):
        repository = InMemoryGenreRepository()
        create_genre = CreateGenre(
            repository=repository,
            category_repository=category_repository,
        )

        created_genre_input = CreateGenre.Input(name="Romance")

        created_genre_output = create_genre.execute(created_genre_input)

        assert isinstance(created_genre_output.id, UUID)
        saved_genre = repository.get_by_id(created_genre_output.id)
        assert saved_genre is not None
        assert saved_genre.name == created_genre_input.name
        assert saved_genre.is_active == created_genre_input.is_active
        assert saved_genre.categories == list()
