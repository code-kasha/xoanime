from django.urls import path
from apps.news import views

app_name = "news"

urlpatterns = [
    path("", views.feed, name="feed"),
    path("details", views.details, name="details"),
]
