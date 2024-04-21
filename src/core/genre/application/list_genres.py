from dataclasses import dataclass
from uuid import UUID
from src.core.genre.gateway.genre_gateway import AbstractGenreRepository

DEFAULT_GENRE_LIST_ORDER = "name"


@dataclass
class GenreOutput:
    id: UUID
    name: str
    categories: list[UUID]
    is_active: bool


class ListGenres:

    @dataclass
    class Input:
        order_by: str | None = None

    @dataclass
    class Output:
        data: list[GenreOutput]

    def __init__(self, repository: AbstractGenreRepository):
        self.repository = repository

    def execute(self, input: Input) -> Output:
        if input.order_by is None:
            order_by = DEFAULT_GENRE_LIST_ORDER
        else:
            order_by = input.order_by

        genres = self.repository.list(order_by=order_by)

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
