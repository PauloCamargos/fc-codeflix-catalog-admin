from uuid import UUID

from django.core.paginator import Paginator
from django.db.models.query import QuerySet

from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.gateway.cast_member_gateway import (
    AbstractCastMemberRepository,
)
from src.core.shared import settings as core_settings
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
        self._count: int | None = None

    def get_queryset(self) -> QuerySet:
        return self.cast_member_model.objects.all()

    def save(self, cast_member: CastMember) -> None:
        CastMemberMapper.to_model(cast_member, save=True)

    def get_by_id(self, id: UUID) -> CastMember | None:
        try:
            cast_member = self.cast_member_model.objects.get(id=id)
        except self.cast_member_model.DoesNotExist:
            return None

        return CastMemberMapper.to_entity(cast_member)

    def list(
        self,
        order_by: str | None = None,
        page: int | None = None,
    ) -> list[CastMember]:
        queryset = self.get_queryset()

        if order_by is not None:
            queryset = queryset.order_by(order_by)

        if page is not None:
            paginator = Paginator(queryset, core_settings.REPOSITORY["page_size"])
            paginator_page = paginator.page(page)
            cast_members = paginator_page.object_list
            self._count = paginator.count
        else:
            cast_members = list(queryset)

        return [
            CastMemberMapper.to_entity(cast_member)
            for cast_member in cast_members
        ]

    def count(
        self,
    ) -> int:
        if self._count is None:
            self._count = self.get_queryset().count()
        return self._count

    def delete(self, id: UUID) -> None:
        self.cast_member_model.objects.filter(id=id).delete()

    def update(self, cast_member: CastMember) -> None:
        self.cast_member_model.objects.filter(id=cast_member.id).update(
            id=cast_member.id,
            name=cast_member.name,
            type=cast_member.type,
        )
