
from dataclasses import asdict
from unittest.mock import MagicMock, create_autospec
from uuid import uuid4

import pytest

from src.core.cast_member.application.errors import (
    CastMemberNotFound,
    InvalidCastMemberData,
)
from src.core.cast_member.application.update_cast_member import UpdateCastMember
from src.core.cast_member.domain.cast_member import (
    MAX_CAST_MEMBER_NAME_NUM_CHARACTERS,
    CastMember,
    CastMemberType,
)
from src.core.cast_member.gateway.cast_member_gateway import (
    AbstractCastMemberRepository,
)


@pytest.fixture
def actor_cast_member() -> CastMember:
    return CastMember(name="John", type="ACTOR")


@pytest.fixture
def mocked_cast_member_repository():
    return create_autospec(AbstractCastMemberRepository)


class TestUpdateCastMember:
    def test_update_cast_member_name_success(
        self,
        actor_cast_member: CastMember,
        mocked_cast_member_repository: MagicMock,
    ):
        mocked_cast_member_repository.get_by_id.return_value = actor_cast_member
        initial_actor_cast_member = CastMember(**asdict(actor_cast_member))
        new_name = "Jonathan"
        input = UpdateCastMember.Input(
            id=actor_cast_member.id,
            name=new_name,
        )

        use_case = UpdateCastMember(repository=mocked_cast_member_repository)

        use_case.execute(input=input)

        mocked_cast_member_repository.get_by_id.assert_called_once_with(
            id=actor_cast_member.id,
        )

        expected_updated_cast_member = CastMember(
            id=actor_cast_member.id,
            name=new_name,
            type=actor_cast_member.type,
        )

        mocked_cast_member_repository.update.assert_called_once_with(
            cast_member=expected_updated_cast_member
        )
        cast_member_updated: CastMember = (
            mocked_cast_member_repository
            .update
            .call_args_list[0]
            .kwargs
        )["cast_member"]

        assert cast_member_updated.id == initial_actor_cast_member.id
        assert cast_member_updated.name == input.name
        assert cast_member_updated.type == initial_actor_cast_member.type

    def test_update_cast_member_type_success(
        self,
        actor_cast_member: CastMember,
        mocked_cast_member_repository: MagicMock,
    ):
        mocked_cast_member_repository.get_by_id.return_value = actor_cast_member
        initial_actor_cast_member = CastMember(**asdict(actor_cast_member))

        new_type = "DIRECTOR"
        input = UpdateCastMember.Input(
            id=actor_cast_member.id,
            type=new_type,
        )

        use_case = UpdateCastMember(repository=mocked_cast_member_repository)

        use_case.execute(input=input)

        mocked_cast_member_repository.get_by_id.assert_called_once_with(
            id=actor_cast_member.id,
        )

        expected_updated_cast_member = CastMember(
            id=actor_cast_member.id,
            name=actor_cast_member.name,
            type=new_type,
        )

        mocked_cast_member_repository.update.assert_called_once_with(
            cast_member=expected_updated_cast_member
        )
        cast_member_updated: CastMember = (
            mocked_cast_member_repository
            .update
            .call_args_list[0]
            .kwargs
        )["cast_member"]

        assert cast_member_updated.id == initial_actor_cast_member.id
        assert cast_member_updated.name == initial_actor_cast_member.name
        assert cast_member_updated.type == input.type

    def test_update_cast_member_invalid_name_length_error(
        self,
        actor_cast_member: CastMember,
        mocked_cast_member_repository: MagicMock,
    ):
        mocked_cast_member_repository.get_by_id.return_value = actor_cast_member

        input = UpdateCastMember.Input(
            id=actor_cast_member.id,
            name="J" * (MAX_CAST_MEMBER_NAME_NUM_CHARACTERS + 1),
        )

        use_case = UpdateCastMember(repository=mocked_cast_member_repository)

        with pytest.raises(
            InvalidCastMemberData,
            match=(
                "'name' must have less than "
                f"{MAX_CAST_MEMBER_NAME_NUM_CHARACTERS} characters"
            ),
        ):
            use_case.execute(input=input)

        mocked_cast_member_repository.get_by_id.assert_called_once_with(
            id=actor_cast_member.id,
        )

        mocked_cast_member_repository.update.assert_not_called()

    def test_update_cast_member_invalid_name_content_error(
        self,
        actor_cast_member: CastMember,
        mocked_cast_member_repository: MagicMock,
    ):
        mocked_cast_member_repository.get_by_id.return_value = actor_cast_member

        input = UpdateCastMember.Input(
            id=actor_cast_member.id,
            name="",
        )

        use_case = UpdateCastMember(repository=mocked_cast_member_repository)

        with pytest.raises(
            InvalidCastMemberData,
            match="'name' must not be empty",
        ):
            use_case.execute(input=input)

        mocked_cast_member_repository.get_by_id.assert_called_once_with(
            id=actor_cast_member.id,
        )

        mocked_cast_member_repository.update.assert_not_called()

    def test_update_cast_member_invalid_type_error(
        self,
        actor_cast_member: CastMember,
        mocked_cast_member_repository: MagicMock,
    ):
        mocked_cast_member_repository.get_by_id.return_value = actor_cast_member

        input = UpdateCastMember.Input(
            id=actor_cast_member.id,
            type="DOES_NOT_EXIST_TYPE",
        )

        use_case = UpdateCastMember(repository=mocked_cast_member_repository)

        valid_types = ", ".join(repr(str(t)) for t in CastMemberType)
        with pytest.raises(
            InvalidCastMemberData,
            match=f"Type must be one of: {valid_types}",
        ):
            use_case.execute(input=input)

        mocked_cast_member_repository.get_by_id.assert_called_once_with(
            id=actor_cast_member.id,
        )

        mocked_cast_member_repository.update.assert_not_called()

    def test_update_cast_member_does_not_exist_error(
        self,
        mocked_cast_member_repository: MagicMock,
    ):
        mocked_cast_member_repository.get_by_id.return_value = None

        does_not_exist_actor_id = uuid4()
        input = UpdateCastMember.Input(
            id=does_not_exist_actor_id,
            name="John",
            type="ACTOR",
        )

        use_case = UpdateCastMember(repository=mocked_cast_member_repository)

        with pytest.raises(CastMemberNotFound):
            use_case.execute(input=input)

        mocked_cast_member_repository.get_by_id.assert_called_once_with(
            id=does_not_exist_actor_id,
        )

        mocked_cast_member_repository.update.assert_not_called()
