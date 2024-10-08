from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings

from cart.models import Cart
from .models import Order, OrderItem
from utilisateur.models import Member, Client


class PasserCommandeView(APIView):
    def post(self, request):
        try:
            client = Client.objects.get(username=request.user.username)
            panier = Cart.objects.get(client=client)  # Récupérer le panier du client

            if panier.articles.count() == 0:  # Vérifie si le panier est vide
                return Response({"detail": "Le panier est vide."}, status=status.HTTP_400_BAD_REQUEST)

            # Créer la commande
            order = Order.objects.create(client=client, status='pending')

            # Initialiser le prix total
            total_price = 0

            # Ajouter les articles à la commande et calculer le prix total
            for item in panier.cartitem_set.all():  # Parcourir les articles du panier
                OrderItem.objects.create(order=order, article=item.article, quantity=item.quantity)
                total_price += item.article.price * item.quantity  # Calculez le prix total

            # Trouver l'organisation associée aux articles du panier
            article_organisation = panier.cartitem_set.first().article.member.organisation

            # Trouver l'admin de l'organisation (membre avec le rôle 'ADMIN')
            admin_organisation = Member.objects.filter(
                organisation=article_organisation,
                rule__role='USER'  # Vérifiez que cela correspond bien au rôle que vous avez défini
            ).first()

            if admin_organisation:
                # Préparer l'email à envoyer à l'admin de l'organisation
                subject_admin = "Nouvelle commande passée"
                message_admin = f"""
                Bonjour {admin_organisation.username},

                Une nouvelle commande a été passée pour l'organisation {article_organisation.label}.

                Client : {client.username}
                Numéro de téléphone : {client.phone}
                Prix total : {total_price} Fcfa

                Articles commandés :
                """

                for item in panier.cartitem_set.all():
                    message_admin += f"- {item.article.label} (Quantité : {item.quantity})\n"

                send_mail(
                    subject_admin,
                    message_admin,
                    settings.DEFAULT_FROM_EMAIL,
                    [admin_organisation.email],
                    fail_silently=False,
                )

                # Préparer l'email à envoyer au client
                subject_client = "Confirmation de votre commande"
                message_client = f"""
                Bonjour {client.username},

                Merci pour votre commande ! Voici un récapitulatif :

                Prix total : {total_price} Fcfa
                Articles commandés :
                """

                for item in panier.cartitem_set.all():
                    message_client += f"- {item.article.label} (Quantité : {item.quantity})\n"

                send_mail(
                    subject_client,
                    message_client,
                    settings.DEFAULT_FROM_EMAIL,
                    [client.email],
                    fail_silently=False,
                )

                # Vider le panier en supprimant les articles
                panier.cartitem_set.all().delete()  # Supprime tous les articles du panier
                panier.delete()

                return Response({"detail": "Commande passée et notifications envoyées."},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Admin de l'organisation non trouvé."}, status=status.HTTP_404_NOT_FOUND)

        except Client.DoesNotExist:
            return Response({"detail": "Client non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        except Cart.DoesNotExist:
            return Response({"detail": "Panier non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"Erreur : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
