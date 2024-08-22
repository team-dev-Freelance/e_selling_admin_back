# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from article.models import Article
from .models import Cart, CartItem
from .serializers import CartSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cart, CartItem
from article.models import Article
from .serializers import CartSerializer


class CartView(APIView):
    def get(self, request):
        # Assurez-vous que le client est bien associé à l'utilisateur
        client = request.user.client
        cart, created = Cart.objects.get_or_create(client=client)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        article_id = request.data.get('article_id')
        quantity = request.data.get('quantity', 1)
        client = request.user.client  # Utilisation du client pour la recherche du panier

        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return Response({'error': 'L\'article est inexistent'}, status=status.HTTP_404_NOT_FOUND)

        cart, created = Cart.objects.get_or_create(client=client)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, article=article)

        if item_created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def delete(self, request, item_id):
        client = request.user.client  # Utilisation du client pour la recherche du panier
        try:
            cart_item = CartItem.objects.get(id=item_id)
            cart_item.delete()
        except CartItem.DoesNotExist:
            return Response({'error': 'L\'élément du panier est introuvable'}, status=status.HTTP_404_NOT_FOUND)

        # Met à jour le panier après la suppression de l'élément
        cart = Cart.objects.get(client=client)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
