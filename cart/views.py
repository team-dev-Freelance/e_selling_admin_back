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

        if not cart_items:
            return Response({'error': 'Aucun article à ajouter.'}, status=status.HTTP_400_BAD_REQUEST)

        # Obtenir le premier article des nouveaux articles
        first_new_item = cart_items[0]
        new_article_id = first_new_item.get('article')
        new_article_quantity = first_new_item.get('quantity')

        if not new_article_id or not new_article_quantity:
            return Response({'error': 'Données d\'article ou de quantité manquantes pour le premier article.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            new_article = Article.objects.get(id=new_article_id)
            new_article_organisation = new_article.member.organisation

            # Vérifier s'il existe un panier pour le client
            try:
                cart = Cart.objects.get(client_id=client_id)
                # Récupérer l'organisation du premier article dans le panier existant
                existing_cart_item = cart.cartitem_set.first()
                existing_organisation = (
                    existing_cart_item.article.member.organisation if existing_cart_item else None
                )

                # Si les organisations ne correspondent pas, réinitialiser le panier
                if existing_organisation and existing_organisation != new_article_organisation:
                    cart.cartitem_set.all().delete()  # Vider les articles existants
                    cart.delete()  # Supprimer le panier existant
                    cart = Cart.objects.create(client_id=client_id)  # Créer un nouveau panier

            except Cart.DoesNotExist:
                # Créer un nouveau panier si le client n'en a pas encore
                cart = Cart.objects.create(client_id=client_id)

            # Ajouter tous les articles au panier (après vérification)
            for item in cart_items:
                article_id = item.get('article')
                quantity = item.get('quantity')
                if not article_id or not quantity:
                    return Response({'error': 'Données d\'article ou de quantité manquantes.'},
                                    status=status.HTTP_400_BAD_REQUEST)

                try:
                    article = Article.objects.get(id=article_id)
                    cart_item, _ = CartItem.objects.get_or_create(cart=cart, article=article)
                    cart_item.quantity = quantity
                    cart_item.save()
                except Article.DoesNotExist:
                    return Response({'error': f'Article {article_id} non trouvé.'}, status=status.HTTP_404_NOT_FOUND)

        except Article.DoesNotExist:
            return Response({'error': f'Article {new_article_id} non trouvé.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def delete(self, request, item_id):
        client_id = request.user.client.id

        try:
            cart_item = CartItem.objects.get(id=item_id, cart__client_id=client_id)
            cart_item.delete()
            cart = Cart.objects.get(client_id=client_id)
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        except CartItem.DoesNotExist:
            return Response({'error': 'L\'élément du panier est introuvable'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Log l'erreur pour le débogage
            print(f"Erreur lors de la suppression de l'élément du panier : {e}")
            return Response({'error': 'Erreur lors de la suppression de l\'élément'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


