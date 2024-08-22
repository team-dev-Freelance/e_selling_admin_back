from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated  # Import du permission class

from article.models import Article
from .models import Cart, CartItem
from .serializers import CartSerializer


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Vérification que l'utilisateur est authentifié
        if not request.user.is_authenticated:
            return Response({'error': 'Vous devez être connecté pour voir le panier.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        # Assurez-vous que le client est bien associé à l'utilisateur
        client = getattr(request.user, 'client', None)
        if not client:
            return Response({'error': 'Client non trouvé pour cet utilisateur.'}, status=status.HTTP_404_NOT_FOUND)

        cart, created = Cart.objects.get_or_create(client=client)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Vous devez être connecté pour ajouter des articles au panier.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        article_id = request.data.get('article_id')
        quantity = request.data.get('quantity', 1)
        client = getattr(request.user, 'client', None)
        if not client:
            return Response({'error': 'Client non trouvé pour cet utilisateur.'}, status=status.HTTP_404_NOT_FOUND)

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
        if not request.user.is_authenticated:
            return Response({'error': 'Vous devez être connecté pour supprimer des articles du panier.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        client = getattr(request.user, 'client', None)
        if not client:
            return Response({'error': 'Client non trouvé pour cet utilisateur.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            cart_item = CartItem.objects.get(id=item_id)
            cart_item.delete()
        except CartItem.DoesNotExist:
            return Response({'error': 'L\'élément du panier est introuvable'}, status=status.HTTP_404_NOT_FOUND)

        cart = Cart.objects.get(client=client)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
