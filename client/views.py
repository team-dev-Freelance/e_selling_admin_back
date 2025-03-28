from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from rest_framework import viewsets
from e_selling_admin_back import settings
from rule.models import Role
from utilisateur.models import Client
from .serializers import ClientSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import gettext as _
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import logging

logger = logging.getLogger(__name__)
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    # Customer's list client/
    def list(self, request):
        client = Client.objects.all()
        serializer = ClientSerializer(client, many=True)
        return Response(serializer.data)

    # Create customer client/
    def create(self, request):
        email = request.data.get('email')
        nom = request.data.get('nom')
        phone = request.data.get('phone')
        password = request.data.get('password')

        # Validate inputs
        if not email or not nom or not phone or not password:
            return Response(
                {'message': _('Tous les champs sont obligatoires!'), 'status': 'error'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if Client.objects.filter(email=email).exists():
            return Response(
                {'message': _('L\'utilisateur existe déjà.'), 'status': 'error'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Password strength validation (example: minimum length)
        if len(password) < 4:
            return Response(
                {'message': _('Le mot de passe doit contenir au moins 4 caractères.'), 'status': 'error'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create or get the role
        role, created = Role.objects.get_or_create(role='CLIENT')

        try:
            # Create the user
            utilisateur = Client.objects.create_user(
                email=email,
                password=password,
                nom=nom,
                phone=phone,
                rule=role
            )
            return Response(
                {
                    'status': 'success',
                    'message': _('Client créé avec succès!'),
                    'user_email': utilisateur.email
                },
                status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            return Response(
                {'message': _('Erreur de validation. Veuillez vérifier vos données.'), 'status': 'error'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Erreur lors de la création de l'utilisateur: {str(e)}")
            return Response(
                {'message': _('Une erreur est survenue. Veuillez réessayer plus tard.'), 'status': 'error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # Get customer by id: client/{id}/
    def retrieve(self, request, pk=None):
        try:
            client = Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ClientSerializer(client)
        return Response(serializer.data)
    
