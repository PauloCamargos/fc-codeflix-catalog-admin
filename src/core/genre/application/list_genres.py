from dataclasses import dataclass, field
from uuid import UUID

from src.core.genre.gateway.genre_gateway import AbstractGenreRepository
from src.core.shared.application.input import ValidateInputMixin

DEFAULT_GENRE_LIST_ORDER = "name"

VALID_ORDER_BY_ATTRIBUTES = [
    "name",
    "-name",
]


class ListGenres:

    @dataclass
    class Input(ValidateInputMixin):
        order_by: str = field(default=DEFAULT_GENRE_LIST_ORDER)

        @staticmethod
        def get_valid_order_by_attributes() -> list[str]:
            return VALID_ORDER_BY_ATTRIBUTES

    @dataclass
    class Output:
        data: list["ListGenres.GenreOutput"]

    @dataclass
    class GenreOutput:
        id: UUID
        name: str
        categories: list[UUID]
        is_active: bool

    def __init__(self, repository: AbstractGenreRepository):
        self.repository = repository

    def execute(self, input: Input) -> Output:
        genres = self.repository.list(order_by=input.order_by)

        return ListGenres.Output(
            data=[
                ListGenres.GenreOutput(
                    id=genre.id,
                    name=genre.name,
                    is_active=genre.is_active,
                    categories=genre.categories,
                )
                for genre in genres
            ]
        )
