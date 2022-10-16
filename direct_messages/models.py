from django.db import models
from common.models import CommonModel

# Create your models here.


class ChatRoom(CommonModel):

    """Chat Room Model Def"""

    users = models.ManyToManyField(
        "users.User",
    )

    def __str__(self) -> str:
        return "Chat Room"


class Message(CommonModel):

    """Message Model Def"""

    text = models.TextField()
    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    room = models.ForeignKey(
        "direct_messages.ChatRoom",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"{self.user} says {self.text}"
