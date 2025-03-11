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

    # Liste des articles: article/
    def list(self, request):
        try:
            articles = Article.objects.all().distinct()
            serializer = ArticleSerializer(articles, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"detail": f"Erreur lors de la récupération des articles : {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Création d'un article: article/
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                user = self.request.user
                member = user.member

                categorie_id = request.data.get('category_id')
                category_instance = Categorie.objects.get(id=categorie_id)
                logo = request.FILES.get('logo', None)
                article = serializer.save(member=member, category=category_instance, logo=logo)
                return Response(ArticleSerializer(article).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Categorie.DoesNotExist:
            return Response({"detail": "Catégorie non trouvée."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"Erreur lors de la création de l'article : {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Un article par son id: article/{id}/
    def retrieve(self, request, pk=None):
        try:
            article = Article.objects.get(pk=pk)
            serializer = ArticleSerializer(article)
            return Response(serializer.data)
        except Article.DoesNotExist:
            return Response({"detail": "Article non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"Erreur lors de la récupération de l'article : {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Mise à jour d'un article: article/{id}/
    def update(self, request, pk=None):
        try:
            article = Article.objects.get(pk=pk)
            serializer = ArticleSerializer(article, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Article.DoesNotExist:
            return Response({"detail": "Article non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"Erreur lors de la mise à jour de l'article : {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Mise à jour partielle d'un article: article/{id}/ avec PATCH
    def partial_update(self, request, pk=None):
        try:
            article = Article.objects.get(pk=pk)
            serializer = ArticleSerializer(article, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Article.DoesNotExist:
            return Response({"detail": "Article non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"Erreur lors de la mise à jour partielle de l'article : {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Liste des articles actifs: article/list_active_articles/
    @action(detail=False, methods=['get'])
    def list_active_articles(self, request):
        try:
            active_articles = Article.objects.filter(active=True).distinct()
            serializer = self.get_serializer(active_articles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": f"Erreur lors de la récupération des articles actifs : {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Désactiver un article: article/deactivate/
    @action(detail=False, methods=['post'], url_path='deactivate')
    def deactivate_art(self, request):
        try:
            article_id = request.data.get('id')
            article = get_object_or_404(Article, id=article_id)
            article.active = not article.active
            article.save()
            return Response({'status': 'article updated'}, status=status.HTTP_200_OK)
        except Article.DoesNotExist:
            return Response({"detail": "Article non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"Erreur lors de la désactivation de l'article : {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Liste des articles publiés par un membre: article/list_articles/bymember/
    @action(detail=False, methods=['get'], url_path='list_articles/bymember')
    def list_articles_member(self, request):
        try:
            articles = Article.objects.filter(member_id=request.user.id).distinct()
            serializer = self.get_serializer(articles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": f"Erreur lors de la récupération des articles par membre : {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Liste des articles actifs publiés par un membre: article/list_actifs_articles/bymember/
    @action(detail=False, methods=['get'], url_path='list_actifs_articles/bymember')
    def list_articles_actifs_user(self, request):
        try:
            articles = Article.objects.filter(member_id=request.user.id, active=True).distinct()
            serializer = self.get_serializer(articles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": f"Erreur lors de la récupération des articles actifs par membre : {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Liste des articles actifs pour une organisation et une catégorie: article/{id}/articles_actifs/
    @action(detail=True, methods=['get'], url_path='articles_actifs')
    def list_active_articles_by_organisation_and_category(self, request, pk=None):
        try:
            article = Article.objects.get(pk=pk)
            organisation = article.member.organisation
            articles = Article.objects.filter(member__organisation=organisation, category=article.category,
                                              active=True).distinct()
            if articles.exists():
                serializer = ArticleSerializer(articles, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"detail": "Aucun article actif trouvé pour cette organisation et cette catégorie."},
                            status=status.HTTP_404_NOT_FOUND)
        except Article.DoesNotExist:
            return Response({"detail": "Article non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"Erreur lors de la récupération des articles actifs : {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

