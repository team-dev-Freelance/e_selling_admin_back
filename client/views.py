from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from rest_framework import viewsets

from e_selling_admin_back import settings
from rule.models import Role
from utilisateur.models import Client

# from .models import Client
from .serializers import ClientSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
# from .models import Utilisateur,Client
# from .serializers import UtilisateurSerializer

@require_http_methods(["GET"])
def client_list(request):
    users = Client.objects.all()
    # Sérialiser les catégories
    serializer = ClientSerializer(users, many=True)  
    return JsonResponse({
        'response': serializer.data  
    }, status=200)  # 200 OK

@require_http_methods(["GET"])
def get_client_by_id(request, client_id):
    # Récupérer le membre ou retourner une erreur 404 s'il n'existe pas
    client = get_object_or_404(Client, id=client_id)

    # Sérialiser le membre
    serializer = ClientSerializer(client)  

    # Retourner la réponse JSON
    return JsonResponse({
        'status': 'success',
        'client': serializer.data  
    }, status=200)  # 200 OK

@csrf_exempt
@require_http_methods(["POST"])
def create_client(request):
    # Vérifier si le corps de la requête contient des données
    if request.body:
        try:
            # Charger les données JSON du corps de la requête
            data = json.loads(request.body)

            # Obtenir les informations de l'utilisateur
            email = data.get("email")
            nom = data.get("nom")
            phone = data.get("phone")
            password = data.get("password")
            # password = get_random_string(length=8)

            # Vérifier la présence des données obligatoires
            if not all([email, nom, password]):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Tous les champs requis (email, nom, password) doivent être fournis.'
                }, status=400)  # 400 Bad Request

            # Créer ou obtenir le rôle ADMIN
            role, created = Role.objects.get_or_create(role='CLIENT')

            # Créer l'utilisateur
            utilisateur = Client.objects.create_user(
                email=email,
                password=password, 
                nom=nom,
                phone=phone,
                rule=role
            )
            # send_welcome_email(utilisateur, password)
            return JsonResponse({
                'status': 'success',
                'message': 'Client créé avec succès!',
                'user_email': utilisateur.email
            }, status=201)  # 201 Created

        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Données JSON invalides.'
            }, status=400)  # 400 Bad Request
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)  # 500 Internal Server Error

    return JsonResponse({
        'status': 'error',
        'message': 'Aucune donnée fournie.'
    }, status=400)  # 400 Bad Request
@csrf_exempt
def delete_all_clients(request):
    if request.method == 'POST':  # Assurez-vous que la méthode est POST
        try:
            # Supprime tous les objets de la table Client
            count, _ = Client.objects.all().delete()  # Delete renvoie le nombre d'objets supprimés

            return JsonResponse({
                'status': 'success',
                'message': f'Tous les membres ont été supprimés. Nombre de membres supprimés: {count}'
            }, status=200)  # 200 OK

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)  # Renvoie l'erreur si quelque chose ne va pas
            }, status=500)  # 500 Internal Server Error

    return JsonResponse({
        'status': 'error',
        'message': 'Méthode non autorisée. Utilisez POST.'
    }, status=405)  # 405 Method Not Allowed

def send_welcome_email( Client, password):
    subject = 'Bienvenue dans GIC Connect'
    message = f"""
    Bonjour {Client.nom},

    Votre compte a été créé avec succès. Voici vos informations de connexion :

    - Nom d'utilisateur : {Client.email}
    - Mot de passe : {password}

    Merci de nous avoir rejoints !

    Cordialement,
    L'équipe GIC Connect
    """
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [Client.email]

    send_mail(subject, message, from_email, recipient_list)