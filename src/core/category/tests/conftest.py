import pytest

from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


@pytest.fixture
def movie_category() -> Category:
    return Category(
        name="Movie",
        description="Movie category",
        is_active=True,
    )


@pytest.fixture
def serie_category() -> Category:
    return Category(
        name="Serie",
        description="Serie category",
        is_active=True,
    )


@pytest.fixture
def documentary_category() -> Category:
    return Category(
        name="Documentary",
        description="Documentary category",
        is_active=True,
    )


@pytest.fixture
def music_clip_category() -> Category:
    return Category(
        name="Music clip",
        description="Music clip category",
        is_active=True,
    )


@pytest.fixture
def lecture_category() -> Category:
    return Category(
        name="Lecture",
        description="Lecture category",
        is_active=True,
    )


@pytest.fixture
def category_repository() -> InMemoryCategoryRepository:
    return InMemoryCategoryRepository()
