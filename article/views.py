from rest_framework import viewsets

from categorie.models import Categorie
# from member.models import Member
from permissions import IsUser, IsMemberOrUser, IsAdmin, IsCreatorOrReadOnly, IsOwnerOrReadOnly
from .models import Article
from .serializers import ArticleSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    # def get_permissions(self):
    #     if self.action in ['create']:
    #         self.permission_classes = [IsMemberOrUser]
    #     elif self.action in ['partial_update', 'deactivate_art', 'list_articles_member', 'retrieve', 'update', 'list_articles_actifs_user']:
    #         self.permission_classes = [IsCreatorOrReadOnly]
    #     elif self.action in ['list']:
    #         self.permission_classes = [IsAdmin]
    #     elif self.action in ['list_active_articles']:
    #         self.permission_classes = [IsOwnerOrReadOnly]
    #     return super().get_permissions()

    # Liste des arcticles: article/
    def list(self, request):
        articles = Article.objects.all().distinct()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = self.request.user
            member = user.member

            categorie_id = request.data.get('category_id')
            try:
                category_instance = Categorie.objects.get(id=categorie_id)
            except Categorie.DoesNotExist:
                return Response({'detail': 'Category not found'}, status=status.HTTP_400_BAD_REQUEST)

            # Passer uniquement les données validées au serializer
            article = serializer.save(member=member, category=category_instance)
            return Response(ArticleSerializer(article).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save()

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

    # Desactiver un article: article/deactivate/
    @action(detail=False, methods=['post'], url_path='deactivate')
    def deactivate_art(self, request):
        article_id = request.data.get('id')
        article = get_object_or_404(Article, id=article_id)
        # article = self.get_object()
        if article.active:
            article.active = False
            article.save()
            return Response({'status': 'article deactivated'}, status=status.HTTP_200_OK)
        else:
            article.active = True
            article.save()
            return Response({'status': 'article activated'}, status=status.HTTP_200_OK)

    # Liste des articles publies par un utilisateur: article/list_articles/bymember/
    @action(detail=False, methods=['get'], url_path='list_articles/bymember')
    def list_articles_member(self, request):
        articles = Article.objects.filter(member_id=request.user.id).distinct()
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Liste des articles actifs publies par un utilisateur: article/list_actifs_articles/bymember/
    @action(detail=False, methods=['get'], url_path='list_actifs_articles/bymember')
    def list_articles_actifs_user(self, request):
        articles = Article.objects.filter(member_id=request.user.id, active=True).distinct()
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Liste des articles actifs pour une organisation et une categorie: article/{id}/articles_actifs/
    @action(detail=True, methods=['get'], url_path='articles_actifs')
    def list_active_articles_by_organisation_and_category(self, request, pk=None):
        try:
            # Récupérer l'article en utilisant le pk fourni dans l'URL
            article = Article.objects.get(pk=pk)

            # Récupérer le membre ayant publié cet article
            member = article.member

            # Récupérer l'organisation à laquelle appartient le membre
            organisation = member.organisation

            # Filtrer les articles actifs de cette organisation et cette catégorie
            articles = Article.objects.filter(member__organisation=organisation, category=article.category,
                                              active=True).distinct()

            # Vérifier si des articles sont trouvés
            if articles.exists():
                serializer = ArticleSerializer(articles, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"detail": "Aucun article actif trouvé pour cette organisation et cette catégorie."},
                    status=status.HTTP_404_NOT_FOUND)

        except Article.DoesNotExist:
            return Response({"detail": "Article non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"Une erreur s'est produite : {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        