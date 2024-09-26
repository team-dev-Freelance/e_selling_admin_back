from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from django.conf import settings

from .models import Order, OrderItem
from utilisateur.models import Member


class OrderViewSet(ViewSet):

    @action(detail=False, methods=['post'], url_path='passer_commande')
    def passer_commande(self, request):
        try:
            client = request.user  # L'utilisateur courant (le client qui passe la commande)
            panier = request.data.get('panier', [])  # Liste des éléments du panier passée en paramètre

            if not panier:
                return Response({"detail": "Le panier est vide."}, status=status.HTTP_400_BAD_REQUEST)

            # Créer la commande
            order = Order.objects.create(client=client, status='pending')

            # Ajouter les articles à la commande
            for item in panier:
                article_id = item.get('article_id')
                quantity = item.get('quantity', 1)
                OrderItem.objects.create(order=order, article_id=article_id, quantity=quantity)

            # Trouver l'organisation associée aux articles du panier (tous les articles sont censés appartenir à la même organisation)
            article_organisation = OrderItem.objects.filter(order=order).first().article.member.organisation

            # Trouver l'admin de l'organisation (membre avec le rôle 'user')
            admin_organisation = Member.objects.filter(organisation=article_organisation, role__rule='user').first()

            if admin_organisation:
                # Préparer l'email à envoyer
                subject = "Nouvelle commande passée"
                message = f"""
                Bonjour {admin_organisation.username},

                Une nouvelle commande a été passée pour l'organisation {article_organisation.name}.

                Client : {client.username}
                Numéro de téléphone : {client.phone}

                Articles commandés :
                """

                for item in panier:
                    article = item.get('article')
                    quantity = item.get('quantity', 1)
                    message += f"- {article['label']} (Quantité : {quantity})\n"

                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [admin_organisation.email],
                    fail_silently=False,
                )
                return Response({"detail": "Commande passée et notification envoyée."}, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Admin de l'organisation non trouvé."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"detail": f"Erreur : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
