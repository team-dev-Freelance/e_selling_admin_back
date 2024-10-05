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
        cart_items = request.data.get('cart_items', [])

        try:
            # Récupérer le panier existant du client (s'il existe)
            cart = Cart.objects.get(client_id=client_id)

            # Récupérer les articles existants dans le panier
            existing_articles = cart.cartitem_set.values_list('article__member__organisation', flat=True)
            existing_organisation = existing_articles[0] if existing_articles else None

            for item in cart_items:
                article_id = item.get('article')
                quantity = item.get('quantity')
                if not article_id or not quantity:
                    return Response({'error': 'Données d\'article ou de quantité manquantes.'},
                                    status=status.HTTP_400_BAD_REQUEST)

                try:
                    article = Article.objects.get(id=article_id)

                    # Vérifier l'organisation de l'article
                    article_organisation = article.member.organisation

                    if existing_organisation and existing_organisation != article_organisation:
                        # Si l'organisation diffère, vider le panier et créer un nouveau panier
                        cart.cartitem_set.all().delete()  # Vider le panier existant
                        cart.delete()  # Supprimer le panier existant
                        cart = Cart.objects.create(client_id=client_id)  # Créer un nouveau panier
                        existing_organisation = article_organisation  # Mettre à jour l'organisation

                    # Ajouter l'article au panier
                    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, article=article)
                    cart_item.quantity = quantity
                    cart_item.save()

                except Article.DoesNotExist:
                    return Response({'error': f'Article {article_id} non trouvé.'}, status=status.HTTP_404_NOT_FOUND)

        except Cart.DoesNotExist:
            # Créer un nouveau panier si le client n'en a pas encore
            cart = Cart.objects.create(client_id=client_id)

            for item in cart_items:
                article_id = item.get('article')
                quantity = item.get('quantity')
                if not article_id or not quantity:
                    return Response({'error': 'Données d\'article ou de quantité manquantes.'},
                                    status=status.HTTP_400_BAD_REQUEST)

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

