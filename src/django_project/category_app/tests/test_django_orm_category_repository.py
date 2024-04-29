import pytest

from src.core.category.domain.category import Category
from src.django_project.category_app.repository import DjangoORMCategoryRepository


@pytest.mark.django_db
class TestSaveDjangoORMCategoryRepository:
    def test_can_save_entity_category(
        self,
        category_repository: DjangoORMCategoryRepository,
        movie_category: Category,
    ):
        category_repository.save(category=movie_category)

        found_category = category_repository.category_model.objects.get(
            id=movie_category.id,
        )
        saved_category = Category(
            id=found_category.id,
            name=found_category.name,
            description=found_category.description,
            is_active=found_category.is_active,
        )

        assert saved_category == movie_category
        assert saved_category.id == movie_category.id
        assert saved_category.name == movie_category.name
        assert saved_category.description == movie_category.description
        assert saved_category.is_active == movie_category.is_active


@pytest.mark.django_db
class TestGetByIdDjangoORMCategoryRepository:
    def test_can_get_by_id_category(
        self,
        movie_category: Category,
        serie_category: Category,
    ):
        categories = [
            movie_category,
            serie_category,
        ]

        repository = DjangoORMCategoryRepository()

        repository.category_model.objects.bulk_create(
            repository.category_model(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active,
            )
            for category in categories
        )

        found_category = repository.get_by_id(id=movie_category.id)

        assert movie_category == found_category


@pytest.mark.django_db
class TestCanListCategoriesRepository:
    def test_can_empty_list_category(self):

        repository = DjangoORMCategoryRepository()

        found_categories = repository.list()

        assert len(found_categories) == 0

    def test_can_list_category(
        self,
        movie_category: Category,
        serie_category: Category,
    ):
        categories = [
            movie_category,
            serie_category,
        ]

        repository = DjangoORMCategoryRepository()

        repository.category_model.objects.bulk_create(
            repository.category_model(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active,
            )
            for category in categories
        )

        found_categories = repository.list()

        assert len(found_categories) == 2
        assert movie_category in found_categories
        assert serie_category in found_categories


@pytest.mark.django_db
class TestDeleteDjangoORMCategoryRepository:
    def test_can_delete_category(
        self,
        movie_category: Category,
        serie_category: Category,
    ):
        categories = [
            movie_category,
            serie_category,
        ]

        repository = DjangoORMCategoryRepository()

        repository.category_model.objects.bulk_create(
            repository.category_model(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active,
            )
            for category in categories
        )

        repository.delete(id=movie_category.id)

        assert not (
            repository.category_model.objects.filter(id=movie_category.id).exists()
        )
        assert repository.category_model.objects.filter(id=serie_category.id).exists()
        assert repository.category_model.objects.count() == 1


@pytest.mark.django_db
class TestUpdateDjangoORMCategoryRepository:
    def test_can_update_entity_category(
        self,
        movie_category: Category,
    ):
        repository = DjangoORMCategoryRepository()

        repository.save(movie_category)

        updated_category_name = "Serie"
        movie_category.update_category(
            name=updated_category_name,
            description=movie_category.description,
        )
        repository.update(category=movie_category)

        assert len(repository.list()) == 1

        updated_category = repository.get_by_id(id=movie_category.id)

        assert updated_category is not None

        assert updated_category.id == movie_category.id
        assert updated_category.name == updated_category_name
        assert updated_category.description == movie_category.description
        assert updated_category.is_active == movie_category.is_active
