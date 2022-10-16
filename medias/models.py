from django.db import models
from common.models import CommonModel

# Create your models here.


class Photo(CommonModel):
    """Def for Photos"""

    file = models.ImageField()
    description = models.CharField(max_length=100)
    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return "Photo File"


class Video(CommonModel):
    """Def for Videos"""

    file = models.FileField()
    experience = models.OneToOneField(
        "experiences.Experience",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return "Video File"