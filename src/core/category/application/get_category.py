from dataclasses import dataclass
from uuid import UUID
from core.category.application.errors import CategoryNotFound

from core.category.gateway.category_gateway import AbstractCategoryRepository


@dataclass
class GetCategoryInput:
    id: UUID


@dataclass
class GetCategoryOutput:
    id: UUID
    name: str
    description: str
    is_active: bool


class GetCategory:
    def __init__(self, repository: AbstractCategoryRepository) -> None:
        self.repository: AbstractCategoryRepository = repository

    def execute(self, input: GetCategoryInput) -> GetCategoryOutput | None:
        category = self.repository.get_by_id(id=input.id)

        if category is None:
            raise CategoryNotFound()

        return GetCategoryOutput(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )
