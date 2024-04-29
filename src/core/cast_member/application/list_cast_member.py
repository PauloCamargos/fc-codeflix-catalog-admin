from dataclasses import dataclass, field
from uuid import UUID

from src.core.cast_member.gateway.cast_member_gateway import (
    AbstractCastMemberRepository,
)
from src.core.shared import settings as core_settings
from src.core.shared.application.input import ListInputMixin

DEFAULT_CAST_MEMBER_LIST_ORDER = "name"

VALID_ORDER_BY_ATTRIBUTES = [
    "name",
    "-name",
]


class ListCastMembers:
    @dataclass
    class Input(ListInputMixin):
        order_by: str = field(default=DEFAULT_CAST_MEMBER_LIST_ORDER)
        page: int = field(default=1)

        @staticmethod
        def get_valid_order_by_attributes() -> list[str]:
            return VALID_ORDER_BY_ATTRIBUTES

    @dataclass
    class Output:
        data: list["ListCastMembers.CastMemberOutput"]
        meta: "ListCastMembers.OutputMeta"

    @dataclass
    class CastMemberOutput:
        id: UUID
        name: str
        type: str

    @dataclass
    class OutputMeta:
        page: int
        per_page: int
        total: int

    def __init__(self, repository: AbstractCastMemberRepository):
        self.repository = repository

    def execute(self, input: Input) -> Output:
        cast_members = self.repository.list(
            order_by=input.order_by,
            page=input.page,
        )
        total = self.repository.count()

        data = [
            ListCastMembers.CastMemberOutput(
                id=cast_member.id,
                name=cast_member.name,
                type=cast_member.type,
            )
            for cast_member in cast_members
        ]

        meta = ListCastMembers.OutputMeta(
            page=input.page,
            per_page=core_settings.REPOSITORY["page_size"],
            total=total,
        )

        return ListCastMembers.Output(
            data=data,
            meta=meta,
        )
