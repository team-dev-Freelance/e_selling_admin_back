import os

from django.db import models
from categorie.models import Categorie
from utilisateur.models import Member


# from member.models import Member


from cloudinary.models import CloudinaryField


class Article(models.Model):
    label = models.CharField(max_length=255) # Mettre a unique
    price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=False)
    logo = models.ImageField(upload_to='photos/', default='media/photos/logo.jpeg')
    # logo_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.label

