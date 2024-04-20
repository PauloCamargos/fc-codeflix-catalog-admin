from uuid import uuid4

import pytest

from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository


@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")


@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Category")


@pytest.fixture
def romance_genre() -> Genre:
    return Genre(name="Romance")


@pytest.fixture
def genre_repository() -> DjangoORMGenreRepository:
    return DjangoORMGenreRepository()


@pytest.fixture
def genre_repository_with_romance_genre(
    romance_genre: Genre,
    movie_category: Category,
    documentary_category: Category,
    category_repository: DjangoORMCategoryRepository,
    genre_repository: DjangoORMGenreRepository,
) -> DjangoORMGenreRepository:
    romance_genre.add_category(movie_category.id)
    romance_genre.add_category(documentary_category.id)

    category_repository.save(category=movie_category)
    category_repository.save(category=documentary_category)

    genre_repository.save(genre=romance_genre)
    return genre_repository


@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()


@pytest.mark.django_db
class TestSave:
    def test_saves_genre_in_database_no_associated_categories_success(
        self,
        romance_genre: Genre,
        genre_repository: DjangoORMGenreRepository,
    ):
        genre_repository.save(genre=romance_genre)

        created_genre = (
            genre_repository.genre_model.objects
            .filter(id=romance_genre.id)
            .first()
        )

        assert created_genre is not None
        assert created_genre.name == romance_genre.name
        assert created_genre.is_active == romance_genre.is_active
        assert set(created_genre.categories.values_list("id", flat=True)) == set()

    def test_saves_genre_in_database_with_associated_categories_success(
        self,
        romance_genre: Genre,
        movie_category: Category,
        documentary_category: Category,
        genre_repository: DjangoORMGenreRepository,
        category_repository: DjangoORMCategoryRepository,
    ):
        romance_genre.add_category(movie_category.id)
        romance_genre.add_category(documentary_category.id)

        category_repository.save(category=movie_category)
        category_repository.save(category=documentary_category)

        genre_repository.save(genre=romance_genre)

        created_genre = (
            genre_repository.genre_model.objects
            .filter(id=romance_genre.id)
            .prefetch_related("categories")
            .first()
        )

        assert created_genre is not None
        assert created_genre.name == romance_genre.name
        assert created_genre.is_active == romance_genre.is_active

        assert (
            set(
                category.id
                for category in created_genre.categories.all()
            ) == romance_genre.categories
        )


@pytest.mark.django_db
class TestList:
    def test_list_genre_success(
        self,
        romance_genre: Genre,
        genre_repository_with_romance_genre: DjangoORMGenreRepository,
    ):
        genres = genre_repository_with_romance_genre.list()

        assert genres == [romance_genre]

    def test_emtpy_list_genre_sucess(
        self,
        genre_repository: DjangoORMGenreRepository,
    ):
        genres = genre_repository.list()
        assert genres == []


@pytest.mark.django_db
class TestGetById:
    def test_get_by_id_returns_none_success(
        self,
        genre_repository: DjangoORMGenreRepository,
    ):
        genre = genre_repository.get_by_id(id=uuid4())
        assert genre is None

    def test_get_by_id_success(
        self,
        romance_genre: Genre,
        genre_repository_with_romance_genre: DjangoORMGenreRepository,
    ):
        genre_found = genre_repository_with_romance_genre.get_by_id(id=romance_genre.id)

        assert genre_found is not None
        assert genre_found.name == romance_genre.name
        assert genre_found.is_active == romance_genre.is_active

        assert genre_found.categories == romance_genre.categories


@pytest.mark.django_db
class TestUpdate:
    def test_update_success(
        self,
        movie_category: Category,
        romance_genre: Genre,
        genre_repository_with_romance_genre: DjangoORMGenreRepository,
    ):
        new_name = "Love"
        romance_genre.update_name(name=new_name)

        if romance_genre.is_active:
            romance_genre.deactivate()
            new_is_active = False
        else:
            romance_genre.activate()
            new_is_active = True

        romance_genre.remove_category(id=movie_category.id)
        new_categories = romance_genre.categories

        genre_repository_with_romance_genre.update(genre=romance_genre)

        genre_found = genre_repository_with_romance_genre.get_by_id(id=romance_genre.id)

        assert genre_found is not None
        assert genre_found.name == new_name
        assert genre_found.is_active == new_is_active

        assert genre_found.categories == new_categories


@pytest.mark.django_db
class TestDelete:
    def test_delete_genre_success(
        self,
        romance_genre: Genre,
        genre_repository_with_romance_genre: DjangoORMGenreRepository,
    ):
        genre_repository_with_romance_genre.delete(id=romance_genre.id)

        genre_found = genre_repository_with_romance_genre.get_by_id(id=romance_genre.id)

        assert genre_found is None
