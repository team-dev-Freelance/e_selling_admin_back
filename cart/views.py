# views.py

from rest_framework.response import Response
from rest_framework.views import APIView

from article.models import Article
from .models import Cart, CartItem
from .serializers import CartSerializer


class CartView(APIView):
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        client_id = request.data.get('client_id')
        quantity = request.data.get('quantity', 1)

        article = Article.objects.get(id=client_id)
        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, article=article)
        if item_created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def delete(self, request, item_id):
        cart_item = CartItem.objects.get(id=item_id)
        cart_item.delete()

        cart = Cart.objects.get(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

