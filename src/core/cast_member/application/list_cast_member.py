from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.gateway.cast_member_gateway import (
    AbstractCastMemberRepository,
)

DEFAULT_CAST_MEMBER_LIST_ORDER = "name"


@dataclass
class CastMemberOutput:
    id: UUID
    name: str
    type: str


class ListCastMember:
    @dataclass
    class Input:
        order_by: str | None = None

    @dataclass
    class Output:
        data: list[CastMemberOutput]

    def __init__(self, repository: AbstractCastMemberRepository):
        self.repository = repository

    def execute(self, input: Input) -> Output:
        if input.order_by is None:
            order_by = DEFAULT_CAST_MEMBER_LIST_ORDER
        else:
            order_by = input.order_by

        cast_members = self.repository.list(order_by=order_by)

        return ListCastMember.Output(
            data=[
                CastMemberOutput(
                    id=cast_member.id,
                    name=cast_member.name,
                    type=cast_member.type,
                )
                for cast_member in cast_members
            ]
        )
