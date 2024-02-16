import pytest

from src.core.cast_member.application.list_cast_member import ListCastMember
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


class TestListCastMember:
    def test_list_cast_member_success(
        self,
        actor_cast_member: CastMember,
        cast_member_repository: AbstractCastMemberRepository,
    ):

        input = ListCastMember.Input()

        use_case = ListCastMember(repository=cast_member_repository)

        output = use_case.execute(input=input)

        assert len(output) == 1
        [found_cast_member_output] = output
        assert found_cast_member_output.id == actor_cast_member.id
        assert found_cast_member_output.name == actor_cast_member.name
        assert found_cast_member_output.type == actor_cast_member.type
