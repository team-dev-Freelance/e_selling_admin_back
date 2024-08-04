from rest_framework import viewsets

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

    # @action(detail=False, methods=['post'], url_path='add')
    # def ajouter(self, request):
    #     serializer = RoleSerializer(data=request.data)
    #     if serializer.is_valid():
    #         role = serializer.save()
    #         add_privilege = Privilegies.objects.get_or_create(privilege=Privilege.ADD)[0]
    #         find_privileges = Privilegies.objects.get_or_create(privilege=Privilege.FIND)[0]
    #         all_privilege = Privilegies.objects.get_or_create(privilege=Privilege.ALL)[0]
    #
    #         if role in [Rule.ADMIN, Rule.MEMBER]:
    #
    #             role.privileges.add(add_privilege, find_privileges)
    #             if role == Rule.USER:
    #                 role.privileges.add(all_privilege)
    #
    #         role.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

