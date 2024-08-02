from rest_framework import viewsets

from member.models import Member
from .models import Article
from .serializers import ArticleSerializer
from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    # Liste des arcticles: article/
    def list(self, request):
        articles = Article.objects.all().distinct()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    # Creation d'un article: article/
    def create(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Un article par son id: article/{id}/
    def retrieve(self, request, pk=None):
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    # Mise a jour d'un article: article/{id}/
    def update(self, request, pk=None):
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Mise a jour partielle d'un article: article/{id}/ avec PATCH
    def partial_update(self, request, pk=None):
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Liste des articles actives: article/list_active_articles/
    @action(detail=False, methods=['get'])
    def list_active_articles(self, request):
        active_articles = Article.objects.filter(active=True).distinct()
        serializer = self.get_serializer(active_articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Liste des articles publies par un utilisateur: article/list_articles/member/{id}/
    @action(detail=False, methods=['get'], url_path='list_articles/member/(?P<member_id>[^/.]+)')
    def list_articles(self, request, member_id=None):
        articles = Article.objects.filter(member_id=member_id).distinct()
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Liste des articles actifs publies par un utilisateur: article/list_actifs_articles/member/{id}/
    @action(detail=False, methods=['get'], url_path='list_actifs_articles/member/(?P<member_id>[^/.]+)')
    def list_articles(self, request, member_id=None):
        articles = Article.objects.filter(member_id=member_id, active=True).distinct()
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Desactiver un article: article/{id}/deactivate/
    @action(detail=True, methods=['post'], url_path='deactivate')
    def deactivate_art(self, request, pk=None):
        article = self.get_object()
        if article.active:
            article.active = False
            article.save()
            return Response({'status': 'article deactivated'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'article already deactivated'}, status=status.HTTP_400_BAD_REQUEST)

