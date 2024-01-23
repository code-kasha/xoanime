from django.urls import path
from apps.anime import views

app_name = "anime"

urlpatterns = [
    path("search", views.search, name="search"),
    path("details", views.details, name="details"),
    path("watch", views.watch, name="watch"),
]
