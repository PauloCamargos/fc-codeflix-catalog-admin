from typing import Callable
import pytest

from src.core.category.domain.category import Category
from src.django_project.category_app.models import Category as CategoryModel
from src.django_project.category_app.repository import DjangoORMCategoryRepository


@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()


# ----------------------------- #
# CATEGORY MODEL                #
# ----------------------------- #
@pytest.fixture
def movie_category_model() -> CategoryModel:
    return CategoryModel.objects.create(
        name="Movie",
        description="Movie category",
        is_active=True,
    )


@pytest.fixture
def serie_category_model() -> CategoryModel:
    return CategoryModel.objects.create(
        name="Serie",
        description="Serie category",
        is_active=True,
    )


@pytest.fixture
def documentary_category_model() -> CategoryModel:
    return CategoryModel.objects.create(
        name="Documentary",
        description="Documentary category",
        is_active=True,
    )


@pytest.fixture
def music_clip_category_model() -> CategoryModel:
    return CategoryModel.objects.create(
        name="Music clip",
        description="Music clip category",
        is_active=True,
    )


@pytest.fixture
def lecture_category_model() -> CategoryModel:
    return CategoryModel.objects.create(
        name="Lecture",
        description="Lecture category",
        is_active=True,
    )


# -------------------------------------- #
# CATEGORY DOMAIN ENTITY (non-persisted) #
# -------------------------------------- #
MAKE_CATEGORY_FIXTURE = Callable[
    [],
    Callable[
        [str, str, bool],
        Category
    ]
]


@pytest.fixture
def make_category() -> Callable[
    [str, str, bool],
    Category,
]:
    def _make_category(
        name: str,
        description: str,
        is_active: bool,
    ) -> Category:
        return Category(
            name=name,
            description=description,
            is_active=is_active,
        )
    return _make_category


@pytest.fixture
def movie_category() -> Category:
    return Category(
        name="Movie",
        description="Movie category",
        is_active=True,
    )


@pytest.fixture
def serie_category(make_category) -> Category:
    return make_category(
        name="Serie",
        description="Serie category",
        is_active=True,
    )


@pytest.fixture
def documentary_category(make_category) -> Category:
    return make_category(
        name="Documentary",
        description="Documentary category",
        is_active=True,
    )


@pytest.fixture
def music_clip_category(make_category) -> Category:
    return make_category(
        name="Music clip",
        description="Music clip category",
        is_active=True,
    )


@pytest.fixture
def lecture_category(make_category) -> Category:
    return make_category(
        name="Lecture",
        description="Lecture category",
        is_active=True,
    )
