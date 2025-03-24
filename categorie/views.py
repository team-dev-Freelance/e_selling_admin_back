
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from article.models import Article
from article.serializers import ArticleSerializer
from permissions import IsMemberOrUser, IsCreatorOrReadOnly
from .models import Categorie
from .serializers import CategorieSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer

    # Liste des categories: categorie/
    def list(self, request):
        categories = Categorie.objects.all()
        serializer = CategorieSerializer(categories, many=True)
        return Response(serializer.data)

    # Creation d'une categorie: categorie/
    def create(self, request):
        serializer = CategorieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # Une categorie par son id: categorie/{id}/
    def retrieve(self, request, pk=None):
        try:
            categorie = Categorie.objects.get(pk=pk)
        except Categorie.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CategorieSerializer(categorie)
        return Response(serializer.data)

    # Mise a jour d'une categorie: categorie/{id}/
    def update(self, request, pk=None):
        try:
            categorie = Categorie.objects.get(pk=pk)
        except Categorie.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CategorieSerializer(categorie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

 