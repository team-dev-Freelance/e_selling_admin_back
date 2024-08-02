from rest_framework import viewsets

from acheter.models import Acheter
from acheter.serializers import AcheterSerializer
from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from article.models import Article
from article.serializers import ArticleSerializer
from member.models import Member
from organisation.models import Organisation


# Create your views here.

class AcheterViewSet(viewsets.ModelViewSet):
    queryset = Acheter.objects.all()
    serializer_class = AcheterSerializer

    # Liste des achats: acheter/
    def list(self, request):
        acheters = Acheter.objects.all()
        serializer = AcheterSerializer(acheters, many=True)
        return Response(serializer.data)

    # Creation un achat: acheter/
    def create(self, request):
        serializer = AcheterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Un acheter par son id: acheter/{id}/
    def retrieve(self, request, pk=None):
        try:
            acheter = Acheter.objects.get(pk=pk)
        except Acheter.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AcheterSerializer(acheter)
        return Response(serializer.data)

    # Mise a jour d'un acheter: acheter/{id}/
    def update(self, request, pk=None):
        try:
            acheter = Acheter.objects.get(pk=pk)
        except Acheter.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AcheterSerializer(acheter, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Mise a jour partielle d'un acheter: acheter/{id}/ avec PATCH
    def partial_update(self, request, pk=None):
        try:
            acheter = Acheter.objects.get(pk=pk)
        except Acheter.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AcheterSerializer(acheter, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Liste des achats actives: acheter/list_active_acheter/
    @action(detail=False, methods=['get'])
    def list_active_acheter(self, request):
        active_acheter = Acheter.objects.filter(active=True)
        serializer = self.get_serializer(active_acheter, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Liste des achats actives d'une organisation: acheter/list_active_acheter/organisation/{id}/
    @action(detail=False, methods=['get'], url_path='list_active_acheter/organisation/(?P<organisation_id>[^/.]+)')
    def list_active_acheter(self, request, organisation_id=None):
        try:
            organisation = Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        members = organisation.members.all().distinct()
        # articles = organisation.articles.all()  # Obtenir tous les articles de l'organisation
        articles = Article.objects.filter(active=True, member__in=members).distinct()
        acheter_list = Acheter.objects.filter(active=True, article__in=articles).distinct()
        serializer = AcheterSerializer(acheter_list, many=True)
        return Response(serializer.data)

    # Liste des achats actives d'une organisation pour un membre: acheter/list_active_acheter/organisation/{id}/member/{id}/
    @action(detail=False, methods=['get'], url_path='list_active_acheter_member/organisation/(?P<organisation_id>[^/.]+)/member/(?P<member_id>[^/.]+)')
    def list_active_acheter_by_member(self, request, organisation_id=None, member_id=None):
        try:
            organisation = Organisation.objects.get(pk=organisation_id)
            # member = Member.objects.get(pk=member_id)
        except Organisation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # members = organisation.members.all().distinct()
        # articles = organisation.articles.all()  # Obtenir tous les articles de l'organisation
        articles = Article.objects.filter(active=True, member_id=member_id).distinct()
        acheter_list = Acheter.objects.filter(active=True, article__in=articles).distinct()
        serializer = AcheterSerializer(acheter_list, many=True)
        return Response(serializer.data)

    # Desactiver un achats: acheter/{id}/deactiver
    @action(detail=True, methods=['post'], url_path='deactivate')
    def deactivate_acheter(self, request, pk=None):
        acheter = self.get_object()
        if acheter.active:
            acheter.active = False
            acheter.save()
            return Response({'status': 'achat deactivated'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'achat already deactivated'}, status=status.HTTP_400_BAD_REQUEST)