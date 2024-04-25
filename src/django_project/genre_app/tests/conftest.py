import pytest

from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.models import Genre as GenreModel
from src.django_project.genre_app.repository import DjangoORMGenreRepository


@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()


@pytest.fixture
def genre_repository() -> DjangoORMGenreRepository:
    return DjangoORMGenreRepository()


# ----------------- #
# CAST MEMBER MODEL #
# ----------------- #
@pytest.fixture
def romance_genre_model_with_categories(
    movie_category: Category,
    documentary_category: Category,
    category_repository: DjangoORMCategoryRepository,
    genre_repository: DjangoORMGenreRepository,
) -> GenreModel:
    category_repository.save(category=movie_category)
    category_repository.save(category=documentary_category)

    romance_genre = Genre(
        name="Romance",
        categories=[
            documentary_category.id,
            movie_category.id,
        ],
    )

    genre_repository.save(genre=romance_genre)

    return (
        GenreModel.objects
        .prefetch_related(
            genre_repository._get_categories_prefetch()
        ).get(id=romance_genre.id)
    )


@pytest.fixture
def drama_genre_model_without_categories(
    genre_repository: DjangoORMGenreRepository,
) -> GenreModel:
    drama_genre = Genre(name="Drama")
    genre_repository.save(genre=drama_genre)
    return (
        GenreModel.objects
        .prefetch_related(
            genre_repository._get_categories_prefetch()
        ).get(id=drama_genre.id)
    )


# ----------------------------------------- #
# CAST MEMBER DOMAIN ENTITY (non-persisted) #
# ----------------------------------------- #
@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")


@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Category")
