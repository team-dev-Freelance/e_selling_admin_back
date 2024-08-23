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

        client_id = request.data.get('clientId')
        article_id = request.data.get('articleId')
        quantity = request.data.get('quantity', 1)

        if not client_id or not article_id or quantity is None:
            return Response({'error': 'Données manquantes.'}, status=status.HTTP_400_BAD_REQUEST)

        # Assurez-vous que les types de données sont corrects
        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            return Response({'error': 'Client non trouvé.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return Response({'error': 'Article non trouvé.'}, status=status.HTTP_404_NOT_FOUND)

        cart, created = Cart.objects.get_or_create(client=client)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, article=article)

        if item_created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def delete(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Vous devez être connecté pour supprimer des articles du panier.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        client_id = request.data.get('client_id')
        item_id = request.data.get('item_id')

        if not client_id:
            return Response({'error': 'Client ID est requis.'}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.client.id != client_id:
            return Response({'error': 'Client ID non autorisé.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            cart_item = CartItem.objects.get(id=item_id)
            cart_item.delete()
        except CartItem.DoesNotExist:
            return Response({'error': 'L\'élément du panier est introuvable'}, status=status.HTTP_404_NOT_FOUND)

        cart = Cart.objects.get(client=client_id)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
