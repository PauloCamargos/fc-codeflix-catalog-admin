from dataclasses import dataclass
from uuid import UUID
from src.core.cast_member.application.errors import InvalidCastMemberData
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.errors import InvalidCastMemberTypeError

from src.core.cast_member.gateway.cast_member_gateway import (
    AbstractCastMemberRepository,
)


class CreateCastMember:
    @dataclass
    class Input:
        name: str
        type: str

    @dataclass
    class Output:
        id: UUID

    def __init__(self, repository: AbstractCastMemberRepository):
        self.repository = repository

    def execute(self, input: Input) -> Output:
        try:
            cast_member = CastMember(
                name=input.name,
                type=input.type,
            )
        except (ValueError, InvalidCastMemberTypeError) as exc:
            raise InvalidCastMemberData(exc)

        self.repository.save(cast_member=cast_member)

        return CreateCastMember.Output(id=cast_member.id)
