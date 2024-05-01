from typing import Any
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
from src.core.cast_member.tests.conftest import cast_member_repository
from src.core.shared import settings
from src.core.shared.application.errors import InvalidOrderByRequested


class TestListCastMember:
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

        expected_cast_members_per_page: dict[int, list[Any]] = {
            1: [
                    CastMemberOutput(
                        id=actor_aston_cast_member.id,
                        name=actor_aston_cast_member.name,
                        type=actor_aston_cast_member.type,
                    ),
                    CastMemberOutput(
                        id=director_jane_cast_member.id,
                        name=director_jane_cast_member.name,
                        type=director_jane_cast_member.type,
                    ),
            ],
            2: [
                    CastMemberOutput(
                        id=actor_john_cast_member.id,
                        name=actor_john_cast_member.name,
                        type=actor_john_cast_member.type,
                    ),
                    CastMemberOutput(
                        id=director_ray_cast_member.id,
                        name=director_ray_cast_member.name,
                        type=director_ray_cast_member.type,
                    ),
            ],
            3: [
                    CastMemberOutput(
                        id=actor_will_cast_member.id,
                        name=actor_will_cast_member.name,
                        type=actor_will_cast_member.type,
                    ),
            ],
        }

        overriden_page_size = 2

        expected_output = ListCastMembers.Output(
            data=expected_cast_members_per_page[page],
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
