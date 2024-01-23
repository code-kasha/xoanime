from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("anime/", include("apps.anime.urls")),
    path("manga/", include("apps.manga.urls")),
    path("news/", include("apps.news.urls")),
    path("novels/", include("apps.novels.urls")),
]
