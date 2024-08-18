from rest_framework import serializers

from rule.models import Role
from utilisateur.models import Client


# from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    rule = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), write_only=True)

    class Meta:
        model = Client
        exclude = ['active', 'is_staff', 'is_superuser', 'password', 'last_login']

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
        return Client.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance
