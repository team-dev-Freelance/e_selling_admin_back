from rest_framework import serializers
from article.models import Article
from utilisateur.models import Client
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    article_label = serializers.CharField(source='article.label', read_only=True)  # Affiche le nom de l'article
    article_price = serializers.DecimalField(source='article.price', max_digits=10, decimal_places=2,
                                             read_only=True)  # Affiche le prix de l'article
    article_id = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all(), source='article.id')

    class Meta:
        model = OrderItem
        fields = ['article_id', 'article_label', 'article_price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.username', read_only=True)  # Affiche le nom du client
    client_phone = serializers.CharField(source='client.phone',
                                         read_only=True)  # Affiche le numéro de téléphone du client
    articles = OrderItemSerializer(many=True, source='orderitem_set')  # Utilise le modèle intermédiaire
    total_price = serializers.SerializerMethodField()  # Champ pour le prix total de la commande

    class Meta:
        model = Order
        fields = ['id', 'client_name', 'client_phone', 'date_command', 'status', 'articles', 'total_price']

    def get_total_price(self, obj):
        # Calcule le prix total en fonction des articles et de leurs quantités
        total = 0
        for item in obj.orderitem_set.all():
            total += item.article.price * item.quantity
        return total

    def create(self, validated_data):
        articles_data = validated_data.pop('orderitem_set')  # Récupère les articles associés à la commande
        order = Order.objects.create(**validated_data)

        # Crée les OrderItems associés
        for article_data in articles_data:
            OrderItem.objects.create(order=order, **article_data)

        return order

