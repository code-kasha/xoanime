from django.urls import path
from apps.anime import views

app_name = "anime"

urlpatterns = [
    path("search", views.search, name="search"),
    path("details", views.details, name="details"),
    path("watch", views.watch, name="watch"),
    path("top", views.top, name="top"),
    path("genre", views.genre, name="genre"),
    path("recent", views.recent, name="recent"),
    path("popular", views.popular, name="popular"),
    path("movies", views.movies, name="movies"),
]
