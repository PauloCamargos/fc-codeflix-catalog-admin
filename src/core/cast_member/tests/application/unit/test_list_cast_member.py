from unittest.mock import MagicMock, create_autospec

import pytest

from src.core.cast_member.application.list_cast_member import ListCastMember
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.gateway.cast_member_gateway import (
    AbstractCastMemberRepository,
)


@pytest.fixture
def actor_cast_member() -> CastMember:
    return CastMember(name="John", type="ACTOR")


@pytest.fixture
def mocked_cast_member_repository():
    return create_autospec(AbstractCastMemberRepository)


class TestListCastMember:
    def test_list_cast_member_success(
        self,
        actor_cast_member: CastMember,
        mocked_cast_member_repository: MagicMock,
    ):
        mocked_cast_member_repository.list.return_value = [actor_cast_member]

        input = ListCastMember.Input()

        use_case = ListCastMember(repository=mocked_cast_member_repository)

        output = use_case.execute(input=input)

        mocked_cast_member_repository.list.assert_called_once_with()

        assert len(output) == 1
        [found_cast_member_output] = output
        assert found_cast_member_output.id == actor_cast_member.id
        assert found_cast_member_output.name == actor_cast_member.name
        assert found_cast_member_output.type == actor_cast_member.type
