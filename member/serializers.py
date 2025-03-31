from django.utils.crypto import get_random_string
from rest_framework import serializers

# from .models import Member
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from utilisateur.models import Member


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Ajouter des données personnalisées au token si nécessaire
        return token


class MemberSerializer(serializers.ModelSerializer):
    # organisation_id = serializers.IntegerField(required=False, write_only=True)
    # rule_id = serializers.IntegerField(required=False, write_only=True)

    class Meta:
        model = Member
        # fields = ['id', 'username', 'email', 'phone', 'organisation_id', 'rule_id']
        fields = ['id', "email" , "name" , "phone"  , "logo"]

    def create(self, validated_data):
        # `validated_data` ne contient pas `rule` ou `organisation` ici
        return Member.objects.create(**validated_data)

    def validate_phone(self, value):
        if not value.startswith(('62', '65', '67', '68', '69')):
            raise serializers.ValidationError('Le numéro doit commencer par 62, 65, 67, 68 ou 69.')
        if len(value) != 9 or not value.isdigit():
            raise serializers.ValidationError('Le numéro de téléphone doit avoir 9 chiffres.')
        return value
