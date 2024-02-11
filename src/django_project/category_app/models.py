from uuid import uuid4

from django.db import models


class Category(models.Model):
    class Meta:
        db_table = "category"
        verbose_name_plural = "categories"

    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name
