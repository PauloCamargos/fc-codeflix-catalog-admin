from uuid import uuid4

from django.db import models


class Genre(models.Model):
    class Meta:
        app_label = "genre_app"
        db_table = "genre"
        verbose_name_plural = "genres"

    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    categories = models.ManyToManyField(
        to="category_app.Category",
        related_name="genres",
    )

    def __str__(self) -> str:
        return self.name
