from django.urls import path

from apps.core import views

urlpatterns = [
    path("", views.index, name="index"),
    path("clear", views.clear, name="clear"),
    path("search", views.search, name="search"),
]
