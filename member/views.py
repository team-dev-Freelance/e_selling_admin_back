from rest_framework import viewsets

from article.models import Article
from organisation.models import Organisation
from privilegies.models import Privilegies, Privilege
from rule.models import Rule
from .models import Member
from .serializers import MemberSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    #Dessactiver un membre
    @action(detail=True, methods=['post'], url_path='deactivate')
    def deactivate_user(self, request, pk=None):
        user = self.get_object()
        if user.active:
            user.active = False
            user.save()
            return Response({'status': 'user deactivated'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'user already deactivated'}, status=status.HTTP_400_BAD_REQUEST)

    # Liste des membres: member/
    def list(self, request):
        members = Member.objects.all().distinct()
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)

    # Liste des membres actifs: member/list_active_members/
    @action(detail=False, methods=['get'], url_path='list_active_members')
    def list_active_members(self, request):
        members = Member.objects.filter(active=True).distinct()
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)

    # Creation d'une member: member/
    # def create(self, request):
    #     serializer = MemberSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Un membre par son id: member/{id}/
    def retrieve(self, request, pk=None):
        try:
            member = Member.objects.get(pk=pk)
        except Member.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MemberSerializer(member)
        return Response(serializer.data)

    # Mise a jour d'un membre: member/{id}/
    def update(self, request, pk=None):
        try:
            member = Member.objects.get(pk=pk)
        except Member.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MemberSerializer(member, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Mise a jour partielle d'un membre: member/{id}/ avec PATCH
    def partial_update(self, request, pk=None):
        try:
            member = Member.objects.get(pk=pk)
        except Member.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MemberSerializer(member, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

