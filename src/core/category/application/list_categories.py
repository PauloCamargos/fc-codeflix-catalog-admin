from dataclasses import dataclass
from uuid import UUID

from src.core.category.domain.category import Category
from src.core.shared.application.list import PaginatedListUseCase


@dataclass
class CategoryOutput:
    id: UUID
    name: str
    description: str
    is_active: bool


class ListCategories(PaginatedListUseCase[Category, CategoryOutput]):
    default_order_by_field = "name"
    order_by_fields = [
        "name",
        "-name",
        "description",
        "-description",
    ]

    @staticmethod
    def get_output_data_from_entities(entities: list[Category]) -> list[CategoryOutput]:
        return [
            CategoryOutput(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active,
            )
            for category in entities
        ]
