from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from rest_framework import viewsets

from e_selling_admin_back import settings
from organisation.models import Organisation
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

    def create(self, request, *args, **kwargs):
        # Passez le contexte de la requête au sérialiseur
        serializer = self.get_serializer(data=request.data, context={'request': request})

        # Valide les données
        if serializer.is_valid():
            # Récupère l'utilisateur courant
            # user = self.request.user

            # # Détermine le rôle
            # if user.rule.role == 'USER':
            #     role, _ = Role.objects.get_or_create(role='MEMBER')
            # else:
            #     role, _ = Role.objects.get_or_create(role='USER')

            # # Détermine l'organisation
            # organisation_id = request.data.get('organisation_id')
            # if user.rule.role == 'USER':
            #     organisation = user.member.organisation
            # else:
            #     organisation = Organisation.objects.get(id=organisation_id) if organisation_id else None

            # Génère un mot de passe aléatoire
            # password = "00000"
            password = get_random_string(length=8)
            role, _ = Role.objects.get_or_create(role='MEMBER')
            # Crée le membre avec le mot de passe généré
            member = serializer.save(rule=role)
            member.set_password(password)
            member.save()

            # Envoi de l'email avec les informations de connexion
            self.send_welcome_email(member, password)

            return Response(MemberSerializer(member).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_welcome_email(self, member, password):
        subject = 'Bienvenue dans GIC Connect'
        message = f"""
        Bonjour {member.name},

        Votre compte a été créé avec succès. Voici vos informations de connexion :

        - Nom d'utilisateur : {member.email}
        - Mot de passe : {password}

        Merci de nous avoir rejoints !

        Cordialement,
        L'équipe GIC Connect
        """
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [member.email]

        send_mail(subject, message, from_email, recipient_list)

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
