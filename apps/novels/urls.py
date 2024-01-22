from django.urls import path

from apps.novels import views

app_name = "novels"

urlpatterns = [
    path("search", views.search, name="search"),
    path("details", views.details, name="details"),
    path("read", views.read, name="read"),
]
