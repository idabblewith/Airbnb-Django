from django.db import models
from common.models import CommonModel

# Create your models here.


class Experience(CommonModel):
    """Experience Model Definition"""

    name = models.CharField(max_length=250)
    description = models.TextField()
    country = models.CharField(
        max_length=50,
        default="Australia",
    )
    city = models.CharField(
        max_length=80,
        default="Perth",
    )
    host = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    price = models.PositiveIntegerField()
    address = models.CharField(
        max_length=250,
    )
    start = models.TimeField()
    end = models.TimeField()
    perks = models.ManyToManyField("experiences.Perk")
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Perk(CommonModel):
    """What's included with each experience"""

    name = models.CharField(max_length=100)
    info = models.CharField(
        max_length=250,
        blank=True,
        default="",
    )
    explanation = models.TextField(
        blank=True,
        default="",
    )

    def __str__(self):
        return self.name
