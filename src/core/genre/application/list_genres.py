from dataclasses import dataclass, field
from uuid import UUID

from src.core.genre.gateway.genre_gateway import AbstractGenreRepository
from src.core.shared import settings as core_settings
from src.core.shared.application.input import ListInputMixin

DEFAULT_GENRE_LIST_ORDER = "name"

VALID_ORDER_BY_ATTRIBUTES = [
    "name",
    "-name",
]


class ListGenres:
    @dataclass
    class Input(ListInputMixin):
        order_by: str = field(default=DEFAULT_GENRE_LIST_ORDER)
        page: int = field(default=1)

        @staticmethod
        def get_valid_order_by_attributes() -> list[str]:
            return VALID_ORDER_BY_ATTRIBUTES

    @dataclass
    class Output:
        data: list["ListGenres.GenreOutput"]
        meta: list["ListGenres.OutputMeta"]

    @dataclass
    class OutputMeta:
        page: int
        per_page: int
        total: int

    @dataclass
    class GenreOutput:
        id: UUID
        name: str
        categories: list[UUID]
        is_active: bool

    def __init__(self, repository: AbstractGenreRepository):
        self.repository = repository

    def execute(self, input: Input) -> Output:
        genres = self.repository.list(
            order_by=input.order_by,
            page=input.page,
        )
        total = self.repository.count()

        data = [
            ListGenres.GenreOutput(
                id=genre.id,
                name=genre.name,
                is_active=genre.is_active,
                categories=genre.categories,
            )
            for genre in genres
        ]

        meta = ListGenres.OutputMeta(
            page=input.page,
            per_page=core_settings.REPOSITORY["page_size"],
            total=total,
        )

        return ListGenres.Output(
            data=data,
            meta=meta,
        )
