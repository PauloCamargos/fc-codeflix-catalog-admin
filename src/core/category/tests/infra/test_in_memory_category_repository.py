from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestSaveInMemoryCategoryRepository:
    def test_can_save_entity_category(self):
        repository = InMemoryCategoryRepository()

        category = Category(
            name="Dummy",
            description="Dummy description",
            is_active=True,
        )

        repository.save(category=category)

        assert category in repository.categories
        assert len(repository.categories) == 1


class TestGetByIdInMemoryCategoryRepository:
    def test_can_get_by_id_category(self):
        movie_category = Category(
            name="Movie",
            description="Movie description",
            is_active=True,
        )
        serie_category = Category(
            name="Series",
            description="Serie description",
            is_active=True,
        )

        repository = InMemoryCategoryRepository(
            categories=[
                movie_category,
                serie_category,
            ]
        )

        found_category = repository.get_by_id(id=movie_category.id)

        assert movie_category == found_category


class TestDeleteInMemoryCategoryRepository:
    def test_can_delete_category(self):
        movie_category = Category(
            name="Movie",
            description="Movie description",
            is_active=True,
        )
        serie_category = Category(
            name="Series",
            description="Serie description",
            is_active=True,
        )

        repository = InMemoryCategoryRepository(
            categories=[
                movie_category,
                serie_category,
            ]
        )

        repository.delete(id=movie_category.id)

        assert repository.categories == [serie_category]
