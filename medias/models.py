from django.db import models
from common.models import CommonModel

# Create your models here.


class Photo(CommonModel):
    """Def for Photos"""

    file = models.URLField()
    description = models.CharField(max_length=100)
    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )

    def __str__(self) -> str:
        return "Photo File"


class Video(CommonModel):
    """Def for Videos"""

    file = models.URLField()
    experience = models.OneToOneField(
        "experiences.Experience",
        on_delete=models.CASCADE,
        related_name="videos",
    )

    def __str__(self) -> str:
        return "Video File"
