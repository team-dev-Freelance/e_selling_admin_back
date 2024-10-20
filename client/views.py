from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from permissions import IsOwnerOrReadOnly
from rule.models import Role
from utilisateur.models import Client
# from .models import Client
from .serializers import ClientSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

import logging

# Configurez un logger pour enregistrer les erreurs
logger = logging.getLogger(__name__)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    # def get_permissions(self):
    #     if self.action in ['retrieve', 'update', 'deactivate_client', 'partial_update']:
    #         self.permission_classes = [IsOwnerOrReadOnly]
    #     return super().get_permissions()

    # Liste des clients: client/
    def list(self, request):
        clients = Client.objects.all().distinct()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ClientSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            phone = serializer.validated_data['phone']
            password = serializer.validated_data['password']

            try:
                role, created = Role.objects.get_or_create(role='CLIENT')

                client = Client(
                    username=username,
                    email=email,
                    phone=phone,
                    rule=role
                )
                client.set_password(password)
                client.save()

                return Response(ClientSerializer(client).data, status=status.HTTP_201_CREATED)

            except ValidationError as e:
                logger.error(f"Erreur de validation : {str(e)}")  # Enregistrer l'erreur de validation
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                # Enregistrer l'erreur générale pour comprendre le problème
                logger.error(f"Erreur inattendue : {str(e)}")
                return Response({"detail": f"Une erreur s'est produite : {str(e)}"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Un client par son id: client/profileClient/
    @action(detail=False, methods=['get'], url_path='profileClient')
    def profile(self, request):
        try:
            client = Client.objects.get(pk=request.user.id)
        except Client.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    # Mise a jour d'un client: client/{id}/
    def update(self, request, pk=None):
        try:
            client = Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Mise a jour partielle d'un client: client/{id}/ avec PATCH
    def partial_update(self, request, pk=None):
        try:
            client = Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ClientSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Liste des clients actives: client/list_active_clients/
    @action(detail=False, methods=['get'])
    def list_active_clients(self, request):
        active_clients = Client.objects.filter(active=True).distinct()
        serializer = self.get_serializer(active_clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Desactiver un client: client/deactivate/
    @action(detail=False, methods=['post'], url_path='deactivate')
    def deactivate_client(self, request):
        client_id = request.data.get('id')
        client = get_object_or_404(Client, id=client_id)
        if client.active:
            client.active = False
            client.save()
            return Response({'status': 'client deactivated'}, status=status.HTTP_200_OK)
        else:
            client.active = True
            client.save()
            return Response({'status': 'client activated'}, status=status.HTTP_200_OK)

