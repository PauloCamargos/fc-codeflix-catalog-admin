from unittest.mock import MagicMock, create_autospec

import pytest

from src.core.cast_member.application.create_cast_member import CreateCastMember
from src.core.cast_member.application.errors import InvalidCastMemberData
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


class TestCreateCastMember:
    def test_create_cast_member_invalid_name_length_error(
        self,
        mocked_cast_member_repository: MagicMock,
    ):
        use_case = CreateCastMember(
            repository=mocked_cast_member_repository,
        )
        name = "J" * (MAX_CAST_MEMBER_NAME_NUM_CHARACTERS + 1)
        input = CreateCastMember.Input(name=name, type=CastMemberType.ACTOR)
        with pytest.raises(
            InvalidCastMemberData,
            match=(
                "'name' must have less than "
                f"{MAX_CAST_MEMBER_NAME_NUM_CHARACTERS} characters"
            ),
        ):
            use_case.execute(input=input)

        mocked_cast_member_repository.save.assert_not_called()

    def test_create_cast_member_invalid_name_content_error(
        self,
        mocked_cast_member_repository: MagicMock,
    ):
        use_case = CreateCastMember(
            repository=mocked_cast_member_repository,
        )
        input = CreateCastMember.Input(name="", type=CastMemberType.ACTOR)
        with pytest.raises(
            InvalidCastMemberData,
            match="'name' must not be empty",
        ):
            use_case.execute(input=input)

        mocked_cast_member_repository.save.assert_not_called()

    def test_create_cast_member_invalid_type_error(
        self,
        mocked_cast_member_repository: MagicMock,
    ):
        use_case = CreateCastMember(
            repository=mocked_cast_member_repository,
        )
        input = CreateCastMember.Input(name="John Doe", type="DOES_NOT_EXIST_TYPE")
        valid_types = ", ".join(repr(str(t)) for t in CastMemberType)
        with pytest.raises(
            InvalidCastMemberData,
            match=f"Type must be one of: {valid_types}",
        ):
            use_case.execute(input=input)

        mocked_cast_member_repository.save.assert_not_called()

    def test_create_cast_member_success(
        self,
        mocked_cast_member_repository: MagicMock,
    ):
        use_case = CreateCastMember(
            repository=mocked_cast_member_repository,
        )
        input = CreateCastMember.Input(
            name="John",
            type="ACTOR",
        )

        output = use_case.execute(input=input)

        mocked_cast_member_repository.save.assert_called_once_with(
            cast_member=CastMember(
                id=output.id,
                name=input.name,
                type=input.type,
            ),
        )
