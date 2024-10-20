from rest_framework import serializers

from rule.models import Role
from rule.serializers import RoleSerializer
from utilisateur.models import Client

# from .models import Client


from rest_framework import serializers


class ClientSerializer(serializers.ModelSerializer):
    rule = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['id', 'username', 'email', 'phone', 'rule', 'logo', 'password', 'status', 'active']

    def get_rule(self, obj):
        return RoleSerializer(obj.rule).data if obj.rule else None

    def get_logo(self, obj):
        # Vérifiez si l'objet a un logo et renvoyez l'URL
        return obj.logo.url if obj.logo else None

    def validate_phone(self, value):
        """
        Validation personnalisée pour le champ `phone`.
        """
        if not value.startswith(('65', '67', '68', '69')):
            raise serializers.ValidationError('Le numéro doit commencer par 65, 67, 68 ou 69.')
        if len(value) != 9 or not value.isdigit():
            raise serializers.ValidationError('Le numéro de téléphone doit avoir 9 chiffres.')
        return value

    def create(self, validated_data):
        # Assurez-vous que le mot de passe est fourni dans les données validées
        password = validated_data.pop('password', None)
        client = super().create(validated_data)
        if password:
            client.set_password(password)
            client.save()
        return client
