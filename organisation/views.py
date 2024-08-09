from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from article.models import Article
from article.serializers import ArticleSerializer
from member.serializers import MemberSerializer
from permissions import IsAdmin, IsCreatorOrReadOnly, IsMemberOrUser, IsMemberOfOrganisation, \
    IsMemberUserOfOrganisation, IsUser, IsOwnerOrReadOnly
from .models import Organisation
from .serializers import OrganisationSerializer


class OrganisationViewSet(viewsets.ModelViewSet):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer

    def get_permissions(self):
        if self.action in ['partial_update', 'retrieve', 'update', 'list_members', 'deactivate_org', 'list_members_active']:
            self.permission_classes = [IsAdmin]
        elif self.action in ['list_articles', 'list_articles_actif', 'list_active_articles_by_category', 'list_articles_by_category']:
            self.permission_classes = [IsMemberOfOrganisation]
        elif self.action in ['list', 'create', 'retrieve', 'list_active_organisations']:
            self.permission_classes = [IsAdmin]
        elif self.action in ['list_active_organisation', 'list_active_articles_by_category', 'list_articles_by_category']:
            self.permission_classes = [IsUser]
        elif self.action in ['list_active_articles']:
            self.permission_classes = [IsOwnerOrReadOnly]
        return super().get_permissions()

    # Liste des organisations: organisation/
    def list(self, request):
        organisations = Organisation.objects.all().distinct()
        serializer = OrganisationSerializer(organisations, many=True)
        return Response(serializer.data)

    # Creation d'une organisation: organisation/
    def create(self, request):
        serializer = OrganisationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Une organisation par son id: organisation/{id}/
    def retrieve(self, request, pk=None):
        try:
            organisation = Organisation.objects.get(pk=pk)
        except Organisation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OrganisationSerializer(organisation)
        return Response(serializer.data)

    # Mise a jour d'une organisation: organisation/{id}/
    def update(self, request, pk=None):
        try:
            organisation = Organisation.objects.get(pk=pk)
        except Organisation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OrganisationSerializer(organisation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Mise a jour partielle d'une organisation: organisation/{id}/ avec PATCH
    def partial_update(self, request, pk=None):
        try:
            organisation = Organisation.objects.get(pk=pk)
        except Organisation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OrganisationSerializer(organisation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Liste des membres d'une organisation: organisation/{id}/list_members/
    @action(detail=True, methods=['get'], url_path='list_members')
    def list_members(self, request, pk=None):
        organisation = self.get_object()
        members = organisation.members.all().distinct()  # Assuming a related_name 'members'
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Liste des membres active d'une organisation: organisation/{id}/list_members_active/
    @action(detail=True, methods=['get'], url_path='list_members_active')
    def list_members_active(self, request, pk=None):
        organisation = self.get_object()
        members = organisation.members.filter(active=True).distinct()
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Liste des organisations actives: organisation/list_active_organisations/
    @action(detail=False, methods=['get'])
    def list_active_organisations(self, request):
        active_organisations = Organisation.objects.filter(active=True).distinct()
        serializer = self.get_serializer(active_organisations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Desactiver une organisation: organisation/{id}/deactiver
    @action(detail=True, methods=['post'], url_path='deactivate')
    def deactivate_org(self, request, pk=None):
        organisation = self.get_object()
        if organisation.active:
            organisation.active = False
            organisation.save()
            return Response({'status': 'organisation deactivated'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'organisation already deactivated'}, status=status.HTTP_400_BAD_REQUEST)

    # Liste des articles d'une organisation: organisation/{id}/list_articles
    @action(detail=True, methods=['get'])
    def list_articles(self, request, pk=None):
        try:
            organisation = Organisation.objects.get(pk=pk)
        except Organisation.DoesNotExist:
            return Response({"error": "Organisation not found."}, status=404)

        members = organisation.members.all().distinct()
        #articles = organisation.articles.all()  # Obtenir tous les articles de l'organisation
        articles = Article.objects.filter(member__in=members).distinct()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    # Liste des articles actifs d'une organisation: organisation/{id}/list_articles_actif
    @action(detail=True, methods=['get'])
    def list_articles_actif(self, request, pk=None):
        try:
            organisation = Organisation.objects.get(pk=pk)
        except Organisation.DoesNotExist:
            return Response({"error": "Organisation not found."}, status=404)

        members = organisation.members.all().distinct()
        # articles = organisation.articles.all()  # Obtenir tous les articles de l'organisation
        articles = Article.objects.filter(member__in=members, active=True).distinct()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    # Liste des articles actifs d'une organisation et d'une categorie: organisation/{id}/article_actif/categorie/{id}/
    @action(detail=True, methods=['get'], url_path='article_actif/categorie/(?P<category_id>[^/.]+)')
    def list_active_articles_by_category(self, request, pk=None, category_id=None):
        try:
            organisation = Organisation.objects.get(pk=pk)
        except Organisation.DoesNotExist:
            return Response({"error": "Organisation not found."}, status=404)

        # Obtenir tous les membres de l'organisation
        members = organisation.members.all().distinct()

        # Obtenir tous les articles actifs de la catégorie spécifiée gérés par les membres de l'organisation
        articles = Article.objects.filter(
            category_id=category_id,
            active=True,
            member__in=members
        ).distinct()

        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    # Liste des articles d'une organisation et d'une categorie: organisation/{id}/article/categorie/{id}/
    @action(detail=True, methods=['get'], url_path='article/categorie/(?P<category_id>[^/.]+)')
    def list_articles_by_category(self, request, pk=None, category_id=None):
        try:
            organisation = Organisation.objects.get(pk=pk)
        except Organisation.DoesNotExist:
            return Response({"error": "Organisation not found."}, status=404)

        # Obtenir tous les membres de l'organisation
        members = organisation.members.all().distinct()

        # Obtenir tous les articles de la catégorie spécifiée gérés par les membres de l'organisation
        articles = Article.objects.filter(
            category_id=category_id,
            member__in=members
        ).distinct()

        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    # Uploader un logo
    # def upload_logo(request):
    #     if request.method == 'POST':
    #         form = PersonneForm(request.POST, request.FILES)
    #         if form.is_valid():
    #             form.save()
    #             return redirect('success')
    #     else:
    #         form = PersonneForm()
    #     return render(request, 'upload_logo.html', {'form': form})
    #
    # def success(request):
    #     return HttpResponse('Photo téléchargée avec succès')

