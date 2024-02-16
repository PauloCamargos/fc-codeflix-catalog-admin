from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.gateway.cast_member_gateway import (
    AbstractCastMemberRepository,
)
from src.django_project.cast_member.models import CastMember as CastMemberModel


class DjangoORMCastMemberRepository(AbstractCastMemberRepository):

    def __init__(self, cast_member_model: CastMemberModel = CastMemberModel):
        self.cast_member_model = cast_member_model

    def save(self, cast_member: CastMember) -> UUID:
        created_cast_member = self.cast_member_model.objects.create(
            id=cast_member.id,
            name=cast_member.name,
            type=cast_member.type,
        )

        return created_cast_member.id

    def get_by_id(self, id: UUID) -> CastMember | None:
        try:
            found_cast_member = self.cast_member_model.objects.get(id=id)
        except self.cast_member_model.DoesNotExist:
            return None

        return CastMember(
            id=found_cast_member.id,
            name=found_cast_member.name,
            type=found_cast_member.type,
        )

    def list(self) -> list[CastMember]:
        found_cast_members = self.cast_member_model.objects.all()

        return [
            CastMember(
                id=found_cast_member.id,
                name=found_cast_member.name,
                type=found_cast_member.type,
            )
            for found_cast_member in found_cast_members
        ]

    def update(self, cast_member: CastMember) -> None:
        self.cast_member_model.objects.filter(id=cast_member.id).update(
            id=cast_member.id,
            name=cast_member.name,
            type=cast_member.type,
        )

    def delete(self, id: UUID) -> None:
        self.cast_member_model.objects.filter(id=id).delete()
