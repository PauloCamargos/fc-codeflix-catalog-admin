from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from src.core.category.gateway.category_gateway import AbstractCategoryRepository


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

    def execute(self, input: GetCategoryInput) -> Optional[GetCategoryOutput]:
        category = self.repository.get(id=input.id)

        if category is None:
            return None

        return GetCategoryOutput(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )
