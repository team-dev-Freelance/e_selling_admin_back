from rest_framework import viewsets
from .models import Privilegies
from .serializers import PrivilegiesSerializer
from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class PrivilegiesViewSet(viewsets.ModelViewSet):
    queryset = Privilegies.objects.all()
    serializer_class = PrivilegiesSerializer

