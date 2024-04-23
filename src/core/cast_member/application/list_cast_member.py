from dataclasses import dataclass, field
from uuid import UUID

from src.core.cast_member.gateway.cast_member_gateway import (
    AbstractCastMemberRepository,
)
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

        @staticmethod
        def get_valid_order_by_attributes() -> list[str]:
            return VALID_ORDER_BY_ATTRIBUTES

    @dataclass
    class Output:
        data: list["ListCastMembers.CastMemberOutput"]

    @dataclass
    class CastMemberOutput:
        id: UUID
        name: str
        type: str

    def __init__(self, repository: AbstractCastMemberRepository):
        self.repository = repository

    def execute(self, input: Input) -> Output:
        cast_members = self.repository.list(order_by=input.order_by)

        return ListCastMembers.Output(
            data=[
                ListCastMembers.CastMemberOutput(
                    id=cast_member.id,
                    name=cast_member.name,
                    type=cast_member.type,
                )
                for cast_member in cast_members
            ]
        )
