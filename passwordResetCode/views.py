from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from passwordResetCode.models import PasswordResetCode
from utilisateur.models import Utilisateur


class SendPasswordResetCodeView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "L'email est requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Vérifier si l'utilisateur avec cet e-mail existe
            user = Utilisateur.objects.get(email=email)

            # Générer un code de réinitialisation aléatoire
            code = get_random_string(length=6, allowed_chars='1234567890')
            PasswordResetCode.objects.create(user=user, code=code)

            # Envoyer l'e-mail avec le code
            send_mail(
                'Votre code de réinitialisation de mot de passe',
                f'Utilisez le code suivant pour réinitialiser votre mot de passe : {code}',
                'no-reply@gicconnect.com',
                [email],
                fail_silently=False,
            )
            return Response({"message": "Code envoyé à votre adresse e-mail."}, status=status.HTTP_200_OK)

        except Utilisateur.DoesNotExist:
            # Gérer le cas où l'utilisateur n'existe pas
            return Response({"error": "Utilisateur avec cet e-mail n'existe pas."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Gérer les erreurs inattendues
            return Response({"error": f"Erreur lors de l'envoi de l'e-mail : {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyResetCodeView(APIView):
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')

        if not email or not code:
            return Response({"error": "L'email et le code sont requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Vérifier si l'utilisateur avec cet e-mail existe
            user = Utilisateur.objects.get(email=email)

            # Vérifier si le code est valide
            reset_code = PasswordResetCode.objects.filter(user=user, code=code).first()
            if reset_code and not reset_code.is_expired():
                return Response({"message": "Code vérifié, redirection vers la réinitialisation du mot de passe."},
                                status=status.HTTP_200_OK)
            return Response({"error": "Code invalide ou expiré."}, status=status.HTTP_400_BAD_REQUEST)

        except Utilisateur.DoesNotExist:
            # Gérer le cas où l'utilisateur n'existe pas
            return Response({"error": "Utilisateur avec cet e-mail n'existe pas."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Gérer les erreurs inattendues
            return Response({"error": f"Erreur lors de la vérification du code : {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

