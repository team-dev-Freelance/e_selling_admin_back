from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Cart
from article.models import Article
from utilisateur.models import Client
from django.shortcuts import  get_object_or_404


@api_view(['POST'])
def add_to_cart(request):
    try:
        # Récupérer les données envoyées par l'utilisateur
        article_id = request.data.get('article')
        client_id = request.data.get('client_id')
        quantity = request.data.get('quantity', 1)  # Valeur par défaut: 1

        # Vérifier que l'article existe
        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return Response({"message": "Article non trouvé."}, status=status.HTTP_404_NOT_FOUND)

        # Vérifier si le client existe
        client  = get_object_or_404(Client, id= client_id)

        # Vérifier si l'article est déjà dans le panier
        cart_item, created = Cart.objects.get_or_create(client=client, article=article)

        if not created:
            # Si l'article existe déjà, on met à jour la quantité
            cart_item.quantity += int(quantity)
            cart_item.save()
        else:
            # Sinon, on ajoute un nouvel article avec la quantité demandée
            cart_item.quantity = int(quantity)
            cart_item.save()

        return Response({
            "message": "Article ajouté au panier avec succès.",
            "cart_item": {
                "article": article.label,
                "quantity": cart_item.quantity,
                "subtotal": article.price * cart_item.quantity
            }
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": f"Erreur : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
