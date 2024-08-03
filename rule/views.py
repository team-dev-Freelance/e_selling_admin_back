from rest_framework import viewsets
from .models import Role
from .serializers import RoleSerializer
from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

