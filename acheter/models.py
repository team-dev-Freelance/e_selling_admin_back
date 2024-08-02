from django.db import models
from article.models import Article
from client.models import Client


# Create your models here.
class Acheter(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    createDate = models.DateField(auto_now_add=True, editable=False)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.total_price = self.get_total_price()
        super().save(*args, **kwargs)

    def get_total_price(self):
        # Calculer le prix total en multipliant la quantité par le prix de l'article
        return self.quantity * self.article.price

    def __str__(self):
        return f'{self.client.name} a acheté {self.quantity} de {self.article.label}'

