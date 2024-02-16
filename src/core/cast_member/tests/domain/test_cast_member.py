from uuid import UUID, uuid4
import pytest

from src.core.cast_member.domain.cast_member import (
    MAX_CAST_MEMBER_NAME_NUM_CHARACTERS,
    CastMember,
    CastMemberType,
)
from src.core.cast_member.domain.errors import InvalidCastMemberTypeError


class TestCastMember:
    def test_create_cast_member_without_name(self):
        with pytest.raises(
            TypeError,
            match="missing 1 required positional argument: 'name'",
        ):
            CastMember(type=CastMemberType.ACTOR)

    def test_create_cast_member_without_type(self):
        with pytest.raises(
            TypeError,
            match="missing 1 required positional argument: 'type'",
        ):
            CastMember(name="John")

    def test_create_cast_member_invalid_type_error(self):
        valid_types = ", ".join(repr(str(t)) for t in CastMemberType)
        with pytest.raises(
            InvalidCastMemberTypeError,
            match=f"Type must be one of: {valid_types}",
        ):
            CastMember(name="John", type="DOES_NOT_EXIST_TYPE")

    def test_create_cast_member_do_not_provide_id_success(self):
        cast_member = CastMember(name="John", type="ACTOR")
        assert isinstance(
            cast_member.id,
            UUID,
        ), f"cast_member.id type was {type(cast_member.id)} instead of {UUID}"

    def test_create_cast_member_provide_all_values_success(self):
        cast_member = CastMember(id=uuid4(), name="John", type="ACTOR")
        assert isinstance(
            cast_member.id,
            UUID,
        ), f"cast_member.id type was {type(cast_member.id)} instead of {UUID}"


@pytest.fixture
def actor_cast_member() -> CastMember:
    return CastMember(name="John", type="ACTOR")


class TestUpdateCastMember:
    def test_update_cast_member_invalid_type_error(self, actor_cast_member: CastMember):
        new_type = "DOES_NOT_EXIST_TYPE"
        valid_types = ", ".join(repr(str(t)) for t in CastMemberType)
        with pytest.raises(
            InvalidCastMemberTypeError,
            match=f"Type must be one of: {valid_types}",
        ):
            actor_cast_member.update_type(type=new_type)

    def test_update_cast_member_valid_type_success(self, actor_cast_member: CastMember):
        new_type = "DIRECTOR"
        actor_cast_member.update_type(type=new_type)
        assert actor_cast_member.type == new_type

    def test_update_cast_member_invalid_name_length_error(
        self,
        actor_cast_member: CastMember,
    ):
        new_name = "H" * (MAX_CAST_MEMBER_NAME_NUM_CHARACTERS + 1)
        with pytest.raises(
            ValueError,
            match=(
                "'name' must have less than "
                f"{MAX_CAST_MEMBER_NAME_NUM_CHARACTERS} characters"
            ),
        ):
            actor_cast_member.update_name(name=new_name)

    def test_update_cast_member_invalid_empty_name_error(
        self, actor_cast_member: CastMember
    ):
        new_name = ""
        with pytest.raises(
            ValueError,
            match="'name' must not be empty",
        ):
            actor_cast_member.update_name(name=new_name)

    def test_update_cast_member_name_success(self, actor_cast_member: CastMember):
        new_name = "Jonathan"
        actor_cast_member.update_name(name=new_name)
        assert actor_cast_member.name == new_name


class TestCastMemberEquality:
    def test_when_cast_members_have_same_id_they_are_equal(self):
        common_id = uuid4()
        cast_member_1 = CastMember(id=common_id, name="John", type="ACTOR")
        cast_member_2 = CastMember(id=common_id, name="Jonathan", type="ACTOR")

        assert cast_member_1 == cast_member_2

    def test_when_cast_members_have_different_id_they_are_not_equal(self):
        id_1 = uuid4()
        id_2 = uuid4()
        cast_member_1 = CastMember(id=id_1, name="John", type="ACTOR")
        cast_member_2 = CastMember(id=id_2, name="Jonathan", type="ACTOR")

        assert cast_member_1 != cast_member_2
