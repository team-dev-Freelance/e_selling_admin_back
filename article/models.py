import os

from django.db import models
from categorie.models import Categorie
from utilisateur.models import Member


# from member.models import Member


class Article(models.Model):
    label = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=False)
    logo = models.ImageField(upload_to='photos/', default='default_logo.png')
    logo_name = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if self.logo:
            self.logo_name = os.path.basename(self.logo.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.label
