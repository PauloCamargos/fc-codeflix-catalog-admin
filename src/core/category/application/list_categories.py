from dataclasses import dataclass
from uuid import UUID
from src.core.category.gateway.category_gateway import AbstractCategoryRepository

DEFAULT_CATEGORY_LIST_ORDER = "name"


@dataclass
class CategoryOutput:
    id: UUID
    name: str
    description: str
    is_active: bool


@dataclass
class ListCategoryInput:
    order_by: str | None = None


@dataclass
class ListCategoryOutput:
    data: list[CategoryOutput]


class ListCategories:
    def __init__(self, repository: AbstractCategoryRepository):
        self.repository = repository

    def execute(self, input: ListCategoryInput) -> ListCategoryOutput:
        if input.order_by is None:
            order_by = DEFAULT_CATEGORY_LIST_ORDER
        else:
            order_by = input.order_by

        categories = self.repository.list(order_by=order_by)

        return ListCategoryOutput(
            data=[
                CategoryOutput(
                    id=category.id,
                    name=category.name,
                    description=category.description,
                    is_active=category.is_active,
                )
                for category in categories
            ]
        )
