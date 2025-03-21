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
        # serializer = OrganisationSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # Récupérer les données de la requête
        logo = request.FILES.get('logo')
        label = request.data.get('label')
        description = request.data.get('description')
        phone = request.data.get('phone')

        # Vérifier si l'organisation existe déjà
        if Organisation.objects.filter(label=label).exists():
            return Response(
                {'message': 'L\'organisation existe déjà.', 'status': 'error'},
                status=status.HTTP_200_OK
            )

        # Créer une nouvelle instance d'Organisation
        organisation = Organisation(
            logo=logo,
            label=label,
            description=description,
            phone=phone
        )

        # Enregistrer l'organisation dans la base de données
        organisation.save()

        # Préparer les données à renvoyer
        response_data = {
            'message': 'Organisation créée avec succès',
            'status': 'success'
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        organisation = get_object_or_404(Organisation, pk=pk)
        serializer = OrganisationSerializer(organisation)
        return Response(serializer.data)

    def update(self, request, pk=None):
        # organisation = get_object_or_404(Organisation, pk=pk)
        # serializer = OrganisationSerializer(organisation, data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # Vérifier si l'organisation existe
        try:
            organisation = Organisation.objects.get(pk=pk)
        except Organisation.DoesNotExist:
            return Response(
                {'message': 'Organisation non trouvée.', 'status': 'error'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Récupérer les données de la requête
        label = request.data.get('label', organisation.label)
        description = request.data.get('description', organisation.description)
        phone = request.data.get('phone', organisation.phone)

        # Mettre à jour les champs de l'organisation
        organisation.label = label
        organisation.description = description
        organisation.phone = phone

        # Enregistrer les modifications
        organisation.save()

        # Préparer les données à renvoyer
        response_data = {
            'message': 'Organisation mise à jour avec succès',
            'status': 'success',
        }

        return Response(response_data, status=status.HTTP_200_OK)

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
        return Response({"detail": "Aucune organisation associée à cet utilisateur."},
                            status=status.HTTP_200_OK)
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

import os
from django.conf import settings


def serve_image(request):
    # Nom du fichier image passé en paramètre GET
    image_name = request.GET.get('image')

    # Chemin complet vers le fichier image
    image_name = image_name[1:] 
    image_path = os.path.join(settings.BASE_DIR, image_name)

    # Vérifie si le fichier image existe et s'il est dans le répertoire autorisé
    if os.path.exists(image_path) and os.path.commonpath([image_path, settings.MEDIA_ROOT]) == settings.MEDIA_ROOT:
        with open(image_path, 'rb') as image_file:
            content_type = 'image/jpeg'  # Valeur par défaut
            if image_name.endswith('.png'):
                content_type = 'image/png'
            elif image_name.endswith('.gif'):
                content_type = 'image/gif'
            # Ajoutez d'autres types si nécessaire

            response = HttpResponse(image_file.read(), content_type=content_type)
            response['Content-Disposition'] = f'inline; filename="{os.path.basename(image_name)}"'
            return response
    else:
        return HttpResponse('L\'image demandée n\'existe pas', status=404)

from django.db import transaction
from categorie.models import Categorie
from article.models import Article
from organisation.models import Organisation

def vider_tables(request):
        # Vider la table Article
        Article.objects.all().delete()
        
        # Vider la table Categorie
        Categorie.objects.all().delete()
          # Vider la table Organisation
        Organisation.objects.all().delete()
from django.shortcuts import get_object_or_404, redirect, render
from .models import Organisation

def recuperer_et_supprimer_organisation(request):
    # Récupérer l'organisation par ID
    organisation = get_object_or_404(Categorie, id=10)

    organisation.delete()