from django.urls import path
from apps.manga import views

app_name = "manga"

urlpatterns = [
    path("search", views.search, name="search"),
    path("details", views.details, name="details"),
    # path("read", views.read, name="read"),
]
