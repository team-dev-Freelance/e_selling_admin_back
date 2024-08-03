from django.db import models
from categorie.models import Categorie
from member.models import Member


class Article(models.Model):
    label = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=False)
    logo = models.ImageField(upload_to='photos/', default='default_logo.png')

    def __str__(self):
        return self.label
