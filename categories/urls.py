from . import views
from django.urls import path

urlpatterns = [
    path("", views.Categories.as_view()),
    path("room", views.CategoryRoomKind.as_view()),
    path("experience", views.CategoryExperienceKind.as_view()),
    path("<int:pk>", views.CategoryDetail.as_view()),
]
