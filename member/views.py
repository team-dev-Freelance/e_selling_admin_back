from rest_framework import viewsets

from permissions import IsAdminOrUser, IsUser
from utilisateur.models import Member

# from .models import Member
from .serializers import MemberSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
# from rest_framework_simplejwt.views import TokenObtainPairView
# from .serializers import MyTokenObtainPairSerializer


# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer
#

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def get_permissions(self):
        if self.action in ['create', 'partial_update', 'deactivate_user', 'list', 'list_active_members', 'retrieve',
                           'update']:
            self.permission_classes = [IsAdminOrUser]
        return super().get_permissions()

    #Dessactiver un membre
    @action(detail=True, methods=['post'], url_path='deactivate')
    def deactivate_user(self, request, pk=None):
        user = self.get_object()
        if user.active:
            user.active = False
            user.save()
            return Response({'status': 'user deactivated'}, status=status.HTTP_200_OK)
        else:
            user.active = True
            user.save()
            return Response({'status': 'user activated'}, status=status.HTTP_200_OK)

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

    def create(self, request):
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            member = Member(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                phone=serializer.validated_data['phone'],
                rule=serializer.validated_data['rule'],
                organisation=serializer.validated_data['organisation'],
            )
            member.set_password(serializer.validated_data['password'])
            member.save()
            return Response(MemberSerializer(member).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def create(self, request):
    #     serializer = MemberSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
