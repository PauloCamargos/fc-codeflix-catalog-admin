from dataclasses import dataclass
from uuid import UUID
from src.core.cast_member.application.errors import CastMemberNotFound

from src.core.cast_member.gateway.cast_member_gateway import (
    AbstractCastMemberRepository,
)


class DeleteCastMember:
    @dataclass
    class Input:
        id: UUID

    def __init__(self, repository: AbstractCastMemberRepository):
        self.repository = repository

    def execute(self, input: Input) -> None:
        cast_member = self.repository.get_by_id(id=input.id)

        if cast_member is None:
            raise CastMemberNotFound()

        self.repository.delete(id=cast_member.id)
