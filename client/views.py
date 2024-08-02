from rest_framework import viewsets
from .models import Client
from .serializers import ClientSerializer
from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    # Liste des clients: client/
    def list(self, request):
        clients = Client.objects.all().distinct()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    # Creation d'un client: client/
    def create(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Un client par son id: client/{id}/
    def retrieve(self, request, pk=None):
        try:
            client = Client.objects.get(pk=pk)
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

    # Desactiver un client: client/{id}/deactivate/
    @action(detail=True, methods=['post'], url_path='deactivate')
    def deactivate_client(self, request, pk=None):
        client = self.get_object()
        if client.active:
            client.active = False
            client.save()
            return Response({'status': 'client deactivated'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'client already deactivated'}, status=status.HTTP_400_BAD_REQUEST)

