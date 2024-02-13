from dataclasses import dataclass
from uuid import UUID
from src.core.genre.gateway.genre_gateway import AbstractGenreRepository


@dataclass
class GenreOutput:
    id: UUID
    name: str
    categories: set[UUID]
    is_active: bool


class ListGenres:

    @dataclass
    class Input:
        pass

    @dataclass
    class Output:
        data: list[GenreOutput]

    def __init__(self, repository: AbstractGenreRepository):
        self.repository = repository

    def execute(self, input: Input) -> Output:
        genres = self.repository.list_genres()

        return ListGenres.Output(
            data=[
                GenreOutput(
                    id=genre.id,
                    name=genre.name,
                    is_active=genre.is_active,
                    categories=genre.categories,
                )
                for genre in genres
            ]
        )
