from unittest.mock import patch

import pytest

from src.core.cast_member.application.list_cast_member import (
    CastMemberOutput,
    ListCastMembers,
)
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.gateway.cast_member_gateway import (
    AbstractCastMemberRepository,
)
from src.core.cast_member.infra.in_memory_cast_member_repository import (
    InMemoryCastMemberRepository,
)
from src.core.shared import settings
from src.core.shared.application.errors import (
    InvalidOrderByRequested,
    InvalidPageRequested,
)


class TestListCastMember:
    def test_list_cast_members_empty_success(
        self,
        cast_member_repository: InMemoryCastMemberRepository,
    ) -> None:

        list_cast_members = ListCastMembers(repository=cast_member_repository)

        input = ListCastMembers.Input()
        output = list_cast_members.execute(input=input)

        expected_output: ListCastMembers.Output[CastMemberOutput] = (
            ListCastMembers.Output(
                data=[],
                meta=ListCastMembers.Meta(
                    page=1,
                    per_page=settings.REPOSITORY["page_size"],
                    total=0,
                )
            )
        )

        assert expected_output == output

    @pytest.mark.parametrize(
        "page",
        [1, 2, 3],
    )
    def test_list_cast_member_pagination_success(
        self,
        page: int,
        cast_member_repository: InMemoryCastMemberRepository,
        actor_aston_cast_member: CastMember,
        actor_john_cast_member: CastMember,
        actor_will_cast_member: CastMember,
        director_ray_cast_member: CastMember,
        director_jane_cast_member: CastMember,
    ):
        cast_member_repository.save(actor_aston_cast_member)
        cast_member_repository.save(actor_john_cast_member)
        cast_member_repository.save(actor_will_cast_member)
        cast_member_repository.save(director_jane_cast_member)
        cast_member_repository.save(director_ray_cast_member)

        expected_cast_members_per_page: dict[int, list[CastMember]] = {
            1: [
                actor_aston_cast_member,
                director_jane_cast_member,
            ],
            2: [
                actor_john_cast_member,
                director_ray_cast_member,
            ],
            3: [
                actor_will_cast_member,
            ],
        }

        overriden_page_size = 2

        expected_output = ListCastMembers.Output(
            data=[
                CastMemberOutput(
                    id=cast_member.id,
                    name=cast_member.name,
                    type=cast_member.type,
                )
                for cast_member in expected_cast_members_per_page[page]
            ],
            meta=ListCastMembers.Meta(
                page=page,
                per_page=overriden_page_size,
                total=5,
            )
        )

        use_case = ListCastMembers(repository=cast_member_repository)
        input = ListCastMembers.Input(order_by="name", page=page)

        with patch.dict(
            settings.REPOSITORY,
            {"page_size": overriden_page_size},
        ):
            output = use_case.execute(input=input)

        assert output == expected_output

    @pytest.mark.parametrize(
        "page",
        [-1, 0, "-1", "0", 10_000],
    )
    def test_list_catgories_pagination_invalid_page_error(
        self,
        page: int,
        cast_member_repository: InMemoryCastMemberRepository,
    ):
        input = ListCastMembers.Input(
            order_by=None,
            page=page,
        )
        use_case = ListCastMembers(repository=cast_member_repository)

        with pytest.raises(
            InvalidPageRequested,
            match=(
                f"Provided page {page} is not valid"
            ),
        ):
            use_case.execute(input=input)

    def test_list_cast_member_no_order_by_success(
        self,
        actor_john_cast_member: CastMember,
        actor_aston_cast_member: CastMember,
        cast_member_repository: InMemoryCastMemberRepository,
    ):
        cast_member_repository.save(actor_john_cast_member)
        cast_member_repository.save(actor_aston_cast_member)

        input = ListCastMembers.Input(order_by=None)

        use_case = ListCastMembers(repository=cast_member_repository)

        output = use_case.execute(input=input)

        expected_cast_members = sorted(
            [
                actor_aston_cast_member,
                actor_john_cast_member,
            ],
            key=lambda cast_member: getattr(
                cast_member,
                ListCastMembers.default_order_by_field,
            ),
            reverse=ListCastMembers.default_order_by_field.startswith("-"),
        )

        expected_output = ListCastMembers.Output(
            data=[
                CastMemberOutput(
                    id=cast_member.id,
                    name=cast_member.name,
                    type=cast_member.type,
                )
                for cast_member in expected_cast_members
            ],
            meta=ListCastMembers.Meta(
                page=1,
                per_page=settings.REPOSITORY["page_size"],
                total=2,
            )
        )

        assert output == expected_output

    @pytest.mark.parametrize(
            "order_by",
            ["name", "-name"]
    )
    def test_list_cast_member_order_by_success(
        self,
        order_by: str,
        actor_john_cast_member: CastMember,
        actor_aston_cast_member: CastMember,
        cast_member_repository: AbstractCastMemberRepository,
    ):
        cast_member_repository.save(actor_john_cast_member)
        cast_member_repository.save(actor_aston_cast_member)

        input = ListCastMembers.Input(order_by=order_by)

        use_case = ListCastMembers(repository=cast_member_repository)

        output = use_case.execute(input=input)

        expected_cast_members = sorted(
            [
                actor_aston_cast_member,
                actor_john_cast_member,
            ],
            key=lambda cast_member: cast_member.name,
            reverse=order_by.startswith("-"),
        )

        expected_output = ListCastMembers.Output(
            data=[
                CastMemberOutput(
                    id=cast_member.id,
                    name=cast_member.name,
                    type=cast_member.type,
                )
                for cast_member in expected_cast_members
            ],
            meta=ListCastMembers.Meta(
                page=1,
                per_page=settings.REPOSITORY["page_size"],
                total=2,
            )
        )

        assert expected_output == output

    def test_list_cast_member_invalid_order_by_error(
        self,
        cast_member_repository: AbstractCastMemberRepository,
    ):
        order_by = "potato"
        valid_order_by_attrs = ", ".join(
            repr(attr)
            for attr in ListCastMembers.order_by_fields
        )

        input = ListCastMembers.Input(order_by=order_by)

        use_case = ListCastMembers(repository=cast_member_repository)

        with pytest.raises(
            InvalidOrderByRequested,
            match=(
                f"Provided ordering {repr(order_by)} "
                f"is not one of: {valid_order_by_attrs}"
            ),
        ):
            use_case.execute(input=input)
