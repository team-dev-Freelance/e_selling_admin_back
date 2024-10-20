from django.shortcuts import render, redirect, get_object_or_404
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

    # def get_permissions(self):
    #     if self.action in ['partial_update', 'retrieve', 'update', 'list_members', 'deactivate_org', 'list_members_active']:
    #         self.permission_classes = [IsAdmin]
    #     elif self.action in ['list_articles', 'list_articles_by_category']:
    #         self.permission_classes = [IsMemberOfOrganisation]
    #     elif self.action in ['list', 'create', 'retrieve', 'list_active_organisations']:
    #         self.permission_classes = [IsAdmin]
    #     elif self.action in ['list_active_organisation', 'list_articles_by_category']:
    #         self.permission_classes = [IsUser]
    #     return super().get_permissions()

    def list(self, request):
        organisations = Organisation.objects.all().distinct()
        serializer = OrganisationSerializer(organisations, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = OrganisationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        organisation = get_object_or_404(Organisation, pk=pk)
        serializer = OrganisationSerializer(organisation)
        return Response(serializer.data)

    def update(self, request, pk=None):
        organisation = get_object_or_404(Organisation, pk=pk)
        serializer = OrganisationSerializer(organisation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        organisation = get_object_or_404(Organisation, pk=pk)
        serializer = OrganisationSerializer(organisation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='list_members')
    def list_members(self, request):
        member = getattr(request.user, 'member', None)
        if member:
            organisation = member.organisation
            if organisation:
                members = organisation.members.all().distinct()
                serializer = MemberSerializer(members, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"detail": "Aucune organisation associée à cet utilisateur."},
                            status=status.HTTP_404_NOT_FOUND)
        return Response({"detail": "L'utilisateur courant n'est pas un membre."}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['get'], url_path='list_members_active')
    def list_members_active(self, request):
        member = getattr(request.user, 'member', None)
        if member:
            organisation = member.organisation
            if organisation:
                members = organisation.members.filter(active=True).distinct()
                serializer = MemberSerializer(members, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"detail": "Aucune organisation associée à cet utilisateur."},
                            status=status.HTTP_404_NOT_FOUND)
        return Response({"detail": "L'utilisateur courant n'est pas un membre."}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['get'], url_path='list_active_organisations')
    def list_active_organisations(self, request):
        active_organisations = Organisation.objects.filter(active=True).distinct()
        serializer = OrganisationSerializer(active_organisations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='deactivate')
    def deactivate_org(self, request):
        organisation_id = request.data.get('id')
        organisation = get_object_or_404(Organisation, id=organisation_id)
        organisation.active = not organisation.active
        organisation.save()
        status_message = 'organisation activated' if organisation.active else 'organisation deactivated'
        return Response({'status': status_message}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='list_articles')
    def list_articles(self, request):
        member = getattr(request.user, 'member', None)
        if member:
            organisation = member.organisation
            if organisation:
                articles = Article.objects.filter(member__organisation=organisation).distinct()
                serializer = ArticleSerializer(articles, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"detail": "Aucune organisation associée à cet utilisateur."},
                            status=status.HTTP_404_NOT_FOUND)
        return Response({"detail": "L'utilisateur courant n'est pas un membre."}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['get'], url_path='list_articles_actif')
    def list_articles_actif(self, request):
        member = getattr(request.user, 'member', None)
        if member:
            organisation = member.organisation
            if organisation:
                articles = Article.objects.filter(member__organisation=organisation, active=True).distinct()
                serializer = ArticleSerializer(articles, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"detail": "Aucune organisation associée à cet utilisateur."},
                            status=status.HTTP_404_NOT_FOUND)
        return Response({"detail": "L'utilisateur courant n'est pas un membre."}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['get'], url_path='article_actif/categorie/(?P<category_id>[^/.]+)')
    def list_active_articles_by_category(self, request, category_id=None):
        member = getattr(request.user, 'member', None)
        if member:
            organisation = member.organisation
            if organisation:
                articles = Article.objects.filter(member__organisation=organisation, category_id=category_id, active=True).distinct()
                serializer = ArticleSerializer(articles, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"detail": "Aucune organisation associée à cet utilisateur."},
                            status=status.HTTP_404_NOT_FOUND)
        return Response({"detail": "L'utilisateur courant n'est pas un membre."}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['get'], url_path='article/categorie/(?P<category_id>[^/.]+)')
    def list_articles_by_category(self, request, category_id=None):
        member = getattr(request.user, 'member', None)
        if member:
            organisation = member.organisation
            if organisation:
                articles = Article.objects.filter(member__organisation=organisation, category_id=category_id).distinct()
                serializer = ArticleSerializer(articles, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"detail": "Aucune organisation associée à cet utilisateur."},
                            status=status.HTTP_404_NOT_FOUND)
        return Response({"detail": "L'utilisateur courant n'est pas un membre."}, status=status.HTTP_403_FORBIDDEN)

