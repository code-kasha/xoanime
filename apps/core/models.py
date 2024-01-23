from django.db import models


class Genres(models.Model):
    key = models.CharField(max_length=255, unique=True)
    value = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.value}"
