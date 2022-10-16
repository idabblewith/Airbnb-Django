from django.contrib import admin
from .models import Booking

# Register your models here.


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        "kind",
        "user",
        "check_in",
        "check_out",
        "guests",
    ]

    list_filter = [
        "guests",
        "check_in",
    ]
