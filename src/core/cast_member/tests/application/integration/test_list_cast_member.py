import pytest

from src.core.cast_member.application.list_cast_member import ListCastMember
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.gateway.cast_member_gateway import (
    AbstractCastMemberRepository,
)
from src.core.cast_member.infra.in_memory_cast_member_repository import (
    InMemoryCastMemberRepository,
)
from src.core.shared.application.errors import InvalidOrderByRequested


@pytest.fixture
def actor_cast_member() -> CastMember:
    return CastMember(name="John", type="ACTOR")


@pytest.fixture
def director_cast_member() -> CastMember:
    return CastMember(name="Amber", type="DIRECTOR")


@pytest.fixture
def cast_member_repository(
    actor_cast_member: CastMember,
) -> AbstractCastMemberRepository:
    return InMemoryCastMemberRepository(
        cast_members=[
            actor_cast_member,
        ]
    )


class TestListCastMember:
    def test_list_cast_member_no_order_by_success(
        self,
        actor_cast_member: CastMember,
        cast_member_repository: AbstractCastMemberRepository,
    ):

        input = ListCastMember.Input()

        use_case = ListCastMember(repository=cast_member_repository)

        output = use_case.execute(input=input)

        assert len(output.data) == 1
        [found_cast_member_output] = output.data
        assert found_cast_member_output.id == actor_cast_member.id
        assert found_cast_member_output.name == actor_cast_member.name
        assert found_cast_member_output.type == actor_cast_member.type

    @pytest.mark.parametrize(
            "order_by",
            ["name", "-name"]
    )
    def test_list_cast_member_order_by_success(
        self,
        order_by: str,
        actor_cast_member: CastMember,
        director_cast_member: CastMember,
        cast_member_repository: AbstractCastMemberRepository,
    ):
        cast_member_repository.save(cast_member=director_cast_member)

        input = ListCastMember.Input(order_by=order_by)

        use_case = ListCastMember(repository=cast_member_repository)

        output = use_case.execute(input=input)

        expected_cast_members = sorted(
            [
                director_cast_member,
                actor_cast_member,
            ],
            key=lambda cast_member: cast_member.name,
            reverse=order_by.startswith("-"),
        )

        expected_output = ListCastMember.Output(
            data=[
                ListCastMember.CastMemberOutput(
                    id=cast_member.id,
                    name=cast_member.name,
                    type=cast_member.type,
                )
                for cast_member in expected_cast_members
            ]
        )

        assert expected_output == output

    def test_list_cast_member_invalid_order_by_error(
        self,
    ):
        order_by = "potato"
        valid_order_by_attrs = ", ".join(
            repr(attr)
            for attr in ListCastMember.Input.get_valid_order_by_attributes()
        )

        with pytest.raises(
            InvalidOrderByRequested,
            match=(
                f"Provided ordering {repr(order_by)} "
                f"is not one of: {valid_order_by_attrs}"
            ),
        ):
            ListCastMember.Input(order_by=order_by)
