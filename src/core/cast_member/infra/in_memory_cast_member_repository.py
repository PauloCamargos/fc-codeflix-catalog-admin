from copy import deepcopy
from math import ceil
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.gateway.cast_member_gateway import (
    AbstractCastMemberRepository,
)
from src.core.shared import settings
from src.core.shared.application.errors import InvalidPageRequested


class InMemoryCastMemberRepository(AbstractCastMemberRepository):
    def __init__(self, cast_members: list[CastMember] | None = None):
        self.cast_members: list[CastMember] = cast_members or []

    def save(self, cast_member: CastMember) -> None:
        self.cast_members.append(cast_member)

    def get_by_id(self, id: UUID) -> CastMember | None:
        return next(
            (
                deepcopy(cast_member)
                for cast_member in self.cast_members
                if cast_member.id == id
            ),
            None,
        )

    def delete(self, id: UUID) -> None:
        cast_member = self.get_by_id(id)
        if cast_member:
            self.cast_members.remove(cast_member)

    def list(
        self,
        order_by: str | None = None,
        page: int | None = None,
    ) -> list[CastMember]:
        cast_members = [
            deepcopy(cast_member)
            for cast_member in self.cast_members
        ]
        if order_by is not None:
            cast_members = sorted(
                cast_members,
                key=lambda cast_member: getattr(cast_member, order_by.strip("-")),
                reverse=order_by.startswith("-"),
            )

        if page is not None:
            page_size = settings.REPOSITORY["page_size"]
            page_offset = (page - 1) * page_size

            num_elements = max(1, self.count())
            if page > ceil(num_elements / page_size):
                raise InvalidPageRequested(page=page)

            return cast_members[page_offset:page_offset + page_size]

        return list(self.cast_members)

    def count(self) -> int:
        return len(self.cast_members)

    def update(self, cast_member: CastMember) -> None:
        old_cast_member = self.get_by_id(cast_member.id)
        if old_cast_member:
            self.cast_members.remove(old_cast_member)
            self.cast_members.append(cast_member)
