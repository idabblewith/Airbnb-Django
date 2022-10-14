from django.contrib import admin
from .models import House

# Register your models here.


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "price_per_night",
        "pets_allowed",
    ]
    list_filter = [
        "price_per_night",
        "pets_allowed",
    ]
    search_fields = [
        "address__startswith",
    ]

    # https://docs.djangoproject.com/en/4.1/ref/contrib/admin/
    # fields = (
    #     "name",
    #     "address",
    #     [
    #         "price_per_night",
    #         "pets_allowed",
    #     ],
    # )
