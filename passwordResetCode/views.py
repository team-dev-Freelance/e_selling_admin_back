from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from passwordResetCode.models import PasswordResetCode
from utilisateur.models import Utilisateur


# Remplacez `User` par `Utilisateur` dans les importations et dans la vue

class SendPasswordResetCodeView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "L'email est requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Utilisateur.objects.get(email=email)  # Utilisez Utilisateur au lieu de User
            code = get_random_string(length=6, allowed_chars='1234567890')
            PasswordResetCode.objects.create(user=user, code=code)
            send_mail(
                'Votre code de réinitialisation de mot de passe',
                f'Utilisez le code suivant pour réinitialiser votre mot de passe : {code}',
                'no-reply@gicconnect.com',
                [email],
                fail_silently=False,
            )
            return Response({"message": "Code envoyé à votre adresse e-mail."}, status=status.HTTP_200_OK)
        except Utilisateur.DoesNotExist:  # Utilisez Utilisateur au lieu de User
            return Response({"error": "Utilisateur avec cet e-mail n'existe pas."}, status=status.HTTP_400_BAD_REQUEST)


class VerifyResetCodeView(APIView):
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        try:
            user = Utilisateur.objects.get(email=email)
            reset_code = PasswordResetCode.objects.filter(user=user, code=code).first()
            if reset_code and not reset_code.is_expired():
                return Response({"message": "Code vérifié, redirection vers la réinitialisation du mot de passe."},
                                status=status.HTTP_200_OK)
            return Response({"error": "Code invalide ou expiré."}, status=status.HTTP_400_BAD_REQUEST)
        except Utilisateur.DoesNotExist:
            return Response({"error": "Utilisateur avec cet e-mail n'existe pas."}, status=status.HTTP_400_BAD_REQUEST)
