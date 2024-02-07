from uuid import UUID
from src.core.category.application.errors import InvalidCategoryData

from src.core.category.domain.category import Category


def create_category_use_case(
    name: str,
    description: str = "",
    is_active: bool = True,
) -> UUID:
    try:
        category = Category(
            name=name,
            description=description,
            is_active=is_active,
        )
    except ValueError as err:
        raise InvalidCategoryData(err)

    return category.id
