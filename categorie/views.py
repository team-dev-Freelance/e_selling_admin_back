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

    # def get_permissions(self):
    #     if self.action in ['create', 'list', 'partial_update', 'retrieve', 'update', 'list_active_categories', 'deactivate_cat']:
    #         self.permission_classes = [IsMemberOrUser]
    #     elif self.action in ['list_articles']:
    #         self.permission_classes = [IsCreatorOrReadOnly]
    #     return super().get_permissions()

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

    # Mise a jour partielle d'une categorie: categorie/{id}/ avec PATCH
    def partial_update(self, request, pk=None):
        try:
            categorie = Categorie.objects.get(pk=pk)
        except Categorie.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CategorieSerializer(categorie, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Liste des categories actives: categorie/list_active_categories/
    @action(detail=False, methods=['get'])
    def list_active_categories(self, request):
        active_categories = Categorie.objects.filter(active=True).distinct()
        serializer = self.get_serializer(active_categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Desactiver une categorie: categorie/deactiver/
    @action(detail=False, methods=['post'], url_path='deactivate')
    def deactivate_cat(self, request):
        categorie_id = request.data.get('id')
        categorie = get_object_or_404(Categorie, id=categorie_id)
        if categorie.active:
            categorie.active = False
            categorie.save()
            return Response({'status': 'categorie deactivated'}, status=status.HTTP_200_OK)
        else:
            categorie.active = True
            categorie.save()
            return Response({'status': 'categorie activated'}, status=status.HTTP_200_OK)

    # Liste des articles d'une categorie: categorie/{id}/list_articles/
    @action(detail=True, methods=['get'])
    def list_articles(self, request, pk=None):
        try:
            categorie = Categorie.objects.get(pk=pk)
        except Categorie.DoesNotExist:
            return Response({"error": "Categorie not found."}, status=404)

        articles = Article.objects.filter(category=categorie.id).distinct()  # Obtenir tous les articles de la categorie
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    # Liste des articles actifs d'une categorie: categorie/{id}/list_articles_actif/
    @action(detail=True, methods=['get'])
    def list_articles_actif(self, request, pk=None):
        try:
            categorie = Categorie.objects.get(pk=pk)
        except Categorie.DoesNotExist:
            return Response({"error": "Categorie not found."}, status=404)

        articles = Article.objects.filter(active=True, category=categorie.id).distinct()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

