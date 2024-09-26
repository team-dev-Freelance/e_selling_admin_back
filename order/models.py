from django.db import models
from article.models import Article
from utilisateur.models import Client


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_command = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'En cours'), ('shipped', 'Expédiée'), ('delivered', 'Livrée')])
    articles = models.ManyToManyField(Article, through='OrderItem')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()