from dataclasses import dataclass
from uuid import UUID
from core.genre.gateway.genre_gateway import AbstractGenreRepository


@dataclass
class GenreOutput:
    id: UUID
    name: str
    description: str
    is_active: bool


@dataclass
class ListGenreInput:
    pass


@dataclass
class ListGenreOutput:
    data: list[GenreOutput]


class ListCategories:
    def __init__(self, repository: AbstractGenreRepository):
        self.repository = repository

    def execute(self, input: ListGenreInput) -> ListGenreOutput:
        categories = self.repository.list_categories()

        return ListGenreOutput(
            data=[
                GenreOutput(
                    id=genre.id,
                    name=genre.name,
                    description=genre.description,
                    is_active=genre.is_active,
                )
                for genre in categories
            ]
        )
