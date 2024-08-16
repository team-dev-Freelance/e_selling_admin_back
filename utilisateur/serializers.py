from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from utilisateur.models import Client


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        # Essayez d'authentifier d'abord en tant que Client
        user = authenticate(request=self.context.get('request'), username=username, password=password)

        if not user:
            # Si l'authentification en tant que Client échoue, essayez en tant que Member
            try:
                from utilisateur.models import Member
                member_user = Member.objects.get(username=username)
                user = authenticate(request=self.context.get('request'), username=member_user.username,
                                    password=password)
            except Member.DoesNotExist:
                pass

        if user:
            # Si l'utilisateur est trouvé, retournez le token JWT
            attrs['user'] = user
            return super().validate(attrs)
        else:
            # Si aucun utilisateur n'est trouvé, retournez une erreur
            raise serializers.ValidationError({"detail": "No active account found with the given credentials"})



