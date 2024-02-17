from unittest.mock import MagicMock, create_autospec
from uuid import uuid4

import pytest
from src.core.cast_member.application.delete_cast_member import DeleteCastMember
from src.core.cast_member.application.errors import CastMemberNotFound

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


class TestDeleteCastMember:
    def test_delete_cast_member_success(
        self,
        actor_cast_member: CastMember,
        mocked_cast_member_repository: MagicMock,
    ):
        mocked_cast_member_repository.get_by_id.return_value = actor_cast_member

        input = DeleteCastMember.Input(id=actor_cast_member.id)

        use_case = DeleteCastMember(repository=mocked_cast_member_repository)

        use_case.execute(input=input)

        mocked_cast_member_repository.get_by_id.assert_called_once_with(
            id=actor_cast_member.id,
        )

        mocked_cast_member_repository.delete.assert_called_once_with(
            id=actor_cast_member.id,
        )

    def test_delete_cast_member_does_not_exist_error(
        self,
        mocked_cast_member_repository: MagicMock,
    ):
        does_not_exist_cast_member_id = uuid4()
        mocked_cast_member_repository.get_by_id.return_value = None

        input = DeleteCastMember.Input(id=does_not_exist_cast_member_id)

        use_case = DeleteCastMember(repository=mocked_cast_member_repository)

        with pytest.raises(CastMemberNotFound):
            use_case.execute(input=input)

        mocked_cast_member_repository.get_by_id.assert_called_once_with(
            id=does_not_exist_cast_member_id,
        )

        mocked_cast_member_repository.delete.assert_not_called()
