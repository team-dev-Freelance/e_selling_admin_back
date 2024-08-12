# serializers.py

from rest_framework import serializers
from .models import Cart, CartItem


class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['article', 'quantity']


class CartWithItemsSerializer(serializers.ModelSerializer):
    cart_items = CartItemCreateSerializer(source='cartitem_set',
        many=True)  # Retirez 'source' si vous n'utilisez pas une relation inversée personnalisée
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['cart_items', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()

    def create(self, validated_data):
        cart_items_data = validated_data.pop('cartitem_set', [])
        if not cart_items_data:
            raise serializers.ValidationError("No cart items data found in request.")

        request = self.context.get('request')
        client = request.user.client

        # Création d'un nouveau panier
        cart = Cart.objects.create(client=client)

        for item_data in cart_items_data:
            CartItem.objects.create(cart=cart, **item_data)

        return cart
