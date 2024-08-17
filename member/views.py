from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from rest_framework import viewsets

from permissions import IsAdminOrUser, IsUser
from rule.models import Role
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

    # def get_permissions(self):
    #     if self.action in ['create', 'partial_update', 'deactivate_user', 'list', 'list_active_members', 'retrieve',
    #                        'update']:
    #         self.permission_classes = [IsAdminOrUser]
    #     return super().get_permissions()

    #Dessactiver un membre
    @action(detail=False, methods=['post'], url_path='deactivate')
    def deactivate_user(self, request):
        user_id = request.data.get('id')
        user = get_object_or_404(Member, id=user_id)
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
            password = get_random_string(length=12)

            member = Member(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                phone=serializer.validated_data['phone'],
                rule=serializer.validated_data.pop('rule_id'),
                organisation=serializer.validated_data.pop('organisation_id')
            )
            user = self.request.user
            send_mail(
                'Votre nouveau compte',
                f'Bonjour,\nVos identifiants de connexion sont:\nVotre nom d\'utilisateur est: {member.username}\n'
                f'Votre mot de passe est : {password}',
                user.email,
                [member.email],
                fail_silently=False,
            )
            member.set_password(password)
            member.save()
            return Response(MemberSerializer(member).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            # Vérifier si le rôle du membre est "MEMBER"
            if request.user.role.name == 'USER':
                password = get_random_string(length=12)

                member = Member(
                    username=serializer.validated_data['username'],
                    email=serializer.validated_data['email'],
                    phone=serializer.validated_data['phone'],
                    role=Role.objects.get_or_create(
                role='MEMBER',
                active=True),
                    organisation=request.user.organisation
                    # Affecter automatiquement à l'organisation de l'utilisateur courant
                )
                user = self.request.user
                send_mail(
                    'Votre nouveau compte',
                    f'Bonjour,\nVos identifiants de connexion sont:\nVotre nom d\'utilisateur est: {member.username}\n'
                    f'Votre mot de passe est : {password}',
                    user.email,
                    [member.email],
                    fail_silently=False,
                )
                member.set_password(password)
                member.save()
                return Response(MemberSerializer(member).data, status=status.HTTP_201_CREATED)
            elif request.user.role.name == 'ADMIN':
                password = get_random_string(length=12)
                member = Member(
                    username=serializer.validated_data['username'],
                    email=serializer.validated_data['email'],
                    phone=serializer.validated_data['phone'],
                    rule=Role.objects.get_or_create(
                role='USER',
                active=True),
                    organisation=serializer.validated_data.pop('organisation_id')
                )
                user = self.request.user
                send_mail(
                    'Votre nouveau compte',
                    f'Bonjour,\nVos identifiants de connexion sont:\nVotre nom d\'utilisateur est: {member.username}\n'
                    f'Votre mot de passe est : {password}',
                    user.email,
                    [member.email],
                    fail_silently=False,
                )
                member.set_password(password)
                member.save()
                return Response(MemberSerializer(member).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def create(self, request):
    #     serializer = MemberSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Un membre par son id: member/profileMember/
    @action(detail=False, methods=['get'], url_path='profileMember')
    def profile(self, request):
        try:
            member = Member.objects.get(pk=request.user.id)
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
