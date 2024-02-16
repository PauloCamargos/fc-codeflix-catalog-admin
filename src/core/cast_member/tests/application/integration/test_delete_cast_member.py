from uuid import uuid4

import pytest

from src.core.cast_member.application.delete_cast_member import DeleteCastMember
from src.core.cast_member.application.errors import CastMemberNotFound
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.gateway.cast_member_gateway import (
    AbstractCastMemberRepository,
)
from src.core.cast_member.infra.in_memory_cast_member_repository import (
    InMemoryCastMemberRepository,
)


@pytest.fixture
def actor_cast_member() -> CastMember:
    return CastMember(name="John", type="ACTOR")


@pytest.fixture
def cast_member_repository(
    actor_cast_member: CastMember,
) -> AbstractCastMemberRepository:
    return InMemoryCastMemberRepository(cast_members=[actor_cast_member])


class TestDeleteCastMember:
    def test_delete_cast_member_success(
        self,
        actor_cast_member: CastMember,
        cast_member_repository: AbstractCastMemberRepository,
    ):
        input = DeleteCastMember.Input(id=actor_cast_member.id)

        use_case = DeleteCastMember(repository=cast_member_repository)

        use_case.execute(input=input)

        deleted_cast_member = cast_member_repository.get_by_id(
            id=actor_cast_member.id,
        )
        assert deleted_cast_member is None

    def test_delete_cast_member_does_not_exist_error(
        self,
        cast_member_repository: AbstractCastMemberRepository,
    ):
        does_not_exist_cast_member_id = uuid4()

        input = DeleteCastMember.Input(id=does_not_exist_cast_member_id)

        use_case = DeleteCastMember(repository=cast_member_repository)

        with pytest.raises(CastMemberNotFound):
            use_case.execute(input=input)
