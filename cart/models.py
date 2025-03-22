from django.db import models
from django.utils import timezone
from article.models import Article
from utilisateur.models import Client


class Cart(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

