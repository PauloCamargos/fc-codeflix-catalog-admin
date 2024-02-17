from uuid import uuid4

from django.db import models

from src.core.cast_member.domain.cast_member import CastMemberType


def cast_member_choices() -> dict[str, str]:
    return {
        str(cast_member_type): str(cast_member_type)
        for cast_member_type in CastMemberType
    }


class CastMember(models.Model):
    class Meta:
        app_label = "cast_member_app"
        db_table = "cast_member"
        verbose_name_plural = "cast_members"

    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=cast_member_choices)

    def __str__(self) -> str:
        return self.name
