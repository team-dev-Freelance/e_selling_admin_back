from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated  # Import du permission class

from article.models import Article
from utilisateur.models import Client
from .models import Cart, CartItem
from .serializers import CartSerializer


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        client = getattr(request.user, 'client', None)
        if not client:
            return Response({'error': 'Client non trouvé pour cet utilisateur.'}, status=status.HTTP_404_NOT_FOUND)

        cart, created = Cart.objects.get_or_create(client=client)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        client_id = request.user.client.id
        article_ids = request.data.get('articleIds', [])
        quantities = request.data.get('quantities', [])

        if len(article_ids) != len(quantities):
            return Response({'error': 'Les articles et les quantités ne correspondent pas.'}, status=status.HTTP_400_BAD_REQUEST)

        cart, created = Cart.objects.get_or_create(client_id=client_id)

        for article_id, quantity in zip(article_ids, quantities):
            try:
                article = Article.objects.get(id=article_id)
                cart_item, item_created = CartItem.objects.get_or_create(cart=cart, article=article)
                cart_item.quantity = quantity
                cart_item.save()
            except Article.DoesNotExist:
                return Response({'error': f'Article {article_id} non trouvé.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def delete(self, request):
        client_id = request.user.client.id
        item_id = request.data.get('item_id')

        try:
            cart_item = CartItem.objects.get(id=item_id, cart__client_id=client_id)
            cart_item.delete()
            cart = Cart.objects.get(client_id=client_id)
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        except CartItem.DoesNotExist:
            return Response({'error': 'L\'élément du panier est introuvable'}, status=status.HTTP_404_NOT_FOUND)

