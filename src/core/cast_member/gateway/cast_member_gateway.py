from abc import ABC, abstractmethod
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMember


class AbstractCastMemberRepository(ABC):
    @abstractmethod
    def save(self, cast_member: CastMember) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_by_id(self, id: UUID) -> CastMember | None:
        raise NotImplementedError()

    @abstractmethod
    def list(
        self,
        order_by: str | None = None,
        page: int | None = None,
    ) -> list[CastMember]:
        raise NotImplementedError()

    @abstractmethod
    def count(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def update(self, cast_member: CastMember) -> None:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, id: UUID) -> None:
        raise NotImplementedError()
