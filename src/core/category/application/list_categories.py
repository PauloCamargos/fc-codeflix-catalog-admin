from dataclasses import dataclass
from uuid import UUID
from src.core.category.gateway.category_gateway import AbstractCategoryRepository


@dataclass
class CategoryOutput:
    id: UUID
    name: str
    description: str
    is_active: bool


@dataclass
class ListCategoryInput:
    pass


@dataclass
class ListCategoryOutput:
    data: list[CategoryOutput]


class ListCategories:
    def __init__(self, repository: AbstractCategoryRepository):
        self.repository = repository

    def execute(self, input: ListCategoryInput) -> ListCategoryOutput:
        categories = self.repository.list()

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
