from django.utils.crypto import get_random_string
from rest_framework import serializers

# from .models import Client
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from utilisateur.models import Client


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Ajouter des données personnalisées au token si nécessaire
        return token


class ClientSerializer(serializers.ModelSerializer):
    # organisation_id = serializers.IntegerField(required=False, write_only=True)
    # rule_id = serializers.IntegerField(required=False, write_only=True)

    class Meta:
        model = Client
        fields = ['id', "email" , "nom" , "phone"  , "logo"]
