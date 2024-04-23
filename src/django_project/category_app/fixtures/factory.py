import pytest

from src.django_project.category_app.models import Category


@pytest.fixture
def make_category() -> Category:
    def _make_category(
        name: str,
        description: str,
        is_active: bool,
    ) -> Category:
        return Category.objects.create(
            name=name,
            description=description,
            is_active=is_active,
        )
    return _make_category

@pytest.fixture
def movie_category(
    make_category,
) -> Category:
    return make_category(
        name="Movie",
        description="Movie category",
        is_active=True,
    )


@pytest.fixture
def serie_category(
    make_category
) -> Category:
    return make_category(
        name="Serie",
        description="Serie category",
        is_active=True,
    )
