# models.py

from django.db import models
from django.utils import timezone

from article.models import Article
from utilisateur.models import Client


class Cart(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    articles = models.ManyToManyField(Article, through='CartItem')
    created_at = models.DateTimeField(default=timezone.now)

    def get_total_price(self):
        total = 0
        cart_items = CartItem.objects.filter(cart=self)
        for item in cart_items:
            total += item.article.price * item.quantity  # Use 'quantity' here
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
