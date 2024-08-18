from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status as drf_status, status

from organisation.serializers import OrganisationSerializer
from utilisateur.models import Utilisateur
from utilisateur.serializers import MyTokenObtainPairSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == drf_status.HTTP_200_OK:
            try:
                user = self.get_serializer().user
                if user:
                    user.status = True
                    user.save()
                else:
                    # Logique à gérer si l'utilisateur n'est pas trouvé
                    return Response({"detail": "Utilisateur non trouvé"}, status=drf_status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                # Gérer les autres exceptions qui peuvent se produire
                return Response({"detail": "Une erreur s'est produite lors de la mise à jour du statut."},
                                status=drf_status.HTTP_500_INTERNAL_SERVER_ERROR)

        return response


class LogoutView(APIView):

    def post(self, request):
        user = request.user
        user.status = False
        user.save()
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)


User = get_user_model()


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


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not user.check_password(current_password):
            return Response({"current_password": "Le mot de passe actuel est incorrect."},
                            status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"new_password": "Les nouveaux mots de passe ne correspondent pas."},
                            status=status.HTTP_400_BAD_REQUEST)

        if current_password == new_password:
            return Response({"new_password": "Le nouveau mot de passe ne peut pas être identique à l'ancien."},
                            status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Le mot de passe a été changé avec succès."}, status=status.HTTP_200_OK)
