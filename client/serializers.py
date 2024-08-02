from rest_framework import serializers
from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    # Vous pouvez ajouter des champs personnalisés ici si nécessaire

    class Meta:
        model = Client
        fields = ['email', 'name', 'phone', 'active']  # Liste des champs à inclure dans le sérialiseur

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
        """
        Crée une instance de Client à partir des données validées.
        """
        # Vous pouvez ajouter des logiques personnalisées pour la création ici si nécessaire
        return Client.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Met à jour une instance existante de Client avec les données validées.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance
