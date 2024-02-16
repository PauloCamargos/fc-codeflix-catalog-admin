from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.gateway.cast_member_gateway import (
    AbstractCastMemberRepository,
)


@dataclass
class CastMemberOutput:
    id: UUID
    name: str
    type: str


class ListCastMember:
    @dataclass
    class Input:
        pass

    @dataclass
    class Output:
        data: list[CastMemberOutput]

    def __init__(self, repository: AbstractCastMemberRepository):
        self.repository = repository

    def execute(self, input: Input) -> list[Output]:
        cast_members = self.repository.list()

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
