# serializers.py

from rest_framework import serializers

from article.serializers import ArticleSerializer
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    article = ArticleSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'article', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'client', 'created_at', 'items', 'total_price']

    def get_items(self, obj):
        cart_items = CartItem.objects.filter(cart=obj)
        return CartItemSerializer(cart_items, many=True).data

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
