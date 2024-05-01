from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMember
from src.core.shared.application.list import PaginatedListUseCase


@dataclass
class CastMemberOutput:
    id: UUID
    name: str
    type: str


class ListCastMembers(PaginatedListUseCase[CastMember, CastMemberOutput]):
    default_order_by_field = "name"
    order_by_fields = [
        "name",
        "-name",
    ]

    @staticmethod
    def get_output_data_from_entities(
        entities: list[CastMember],
    ) -> list[CastMemberOutput]:
        return [
            CastMemberOutput(
                id=cast_member.id,
                name=cast_member.name,
                type=cast_member.type,
            )
            for cast_member in entities
        ]
