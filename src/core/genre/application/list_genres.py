from dataclasses import dataclass
from uuid import UUID

from src.core.genre.domain.genre import Genre
from src.core.shared.application.list import PaginatedListUseCase


@dataclass
class GenreOutput:
    id: UUID
    name: str
    categories: list[UUID]
    is_active: bool


class ListGenres(PaginatedListUseCase[Genre, GenreOutput]):
    default_order_by_field = "name"
    order_by_fields = [
        "name",
        "-name",
    ]

    @staticmethod
    def get_output_data_from_entities(entities: list[Genre]) -> list[GenreOutput]:
        return [
            GenreOutput(
                id=genre.id,
                name=genre.name,
                is_active=genre.is_active,
                categories=genre.categories,
            )
            for genre in entities
        ]
