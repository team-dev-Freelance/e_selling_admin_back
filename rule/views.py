from rest_framework import viewsets

from permissions import IsAdmin, IsAdminOrUser, IsUser
from privilegies.models import Privilegies, Privilege
from .models import Role, Rule
from .serializers import RoleSerializer
from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    # def get_permissions(self):
    #     if self.action in ['list', 'create', 'partial_update', 'retrieve', 'update']:
    #         self.permission_classes = [IsAdmin]
    #     elif self.action in ['list_except_admin']:
    #         self.permission_classes = [IsUser]
    #     elif self.action in ['partial_update', 'update']:
    #         self.permission_classes = [IsAdminOrUser]
    #     return super().get_permissions()

    # Liste des rôles à l'exception de l'admin: rule/except_admin/
    @action(detail=False, methods=['get'], url_path='except_admin')
    def list_except_admin(self, request):
        try:
            # Récupère les rôles actifs en excluant les admins
            roles = Role.objects.filter(active=True).exclude(role=Rule.ADMIN)
            serializer = self.get_serializer(roles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Role.DoesNotExist:
            # Si aucune donnée n'est trouvée
            return Response({'error': 'Aucun rôle trouvé.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Gestion des erreurs inattendues
            return Response({'error': f'Erreur inattendue: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


