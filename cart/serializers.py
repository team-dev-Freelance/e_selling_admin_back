from rest_framework import serializers
from .models import Cart
from article.serializers import ArticleSerializer
from client.serializers import ClientSerializer

class CartSerializer(serializers.ModelSerializer):
    client = ClientSerializer()  # Sérialisation des détails du client
    article = ArticleSerializer()  # Sérialisation des détails de l'article

    class Meta:
        model = Cart
        fields = ['id', 'client', 'article', 'quantity', 'created_at']
