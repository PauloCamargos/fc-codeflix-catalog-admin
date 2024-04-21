from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.gateway.cast_member_gateway import (
    AbstractCastMemberRepository,
)
from src.django_project.cast_member_app.models import CastMember as CastMemberModel
from src.django_project.shared.repository.mapper import BaseORMMapper


class CastMemberMapper(BaseORMMapper[CastMember, CastMemberModel]):
    @staticmethod
    def to_model(entity: CastMember, save: bool = False) -> CastMemberModel:
        instance = CastMemberModel(
            id=entity.id,
            name=entity.name,
            type=entity.type,
        )
        if save:
            instance.save()
        return instance

    @staticmethod
    def to_entity(model: CastMemberModel) -> CastMember:
        return CastMember(
            id=model.id,
            name=model.name,
            type=model.type,
        )


class DjangoORMCastMemberRepository(AbstractCastMemberRepository):

    def __init__(self, cast_member_model: type[CastMemberModel] = CastMemberModel):
        self.cast_member_model = cast_member_model

    def save(self, cast_member: CastMember) -> None:
        CastMemberMapper.to_model(cast_member, save=True)

    def get_by_id(self, id: UUID) -> CastMember | None:
        try:
            found_cast_member = self.cast_member_model.objects.get(id=id)
        except self.cast_member_model.DoesNotExist:
            return None

        return CastMemberMapper.to_entity(found_cast_member)

    def list(self) -> list[CastMember]:
        found_cast_members = self.cast_member_model.objects.all()

        return [
            CastMemberMapper.to_entity(found_cast_member)
            for found_cast_member in found_cast_members
        ]

    def delete(self, id: UUID) -> None:
        self.cast_member_model.objects.filter(id=id).delete()

    def update(self, cast_member: CastMember) -> None:
        self.cast_member_model.objects.filter(id=cast_member.id).update(
            id=cast_member.id,
            name=cast_member.name,
            type=cast_member.type,
        )
