
from dataclasses import asdict
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


class TestUpdateCastMember:
    def test_update_cast_member_name_success(
        self,
        actor_cast_member: CastMember,
        cast_member_repository: AbstractCastMemberRepository,
    ):
        initial_actor_cast_member = CastMember(**asdict(actor_cast_member))

        input = UpdateCastMember.Input(
            id=actor_cast_member.id,
            name="Jonathan",
        )

        use_case = UpdateCastMember(repository=cast_member_repository)

        use_case.execute(input=input)

        cast_member_updated = cast_member_repository.get_by_id(
            id=actor_cast_member.id,
        )

        assert cast_member_updated.id == initial_actor_cast_member.id
        assert cast_member_updated.name == input.name
        assert cast_member_updated.type == initial_actor_cast_member.type

    def test_update_cast_member_type_success(
        self,
        actor_cast_member: CastMember,
        cast_member_repository: AbstractCastMemberRepository,
    ):
        initial_actor_cast_member = CastMember(**asdict(actor_cast_member))

        input = UpdateCastMember.Input(
            id=actor_cast_member.id,
            type="DIRECTOR",
        )

        use_case = UpdateCastMember(repository=cast_member_repository)

        use_case.execute(input=input)

        cast_member_updated = cast_member_repository.get_by_id(
            id=actor_cast_member.id,
        )

        assert cast_member_updated.id == initial_actor_cast_member.id
        assert cast_member_updated.name == initial_actor_cast_member.name
        assert cast_member_updated.type == input.type

    def test_update_cast_member_invalid_name_length_error(
        self,
        actor_cast_member: CastMember,
        cast_member_repository: AbstractCastMemberRepository,
    ):

        input = UpdateCastMember.Input(
            id=actor_cast_member.id,
            name="J" * (MAX_CAST_MEMBER_NAME_NUM_CHARACTERS + 1),
        )

        use_case = UpdateCastMember(repository=cast_member_repository)

        with pytest.raises(
            InvalidCastMemberData,
            match=(
                "'name' must have less than "
                f"{MAX_CAST_MEMBER_NAME_NUM_CHARACTERS} characters"
            ),
        ):
            use_case.execute(input=input)

    def test_update_cast_member_invalid_name_content_error(
        self,
        actor_cast_member: CastMember,
        cast_member_repository: AbstractCastMemberRepository,
    ):
        input = UpdateCastMember.Input(
            id=actor_cast_member.id,
            name="",
        )

        use_case = UpdateCastMember(repository=cast_member_repository)

        with pytest.raises(
            InvalidCastMemberData,
            match="'name' must not be empty",
        ):
            use_case.execute(input=input)

    def test_update_cast_member_invalid_type_error(
        self,
        actor_cast_member: CastMember,
        cast_member_repository: AbstractCastMemberRepository,
    ):

        input = UpdateCastMember.Input(
            id=actor_cast_member.id,
            type="DOES_NOT_EXIST_TYPE",
        )

        use_case = UpdateCastMember(repository=cast_member_repository)

        valid_types = ", ".join(repr(str(t)) for t in CastMemberType)
        with pytest.raises(
            InvalidCastMemberData,
            match=f"Type must be one of: {valid_types}",
        ):
            use_case.execute(input=input)

    def test_update_cast_member_does_not_exist_error(
        self,
        cast_member_repository: AbstractCastMemberRepository,
    ):
        does_not_exist_actor_id = uuid4()
        input = UpdateCastMember.Input(
            id=does_not_exist_actor_id,
            name="John",
            type="ACTOR",
        )

        use_case = UpdateCastMember(repository=cast_member_repository)

        with pytest.raises(CastMemberNotFound):
            use_case.execute(input=input)
