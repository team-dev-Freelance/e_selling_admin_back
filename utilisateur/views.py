from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.http.response import Http404
from django.utils.crypto import get_random_string
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from client.serializers import ClientSerializer
from organisation.serializers import OrganisationSerializer

from passwordResetCode.models import PasswordResetCode

from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Utilisateur, Client
from .serializers import MyTokenObtainPairSerializer
import logging

logger = logging.getLogger(__name__)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        logger.debug(f'Response data: {response.data}')
        return response


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            user = request.user
            user.status = False
            user.save()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        organisation_data = None

        # Vérifiez si l'utilisateur est un Member et a une organisation
        if hasattr(user, 'member'):
            organisation = user.member.organisation
            organisation_data = OrganisationSerializer(organisation).data

        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.rule.role if hasattr(user, 'rule') else None,
            "organisation": organisation_data,  # Incluez l'objet organisation ici
            "is_admin": user.is_staff,
        }
        return Response(user_data, status=status.HTTP_200_OK)


class CurrentClientView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            serializer = ClientSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des données utilisateur : {str(e)}")
            return Response({"error": "Une erreur s'est produite lors de la récupération des données utilisateur."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChangePasswordView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Récupération des données
        user = request.user  # Récupère l'utilisateur courant
        email = user.email
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        try:
            # Rechercher l'utilisateur dans la base de données par nom d'utilisateur ou email
            user = Utilisateur.objects.get(email=email)  # ou email=email selon ce que vous préférez

            # Vérification du mot de passe actuel
            if not user.check_password(current_password):
                return Response({"current_password": "Le mot de passe actuel est incorrect."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Vérification de la correspondance des nouveaux mots de passe
            if new_password != confirm_password:
                return Response({"new_password": "Les nouveaux mots de passe ne correspondent pas."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Vérification si le nouveau mot de passe est identique à l'ancien
            if current_password == new_password:
                return Response({"new_password": "Le nouveau mot de passe ne peut pas être identique à l'ancien."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Mise à jour du mot de passe
            user.set_password(new_password)
            user.save()

            return Response({"message": "Le mot de passe a été changé avec succès."}, status=status.HTTP_200_OK)

        except Utilisateur.DoesNotExist:
            return Response({"error": "Utilisateur non trouvé."}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Récupération des données
        email = request.data.get("email")  # ou email, selon ce que vous préférez
        # current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        try:
            # Rechercher l'utilisateur dans la base de données par nom d'utilisateur ou email
            user = Utilisateur.objects.get(email=email)  # ou email=email selon ce que vous préférez

            # Vérification de la correspondance des nouveaux mots de passe
            if new_password != confirm_password:
                return Response({"new_password": "Les nouveaux mots de passe ne correspondent pas."},
                                status=status.HTTP_400_BAD_REQUEST)

             # Mise à jour du mot de passe
            user.set_password(new_password)
            user.save()

            return Response({"message": "Le mot de passe a été changé avec succès."}, status=status.HTTP_200_OK)

        except Utilisateur.DoesNotExist:
            return Response({"error": "Utilisateur non trouvé."}, status=status.HTTP_400_BAD_REQUEST)


class ResendPasswordResetCodeView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = Utilisateur.objects.get(email=email)
            # Supprimer les anciens codes de réinitialisation s'ils existent
            PasswordResetCode.objects.filter(user=user).delete()
            # Générer un nouveau code
            code = get_random_string(length=6, allowed_chars='1234567890')
            PasswordResetCode.objects.create(user=user, code=code)
            # Envoyer le code par email
            send_mail(
                'Votre nouveau code de réinitialisation de mot de passe',
                f'Utilisez le code suivant pour réinitialiser votre mot de passe : {code}',
                'no-reply@gicconnect.com',
                [email],
                fail_silently=False,
            )
            return Response({"message": "Nouveau code envoyé à votre adresse e-mail."}, status=status.HTTP_200_OK)
        except Utilisateur.DoesNotExist:
            return Response({"error": "Utilisateur avec cet e-mail n'existe pas."}, status=status.HTTP_400_BAD_REQUEST)


class UpdateClientView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        client = self.get_object(pk)
        serializer = ClientSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        try:
            return Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            raise Http404

