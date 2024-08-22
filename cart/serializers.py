# serializers.py

from rest_framework import serializers

from article.serializers import ArticleSerializer
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    article = ArticleSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'article', 'quantity', 'get_total_price']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'client', 'created_at', 'items']

    def get_total_price(self, obj):
        return obj.get_total_price()

    # def create(self, validated_data):
    #     cart_items_data = validated_data.pop('cartitem_set', [])
    #     if not cart_items_data:
    #         raise serializers.ValidationError("Aucune donnée d'articles de panier trouvée dans la requête.")
    #
    #     request = self.context.get('request')
    #     client = request.user.client
    #
    #     # Création d'un nouveau panier
    #     cart = Cart.objects.create(client=client)
    #
    #     for item_data in cart_items_data:
    #         CartItem.objects.create(cart=cart, **item_data)
    #
    #     return cart
