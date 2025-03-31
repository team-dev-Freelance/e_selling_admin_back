from django.db import models


class Categorie(models.Model):
    label = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.label
