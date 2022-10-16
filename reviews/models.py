from django.db import models
from common.models import CommonModel

# Create your models here.


class Review(CommonModel):

    """Reviews from a User about Room or Experience"""

    def __str__(self):
        return f"{self.user} | {self.rating}"

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    room = models.ForeignKey(
        "rooms.Room",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    payload = models.TextField()
    rating = models.PositiveIntegerField()
