
from uuid import UUID, uuid4

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from src.core.cast_member.application.list_cast_member import (
    DEFAULT_CAST_MEMBER_LIST_ORDER,
)
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.gateway.cast_member_gateway import (
    AbstractCastMemberRepository,
)
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository

BASE_CAST_MEMBERS_URL = "/api/cast_members/"


@pytest.mark.django_db
class TestListAPI:
    @pytest.mark.parametrize(
        "order_by",
        [None, "name", "-name"]
    )
    def test_list_cast_members_success(
        self,
        order_by,
        actor_cast_member_model: CastMember,
        director_cast_member_model: CastMember,
    ):
        expected_cast_members = [
            {
                "id": str(actor_cast_member_model.id),
                "name": actor_cast_member_model.name,
                "type": actor_cast_member_model.type,
            },
            {
                "id": str(director_cast_member_model.id),
                "name": director_cast_member_model.name,
                "type": director_cast_member_model.type,
            }
        ]

        if order_by is None:
            order_by = DEFAULT_CAST_MEMBER_LIST_ORDER
            params = {}
        else:
            params = {
                "order_by": order_by,
            }

        expected_data = {
            "data": sorted(
                expected_cast_members,
                key=lambda item: item[order_by.strip("-")],
                reverse=order_by.startswith("-"),
            )
        }

        response = APIClient().get(BASE_CAST_MEMBERS_URL, params)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    def test_list_no_cast_members(
        self,
    ):
        expected_data = {"data": []}

        response = APIClient().get(path=BASE_CAST_MEMBERS_URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    @pytest.mark.parametrize(
        "page",
        [1, 2, 3],
    )
    def test_list_categories_with_pagination(
        self,
        page: int,
        movie_category_model: Category,
        serie_category_model: Category,
        documentary_category_model: Category,
        music_clip_category_model: Category,
        lecture_category_model: Category,
    ):
        expected_categories_per_page: dict[int, list[Any]] = {
            1: [
                    {
                        "id": str(serie_category_model.id),
                        "name": serie_category_model.name,
                        "description": serie_category_model.description,
                        "is_active": serie_category_model.is_active,
                    },
                    {
                        "id": str(music_clip_category_model.id),
                        "name": music_clip_category_model.name,
                        "description": music_clip_category_model.description,
                        "is_active": music_clip_category_model.is_active,
                    },
            ],
            2: [
                    {
                        "id": str(movie_category_model.id),
                        "name": movie_category_model.name,
                        "description": movie_category_model.description,
                        "is_active": movie_category_model.is_active,
                    },
                    {
                        "id": str(lecture_category_model.id),
                        "name": lecture_category_model.name,
                        "description": lecture_category_model.description,
                        "is_active": lecture_category_model.is_active,
                    },
            ],
            3: [
                    {
                        "id": str(documentary_category_model.id),
                        "name": documentary_category_model.name,
                        "description": documentary_category_model.description,
                        "is_active": documentary_category_model.is_active,
                    },
            ],
        }

        params = {
            "order_by": "-description",
            "page": page,
        }

        expected_data = {
            "data": expected_categories_per_page[page]
        }

        overriden_page_size = 2

        url = "/api/categories/"
        with patch.dict(
            core_settings.REPOSITORY,
            {"page_size": overriden_page_size},
        ):
            response = APIClient().get(url, params)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data



@pytest.mark.django_db
class TestCreateAPI:
    def test_create_cast_member_invalid_name_content_data_error(
        self,
    ):
        post_data = {
            "name": "",
            "type": "ACTOR",
        }

        response = APIClient().post(
            path=BASE_CAST_MEMBERS_URL,
            data=post_data,
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"name": ["This field may not be blank."]}

    def test_create_cast_member_invalid_type_content_data_error(
        self,
    ):
        post_data = {
            "name": "John",
            "type": "INVALID_TYPE",
        }

        response = APIClient().post(
            path=BASE_CAST_MEMBERS_URL,
            data=post_data,
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"type": ['"INVALID_TYPE" is not a valid choice.']}

    def test_create_cast_member_success(
        self,
        cast_member_repository: AbstractCastMemberRepository,
    ):
        post_data = {
            "name": "John",
            "type": "ACTOR",
        }

        response = APIClient().post(
            path=BASE_CAST_MEMBERS_URL,
            data=post_data,
        )

        assert response.status_code == status.HTTP_201_CREATED

        created_cast_member_id = UUID(response.data["id"])

        created_cast_member = cast_member_repository.get_by_id(
            id=created_cast_member_id,
        )

        assert created_cast_member is not None

        assert created_cast_member.name == post_data["name"]
        assert created_cast_member.type == post_data["type"]


@pytest.mark.django_db
class TestUpdateAPI:
    def test_update_cast_member_invalid_payload_error(
        self,
        actor_cast_member_model: CastMember,
    ):

        post_data = {
            "name": "",
        }

        url = BASE_CAST_MEMBERS_URL + f"{str(actor_cast_member_model.id)}/"
        response = APIClient().put(url, data=post_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["This field may not be blank."],
            "type": ['This field is required.'],
        }

    def test_update_cast_member_invalid_id_error(
        self,
        actor_cast_member_model: CastMember,
    ):

        post_data = {
            "type": actor_cast_member_model.type,
        }

        url = BASE_CAST_MEMBERS_URL + "invalid-id/"
        response = APIClient().put(url, data=post_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "id": ["Must be a valid UUID."],
            "name": ['This field is required.'],
        }

    def test_update_non_existing_cast_member_error(
        self,
    ):
        post_data = {
            "name": "Jonh",
            "type": "ACTOR",
        }

        url = BASE_CAST_MEMBERS_URL + f"/{str(uuid4())}/"
        response = APIClient().put(url, data=post_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_cast_member_valid_payload_success(
        self,
        actor_cast_member_model: CastMember,
        cast_member_repository: DjangoORMCastMemberRepository,
    ):

        post_data = {
            "name": "Jonathan",
            "type": "DIRECTOR",
        }

        url = BASE_CAST_MEMBERS_URL + f"{str(actor_cast_member_model.id)}/"
        response = APIClient().put(url, data=post_data)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data["id"] == str(actor_cast_member_model.id)

        updated_cast_member = cast_member_repository.get_by_id(
            id=UUID(response.data["id"])
        )

        assert updated_cast_member is not None

        assert updated_cast_member.name == post_data["name"]
        assert updated_cast_member.type == post_data["type"]


@pytest.mark.django_db
class TestDeleteCastMember:
    def test_delete_cast_member_success(
        self,
        actor_cast_member_model: CastMember,
        cast_member_repository: DjangoORMCastMemberRepository,
    ):
        url = BASE_CAST_MEMBERS_URL + f"{str(actor_cast_member_model.id)}/"
        response = APIClient().delete(path=url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        found_cast_member = cast_member_repository.get_by_id(
            id=actor_cast_member_model.id
        )
        assert found_cast_member is None

    def test_delete_cast_member_non_existing_id_error(
        self,
    ):
        url = f"/api/categories/{str(uuid4())}/"

        response = APIClient().delete(path=url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_cast_member_non_invalid_id_error(
        self,
    ):
        url = "/api/cast_members/invalid-id/"

        response = APIClient().delete(path=url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "id": ["Must be a valid UUID."],
        }
