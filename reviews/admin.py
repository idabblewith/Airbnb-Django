from django.contrib import admin
from .models import Review

# Register your models here.


class WordFilter(admin.SimpleListFilter):

    title = "Words"
    parameter_name = "potato"

    def lookups(self, request, model_admin):
        return [("good", "Good"), ("great", "Great"), ("awesome", "Awesome")]

    def queryset(self, request, queryset):
        word = self.value()
        if word:
            return queryset.filter(payload__contains=word)
        else:
            return queryset
        # replace queryset with reviews in this case


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["__str__", "payload"]
    list_filter = [
        WordFilter,
        "rating",
        "user__is_host",
        "room__category",
    ]
