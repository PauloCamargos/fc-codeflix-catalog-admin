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
    return Genre(name="Action")


@pytest.fixture
def genre_repository() -> DjangoORMGenreRepository:
    return DjangoORMGenreRepository()


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
