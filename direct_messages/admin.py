from django.contrib import admin
from .models import ChatRoom, Message

# Register your models here.


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "created_at",
        "updated_at",
    ]

    list_filter = [
        "created_at",
    ]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        "room",
        "user",
        "text",
        "created_at",
    ]
    list_filter = [
        "user",
        "created_at",
    ]
