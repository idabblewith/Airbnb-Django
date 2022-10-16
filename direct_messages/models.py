from django.db import models
from common.models import CommonModel

# Create your models here.


class ChatRoom(CommonModel):

    """Chat Room Model Def"""

    users = models.ManyToManyField(
        "users.User",
        related_name="chat_rooms",
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
        related_name="messages",
    )
    room = models.ForeignKey(
        "direct_messages.ChatRoom",
        on_delete=models.CASCADE,
        related_name="messages",
    )

    def __str__(self) -> str:
        return f"{self.user} says {self.text}"
