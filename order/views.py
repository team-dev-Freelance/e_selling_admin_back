from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from django.conf import settings

from cart.models import Cart
from .models import Order, OrderItem
from utilisateur.models import Member, Client


class PasserCommandeView(APIView):
    def post(self, request):
        try:
            client = Client.objects.get(user=request.user)
            panier = Cart.objects.get(client=client)  # Récupérer le panier du client

            if panier.articles.count() == 0:  # Vérifie si le panier est vide
                return Response({"detail": "Le panier est vide."}, status=status.HTTP_400_BAD_REQUEST)

            # Créer la commande
            order = Order.objects.create(client=client, status='pending')

            # Ajouter les articles à la commande
            for item in panier.cartitem_set.all():  # Parcourir les articles du panier
                OrderItem.objects.create(order=order, article=item.article, quantity=item.quantity)

            # Trouver l'organisation associée aux articles du panier
            article_organisation = panier.cartitem_set.first().article.member.organisation

            # Trouver l'admin de l'organisation (membre avec le rôle 'ADMIN')
            admin_organisation = Member.objects.filter(
                organisation=article_organisation,
                rule__role='ADMIN'  # Vérifiez que cela correspond bien au rôle que vous avez défini
            ).first()

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

                for item in panier.cartitem_set.all():
                    message += f"- {item.article.label} (Quantité : {item.quantity})\n"

                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [admin_organisation.email],
                    fail_silently=False,
                )

                # Vider le panier en supprimant les articles
                panier.cartitem_set.all().delete()  # Supprime tous les articles du panier

                return Response({"detail": "Commande passée et notification envoyée."}, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Admin de l'organisation non trouvé."}, status=status.HTTP_404_NOT_FOUND)

        except Cart.DoesNotExist:
            return Response({"detail": "Panier non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"Erreur : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
