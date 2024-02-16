from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.application.errors import (
    CastMemberNotFound,
    InvalidCastMemberData,
)
from src.core.cast_member.domain.errors import InvalidCastMemberTypeError
from src.core.cast_member.gateway.cast_member_gateway import (
    AbstractCastMemberRepository,
)


class UpdateCastMember:
    @dataclass
    class Input:
        id: UUID
        name: str | None = None
        type: str | None = None

    @dataclass
    class Output:
        id: UUID
        name: str
        type: str

    def __init__(self, repository: AbstractCastMemberRepository):
        self.repository = repository

    def execute(self, input: Input) -> None:
        cast_member = self.repository.get_by_id(id=input.id)

        if cast_member is None:
            raise CastMemberNotFound()

        try:
            if input.name is not None:
                cast_member.update_name(name=input.name)
        except ValueError as exc:
            raise InvalidCastMemberData(exc)

        try:
            if input.type is not None:
                cast_member.update_type(type=input.type)
        except InvalidCastMemberTypeError as exc:
            raise InvalidCastMemberData(exc)

        self.repository.update(cast_member=cast_member)

        return UpdateCastMember.Output(
            id=cast_member.id,
            name=cast_member.name,
            type=cast_member.type,
        )
