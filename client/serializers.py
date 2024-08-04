from rest_framework import serializers
from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    # Vous pouvez ajouter des champs personnalisés ici si nécessaire

    class Meta:
        model = Client
        # fields = ['email', 'name', 'phone', 'articles', 'logo']  # Liste des champs à inclure dans le sérialiseur
        exclude = ['active']

    def validate_phone(self, value):
        """
        Validation personnalisée pour le champ `phone`.
        """
        if not value.startswith(('62', '65', '67', '68', '69')):
            raise serializers.ValidationError('Le numéro doit commencer par 62, 65, 67, 68 ou 69.')
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
